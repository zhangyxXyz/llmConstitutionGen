---
name: Soul 项目重要约定和最佳实践
description: 汇总Soul开发必须遵守的禁止事项和最佳实践，覆盖相机、音频、Manager、事件、网络、战斗、热更新等高风险场景的审查要点和落地建议
allowed-tools: *
permission: allow
---

# Soul 项目重要约定和最佳实践

本文档列出 Soul 项目开发中必须遵守的重要约定和推荐的最佳实践。

## ❌ 不要做的事情

### 相机系统

❌ **不要直接操作 `Camera.main`**
- 必须通过 `SoulCameraManager` 操作相机
- 直接操作会破坏相机栈管理和优先级系统

```csharp
// ❌ 错误
Camera.main.transform.position = newPos;

// ✅ 正确
SoulCameraManager.Instance.SwitchCamera(CameraType.Battle);
```

### 音频系统

❌ **不要使用 Unity 的 `AudioSource`**
- 必须使用 Wwise 音频中间件
- 使用 `AkSoundEngine` 播放音频

```csharp
// ❌ 错误
AudioSource.PlayClipAtPoint(clip, position);

// ✅ 正确
AkSoundEngine.PostEvent("Play_SFX_Gunshot", gameObject);
```

### Manager 类

❌ **不要在 Manager 类中做大改动**
- Manager 类是单例，影响范围大
- 修改前要充分评估影响
- 确保所有调用者都能正常工作

### 事件系统

❌ **不要忘记取消事件订阅**
- 未取消订阅会导致内存泄漏
- 订阅和取消订阅必须配对
- 使用相同的 Dispatcher 对象

```csharp
// ❌ 错误：没有取消订阅
private void OnEnable()
{
    EventManager.AddListener(EventType.PlayerDied, OnPlayerDied);
}
// OnDisable 中忘记取消订阅

// ✅ 正确
private void OnEnable()
{
    EventManager.AddListener(EventType.PlayerDied, OnPlayerDied);
}

private void OnDisable()
{
    EventManager.RemoveListener(EventType.PlayerDied, OnPlayerDied);
}
```

### 网络同步

❌ **不要在 RPC 中跳过参数校验**
- 所有 RPC 必须校验参数合法性
- 缺少校验会导致安全漏洞和作弊风险
- GM 命令除外

```csharp
// ❌ 错误：缺少校验
[ServerRPC]
void CmdAttack(int targetId)
{
    Attack(targetId); // 直接执行，可能被作弊利用
}

// ✅ 正确
[ServerRPC(RPCMask.WithValidation)]
void CmdAttack(int targetId)
{
    // 校验参数
    if (!IsValidTarget(targetId))
    {
        CheatPunishment.PunishCheat(this, CheatMetricsSubReasonType.InvalidParameter);
        return;
    }
    
    // 校验玩家状态
    if (!CanAttack())
    {
        return;
    }
    
    // 执行逻辑
    Attack(targetId);
}
```

### 战斗系统

❌ **不要修改战斗逻辑而不测试回放**
- 战斗回放依赖于确定性的逻辑执行
- 修改战斗逻辑必须测试回放兼容性
- 避免随机数和时间相关的非确定性操作

### 热更新

❌ **不要使用 ILRuntime 不支持的特性**
- 静态构造函数需特殊处理
- 某些 ref/out 参数用法需适配器
- 跨域继承需适配器

### 日志和存储

❌ **不要直接使用 `UnityEngine.Debug`**
- 必须使用项目封装的 `Debuger` 类
- 使用 `EDebugTag` 区分模块

```csharp
// ❌ 错误
Debug.Log("Message");

// ✅ 正确
Debuger.LogInfo(EDebugTag.Battle, "Message");
```

❌ **不要直接使用 `PlayerPrefs`**
- 必须使用项目封装的 `PrefUtils` 类
- 所有 key 必须定义在 `PrefKeyDefine` 中

```csharp
// ❌ 错误
PlayerPrefs.SetInt("Score", 100);

// ✅ 正确
PrefUtils.SetInt(PrefKeyDefine.PlayerScore, 100);
```

### 代码规范

❌ **不要使用匿名函数（Lambda）**
- 禁止使用 lambda 表达式
- 使用对象池 + 辅助类替代

```csharp
// ❌ 错误
callback = () => { DoSomething(); };

// ✅ 正确：使用对象池 + 辅助类
var loader = m_loaderPool.Get();
loader.SetData(data, OnComplete);
```

❌ **不要使用 LINQ**
- 禁止使用 `System.Linq` 命名空间
- 性能问题和 GC 压力

❌ **不要使用内部函数**
- 禁止在方法内定义函数
- 会产生闭包和 GC 分配

❌ **不要使用魔法数字**
- 单一使用的 ID：定义为有意义的常量
- 多处使用的 ID：定义为枚举类型

```csharp
// ❌ 错误
if (itemId == 10001) { }

// ✅ 正确：定义为常量
private const int HEALTH_POTION_ID = 10001;
if (itemId == HEALTH_POTION_ID) { }

// ✅ 正确：定义为枚举
public enum ItemId
{
    HealthPotion = 10001,
    ManaPotion = 10002
}
if (itemId == (int)ItemId.HealthPotion) { }
```

---

## ✅ 应该做的事情

### 对象池

✅ **使用 InstancePool 对象池**
- 频繁创建销毁的对象应使用对象池
- 减少 GC 压力，提升性能

```csharp
// 获取对象
var obj = InstancePool.Get<GameObject>(prefab);

// 使用对象
// ...

// 归还对象
InstancePool.Release(obj);
```

### 生命周期管理

✅ **配对使用协程**
- StartCoroutine 和 StopCoroutine 必须配对
- 避免协程泄漏

```csharp
private Coroutine m_coroutine;

private void StartMyCoroutine()
{
    m_coroutine = StartCoroutine(MyCoroutine());
}

private void StopMyCoroutine()
{
    if (m_coroutine != null)
    {
        StopCoroutine(m_coroutine);
        m_coroutine = null;
    }
}
```

✅ **配对使用事件订阅**
- AddListener 和 RemoveListener 必须配对
- 使用相同的 Dispatcher 对象

```csharp
private void OnEnable()
{
    BattleEngine.Instance?.Dispatcher?.AddEventListener(BattleEvent.ON_START, OnBattleStart);
}

private void OnDisable()
{
    BattleEngine.Instance?.Dispatcher?.RemoveEventListener(BattleEvent.ON_START, OnBattleStart);
}
```

✅ **配对使用资源加载卸载**
- 加载和卸载必须配对
- 避免资源泄漏

```csharp
// 加载资源
await ResourceManager.LoadAssetAsync<GameObject>(path);

// 使用资源
// ...

// 卸载资源
ResourceManager.Unload(path);
```

### 网络同步

✅ **所有 RPC 校验参数**
- 添加 `RPCMask.WithValidation`
- 校验参数合法性
- 校验玩家权限和状态
- GM 命令除外

```csharp
[ServerRPC(RPCMask.WithValidation)]
public void CmdUseItem(int itemId)
{
    // 1. 校验参数
    if (!IsValidItemId(itemId))
    {
        CheatPunishment.PunishCheat(this, CheatMetricsSubReasonType.InvalidParameter);
        return;
    }
    
    // 2. 校验玩家状态
    if (!HasItem(itemId))
    {
        return;
    }
    
    // 3. 执行逻辑
    UseItem(itemId);
}
```

### 战斗系统

✅ **修改战斗逻辑测试回放**
- 确保逻辑确定性执行
- 避免随机数和时间相关操作
- 测试回放兼容性

```csharp
// 记录战斗事件
RecordBattleEvent(new DamageEvent(targetId, damage));

// 确保确定性执行
// ❌ 错误：使用 Random
var damage = Random.Range(10, 20);

// ✅ 正确：使用确定性随机数生成器
var damage = m_battleRandom.Range(10, 20);
```

### 热更新

✅ **考虑 ILRuntime 兼容性**
- 避免使用不支持的特性
- 注意 ref/out 参数的兼容性
- 保持序列化版本兼容性

### 架构模式

✅ **遵循现有的架构模式**
- Manager Pattern：核心系统使用单例管理器
- Component Pattern：游戏实体的模块化组件
- Event System：系统间通信的插件消息系统
- Object Pooling：性能优化的实例池

### BattleWorld 引用管理

❌ **不要直接存储 BattleWorld 成员变量**

```csharp
// ❌ 错误：直接存储 BattleWorld
public class GrassTrampleManager
{
    public BattleWorld m_BattleWorld; // 可能在切换场景时失效
}

// ✅ 正确：存储 BattleWorldType，动态获取
public class GrassTrampleManager
{
    private BattleWorldType m_battleWorldType = BattleWorldType.None;
    public BattleWorld BattleWorld => BattleEngine.Instance.GetBattleWorldByWorldType(m_battleWorldType);
    
    public GrassTrampleManager(BattleWorld battleWorld)
    {
        m_battleWorldType = battleWorld.WorldType;
    }
}
```

---

## 性能优化最佳实践

### 避免的操作

```csharp
// ❌ Update 中查找对象
void Update() 
{ 
    var player = GameObject.Find("Player"); // 非常慢
}

// ❌ Update 中频繁 GetComponent
void Update() 
{ 
    GetComponent<Rigidbody>(); // 每帧调用
}

// ❌ 热路径分配内存
void Update() 
{ 
    new List<int>(); // 每帧分配，产生 GC
}

// ❌ 字符串拼接产生 GC
string log = "HP: " + hp; // 产生 GC

// ❌ 字符串插值也产生 GC
string msg = $"Frame {frameCount}, Time {time}"; // 产生 GC
```

### 推荐做法

```csharp
// ✅ 缓存引用
private GameObject m_player;
private Rigidbody m_rb;

void Start()
{
    m_player = GameObject.Find("Player");
    m_rb = GetComponent<Rigidbody>();
}

// ✅ 使用对象池
var obj = InstancePool.Get<GameObject>(prefab);

// ✅ 使用 RAII 零 GC（⚠️ 必须使用 using 语句！）
void Update()
{
    using var raiiList = new RaiiUtilList<int>();
    var list = raiiList.Value;
    // 使用 list
    // 作用域结束自动归还
}

// ❌ 错误：不使用 using 会导致内存泄漏！
void BadExample()
{
    var raiiList = new RaiiUtilList<int>(); // 缺少 using
    var list = raiiList.Value;
    // Dispose() 不会被调用，对象永远不会归还到池中！
}

// ❌ 错误：多线程场景禁止使用 RAII
void WriteTLog()
{
    // tlog 输出涉及多线程，使用 RAII 会导致数据错乱
    // using var info = new RaiiUtilObject<ItemFlowInfo>(); // ❌ 危险！
    
    // ✅ 正确：直接 new 对象
    var info = new ItemFlowInfo();
    TLogManager.Write(info);
}

// ✅ 使用 ZString 零 GC
string log = ZString.Format("HP: {0}", hp);

// ✅ 使用 StringConcatUtil（项目推荐）
var log2 = StringConcatUtil.Begin;
log2.Append("Player ").Append(playerId).Append(" HP: ").Append(hp);
Debuger.Log(log2.Tostring()); // 注意是 Tostring 不是 ToString

// ✅ 使用 Job System + Burst
[BurstCompile]
struct MyJob : IJob 
{
    public void Execute()
    {
        // 高性能计算
    }
}
```

---

## Unity 生命周期最佳实践

### MonoBehaviour 生命周期

```csharp
public class MyComponent : MonoBehaviour
{
    // 初始化引用
    private void Awake()
    {
        // 获取组件引用
        m_transform = transform;
        m_rigidbody = GetComponent<Rigidbody>();
    }
    
    // 初始化逻辑
    private void Start()
    {
        // 初始化数据
        Initialize();
    }
    
    // 订阅事件
    private void OnEnable()
    {
        EventManager.AddListener(EventType.GameStart, OnGameStart);
    }
    
    // 取消订阅事件
    private void OnDisable()
    {
        EventManager.RemoveListener(EventType.GameStart, OnGameStart);
    }
    
    // 清理资源
    private void OnDestroy()
    {
        CleanupResources();
    }
}
```

### 协程管理

```csharp
public class MyComponent : MonoBehaviour
{
    private Coroutine m_updateCoroutine;
    
    private void Start()
    {
        m_updateCoroutine = StartCoroutine(UpdateCoroutine());
    }
    
    private void OnDestroy()
    {
        // 停止协程
        if (m_updateCoroutine != null)
        {
            StopCoroutine(m_updateCoroutine);
            m_updateCoroutine = null;
        }
    }
    
    private IEnumerator UpdateCoroutine()
    {
        while (true)
        {
            // 协程逻辑
            yield return new WaitForSeconds(1.0f);
        }
    }
}
```

---

## 网络同步最佳实践

### 服务器权威架构

```csharp
public class PlayerController : NetworkBehaviour
{
    // 关键数据使用 ServerAll 同步模式
    [SyncVar(syncMode = ESyncMode.ServerAll)]
    private int m_health;
    
    // 表现数据可以使用 ClientLocal
    [SyncVar(syncMode = ESyncMode.ClientLocal)]
    public int displayScore;
    
    // 客户端请求 -> 服务器验证 -> 服务器执行
    [ServerRPC(RPCMask.WithValidation)]
    public void CmdTakeDamage(int damage)
    {
        // 服务器验证
        if (damage <= 0 || damage > 1000)
        {
            CheatPunishment.PunishCheat(this, CheatMetricsSubReasonType.InvalidParameter);
            return;
        }
        
        // 服务器执行
        m_health -= damage;
        
        // 同步到客户端（SyncVar 自动同步）
        if (m_health <= 0)
        {
            RpcOnDeath();
        }
    }
    
    // 服务器 -> 客户端
    [ClientRPC]
    private void RpcOnDeath()
    {
        // 客户端表现
        PlayDeathAnimation();
    }
}
```

### 配置使用规范

```csharp
// ❌ 客户端从表格读取关键配置
void OnClient()
{
    var buffConfig = BaseDataConfigManager.Instance.GetBuffConfig(buffId);
    float duration = buffConfig.duration; // 运营无法快速调整
}

// ✅ 服务器通过协议传递配置
[ServerOnly]
public void AddBuff(int buffId)
{
    var buffConfig = BaseDataConfigManager.Instance.GetBuffConfig(buffId);
    var syncInfo = new BuffSyncInfo
    {
        buffId = buffId,
        duration = buffConfig.duration // 服务器计算，通过协议传递
    };
    SyncToClient(syncInfo);
}

void OnClient(BuffSyncInfo syncInfo)
{
    float duration = syncInfo.duration; // 从协议获取，运营可快速调整
    ShowBuffUI(duration);
}
```

---

## 反作弊最佳实践

### RPC 参数校验

```csharp
[ServerRPC(RPCMask.WithValidation)]
public void CmdPurchaseItem(int itemId, int quantity)
{
    // 1. 参数范围校验
    if (itemId <= 0 || quantity <= 0 || quantity > 999)
    {
        CheatPunishment.PunishCheat(this, CheatMetricsSubReasonType.InvalidParameter);
        return;
    }
    
    // 2. 配置数据校验
    var itemConfig = BaseDataConfigManager.Instance.GetItemConfig(itemId);
    if (itemConfig == null)
    {
        CheatPunishment.PunishCheat(this, CheatMetricsSubReasonType.InvalidItemId);
        return;
    }
    
    // 3. 玩家状态校验
    if (!HasEnoughCurrency(itemConfig.price * quantity))
    {
        return;
    }
    
    // 4. 执行逻辑
    PurchaseItem(itemId, quantity);
}
```

### ServerOnly 标签

```csharp
// 反作弊代码添加 ServerOnly 标签
[ServerOnly]
public static partial class CheatPunishment
{
    public static void PunishCheat(PlayerActor player, CheatMetricsSubReasonType reason)
    {
        // 服务器端反作弊惩罚
        player.Kick();
    }
}

// 服务器管理器添加 ServerOnly 标签
[ServerOnly]
public class ServerBattleManager
{
    public void Initialize()
    {
        // 服务器端逻辑
    }
}
```

---

## 代码审查检查清单

### 安全性
- [ ] 所有 RPC 添加 `RPCMask.WithValidation`（GM 命令除外）
- [ ] 所有 RPC 校验参数合法性
- [ ] 关键数据使用 `ServerAll` 同步模式
- [ ] 服务器权威架构，客户端只做表现

### 性能
- [ ] 热路径避免 GC 分配
- [ ] 使用 RAII 工具类（RaiiUtilList、RaiiUtilObject）
- [ ] 使用对象池复用对象
- [ ] 缓存组件引用，避免频繁 GetComponent

### 内存管理
- [ ] 事件订阅和取消订阅配对
- [ ] 资源加载和卸载配对
- [ ] 协程 Start 和 Stop 配对
- [ ] 对象池对象正确归还

### 代码规范
- [ ] 命名符合规范（m_、s_、PascalCase）
- [ ] 禁止使用匿名函数、LINQ、内部函数
- [ ] 使用 Debuger 而不是 Debug
- [ ] 使用 PrefUtils 而不是 PlayerPrefs

### 架构模式
- [ ] 遵循 Manager Pattern
- [ ] 遵循 Component Pattern
- [ ] 使用 Event System 解耦
- [ ] 相机操作通过 SoulCameraManager
- [ ] 音频播放使用 Wwise

### 战斗系统
- [ ] 修改战斗逻辑测试回放兼容性
- [ ] 确保确定性执行
- [ ] 避免随机数和时间相关操作

### 热更新
- [ ] 避免 ILRuntime 不支持的特性
- [ ] 保持序列化版本兼容性
