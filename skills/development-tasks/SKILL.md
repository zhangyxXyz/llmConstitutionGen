---
name: Soul 项目开发任务指南
description: 提供常见开发任务的流程模板与注意事项，覆盖配置生成、相机修改、AI 行为、动画、资源等操作步骤和风险提醒
allowed-tools: *
permission: allow
---

# Soul 项目开发任务指南

本文档提供常见开发任务的完整流程和最佳实践。

## 1. 添加新配置

### 流程步骤

```
1. 编辑 Excel 配置文件：BuildDataConfig/DataConfig/XXX.xlsx
2. 运行配置生成工具：Tools/ConfigGenerate.bat
3. 配置类自动生成到：Packages/soul.proto.config/DataConfig/DataProto/
4. 使用 BaseDataConfigManager.Instance 获取配置
```

### 代码示例

```csharp
// 获取配置值
BaseDataConfigManager.Instance.TryGetCommonKeyValueConfigDictItem(key, out var value);

// 获取其他类型配置
var buffConfig = BaseDataConfigManager.Instance.GetBuffConfig(buffId);
```

### 注意事项

- ✅ 修改 Excel 后必须运行配置生成工具
- ✅ 配置类会自动生成，不要手动修改
- ⚠️ 配置文件包含元数据，可追踪配置来源
- ⚠️ 客户端不应读取关键配置，优先从协议获取

---

## 2. 修改相机行为

### 流程步骤

```
1. 定位相机类型：Assets/Scripts/Soul/Camera/
2. 修改 SoulCameraManager 或对应的相机组件
3. ⚠️ 考虑相机优先级和栈管理
4. ⚠️ 确保 Cinemachine 集成正确
5. 测试遮挡半透明效果
```

### 代码示例

```csharp
// 切换相机
SoulCameraManager.Instance.SwitchCamera(CameraType.Battle);

// 相机震动
SoulCameraManager.Instance.Shake(intensity, duration);

// 相机栈管理
SoulCameraManager.Instance.PushCamera(camera, priority);
SoulCameraManager.Instance.PopCamera();
```

### 注意事项

- ❌ 禁止直接操作 `Camera.main`
- ✅ 必须通过 `SoulCameraManager` 操作
- ⚠️ 修改时考虑相机优先级和栈管理
- ⚠️ 确保与 Cinemachine 的集成正确
- ⚠️ 涉及渲染的修改要考虑 SOC 剔除系统

---

## 3. 添加 AI 行为

### 流程步骤

```
1. 打开 AI 行为树编辑器：Assets/Scripts/Editor/AI/BehaviorTree/
2. 创建新的行为节点或修改现有节点
3. 使用 Blackboard 共享数据
4. 保存并测试序列化
```

### 代码示例

```csharp
// Blackboard 共享数据
blackboard.SetValue("TargetEnemy", enemy);
var target = blackboard.GetValue<GameObject>("TargetEnemy");

// 自定义行为节点
public class MyCustomNode : BehaviorNode
{
    public override NodeState Evaluate()
    {
        // 行为逻辑
        return NodeState.Success;
    }
}
```

### 注意事项

- ✅ 使用可视化编辑器设计行为树
- ✅ 通过 Blackboard 共享数据
- ⚠️ 确保节点序列化正确
- ⚠️ 测试多窗口编辑支持

---

## 4. 修改战斗逻辑

### 流程步骤

```
1. 定位战斗逻辑：Assets/Scripts/Soul/Battle/
2. 修改逻辑代码
3. ⚠️ 必须测试战斗回放兼容性
4. ⚠️ 考虑网络同步影响
5. 更新相关配置表
```

### 代码示例

```csharp
// 战斗逻辑修改示例
public class BattleLogic
{
    [ServerOnly]
    public void ApplyDamage(int targetId, int damage)
    {
        // 1. 服务器权威：在服务器端验证
        if (!IsValidTarget(targetId))
        {
            return;
        }
        
        // 2. 执行逻辑
        var target = GetTarget(targetId);
        target.TakeDamage(damage);
        
        // 3. 同步到客户端
        RpcUpdateHealth(targetId, target.Health);
        
        // 4. 记录回放数据
        RecordBattleEvent(new DamageEvent(targetId, damage));
    }
}
```

### 注意事项

- ⚠️ **必须测试战斗回放兼容性**（最重要！）
- ✅ 确保逻辑确定性执行
- ✅ 避免随机数和时间相关的非确定性操作
- ⚠️ 考虑网络同步影响
- ⚠️ 更新相关配置表

---

## 5. 添加网络消息

### 流程步骤

```
1. 定义 .proto 文件
2. 生成代码：Tools/ProtoGenerate.bat
3. 注册消息处理：NetworkManager.Register<S2C_NewMessage>(OnNewMessage)
4. ⚠️ 所有 RPC 必须校验参数
5. 测试网络同步
```

### 代码示例

**定义 Proto 文件**

```protobuf
// Messages.proto
message C2S_UseItem
{
    int32 itemId = 1;
    int32 targetId = 2;
}

message S2C_ItemUsed
{
    int32 itemId = 1;
    int32 result = 2;
}
```

**实现 RPC**

```csharp
// 服务器 RPC（客户端 -> 服务器）
[ServerRPC(RPCMask.WithValidation)]
public void CmdUseItem(int itemId, int targetId)
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
    UseItem(itemId, targetId);
    
    // 4. 通知客户端
    RpcItemUsed(itemId, 0);
}

// 客户端 RPC（服务器 -> 客户端）
[ClientRPC]
public void RpcItemUsed(int itemId, int result)
{
    // 更新客户端表现
    ShowItemUseEffect(itemId);
}
```

**注册消息处理**

```csharp
// 注册协议消息
NetworkManager.Register<S2C_ItemUsed>(OnItemUsed);

private void OnItemUsed(S2C_ItemUsed msg)
{
    // 处理消息
    Debuger.LogInfo(EDebugTag.Network, $"Item {msg.itemId} used, result: {msg.result}");
}
```

### 注意事项

- ✅ 修改 .proto 后必须运行生成工具
- ⚠️ **所有 RPC 必须添加 `RPCMask.WithValidation`**
- ⚠️ **所有 RPC 必须校验参数合法性**
- ✅ 服务器权威架构，关键逻辑在服务器端执行
- ⚠️ GM 命令除外，仅需基础实现

---

## 6. 添加 UI 界面

### 流程步骤

```
1. 创建 UI Prefab：遵循命名规范（功能_组件名缩写）
2. 继承 UIWindow 实现 UIPanel
3. 实现生命周期方法（OnStart/OnStop, OnShow/OnHide）
4. 注册 UI 到 UIManager
5. 测试 UI 生命周期
```

### 代码示例

**UI Panel 实现**

```csharp
using Soul.UI;

public class BattleResultPanel : UIWindow
{
    // UI 节点引用（遵循命名规范）
    private Button m_closeBtn;
    private Text m_titleTxt;
    private Image m_bgImg;
    
    public override void OnStart()
    {
        // 初始化资源
        m_closeBtn = transform.Find("Close_Btn").GetComponent<Button>();
        m_titleTxt = transform.Find("Title_Txt").GetComponent<Text>();
        m_bgImg = transform.Find("Bg_Img").GetComponent<Image>();
        
        // 注册事件
        m_closeBtn.onClick.AddListener(OnCloseClicked);
    }
    
    public override void OnStop()
    {
        // 清理资源（必须与 OnStart 配对）
        m_closeBtn.onClick.RemoveListener(OnCloseClicked);
    }
    
    public override void OnShow()
    {
        // 显示逻辑
        RefreshUI();
        PlayShowAnimation();
    }
    
    public override void OnHide()
    {
        // 隐藏逻辑（必须与 OnShow 配对）
        StopAnimations();
    }
    
    private void RefreshUI()
    {
        // 刷新 UI 数据
    }
    
    private void OnCloseClicked()
    {
        UIManager.Instance.ClosePanel<BattleResultPanel>();
    }
}
```

**UI 命名规范**

```
功能_组件名缩写

常用组件缩写：
- Img   - Image
- Btn   - Button
- Txt   - Text
- Grid  - Grid Layout Group
- Tog   - Toggle
- Icon  - Icon Image
- Drop  - Dropdown
- Input - Input Field
- ScrBar - Scrollbar

示例：
- Match_Btn      - 匹配按钮
- PlayerName_Txt - 玩家名称文本
- Check_Tog      - 选中开关
- Avatar_Icon    - 头像图标
```

### 注意事项

- ✅ UI 节点命名遵循规范（功能_组件缩写）
- ✅ 生命周期方法必须配对（OnStart/OnStop, OnShow/OnHide）
- ⚠️ 事件订阅和取消订阅必须配对
- ⚠️ 注意内存泄漏（纹理、Sprite 等）

---

## 7. 添加对象池

### 流程步骤

```
1. 确定需要池化的对象类型
2. 使对象实现池化接口（Poolable/ThreadSafePoolable）
3. 使用 InstancePool 或 ThreadSafePoolHelper
4. 确保对象复用前被正确重置
```

### 代码示例

**定义池化对象**

```csharp
// 单线程对象池
public class Bullet : Poolable
{
    private Vector3 m_velocity;
    private float m_lifetime;
    
    public override void OnReturnToPool()
    {
        // 清理逻辑
        m_velocity = Vector3.zero;
        m_lifetime = 0;
        gameObject.SetActive(false);
    }
    
    public override void OnAwakenFromPool()
    {
        // 初始化逻辑
        gameObject.SetActive(true);
    }
}

// 多线程对象池
public class NetworkMessage : ThreadSafePoolable
{
    private byte[] m_data;
    
    public override void OnReturnToPool()
    {
        // 清理逻辑
        m_data = null;
    }
}
```

**使用对象池**

```csharp
// 方式1：InstancePool（Unity 对象）
public class BulletSpawner
{
    private void SpawnBullet()
    {
        // 从池中获取
        var bullet = InstancePool.Get<Bullet>(bulletPrefab);
        bullet.Initialize(position, direction);
        
        // 使用完毕后归还
        // 通常在子弹销毁时调用
        // InstancePool.Release(bullet);
    }
}

// 方式2：ThreadSafePoolHelper（纯 C# 对象）
public class NetworkHandler
{
    private void ProcessMessage()
    {
        // 从池中获取
        var msg = ThreadSafePoolHelper<NetworkMessage>.Alloc();
        msg.Init(data);
        
        // 使用
        SendMessage(msg);
        
        // 归还到池
        ThreadSafePoolHelper.Release(msg);
    }
}
```

### 注意事项

- ✅ 频繁创建销毁的对象应使用对象池
- ✅ 实现 `OnReturnToPool` 清理逻辑
- ✅ 实现 `OnAwakenFromPool` 初始化逻辑
- ⚠️ 确保对象归还后不再被使用
- ⚠️ 多线程场景使用 `ThreadSafePoolHelper`

---

## 8. 优化 GC 性能

### 流程步骤

```
1. 使用 Unity Profiler 分析 GC 分配
2. 识别热路径（Update/FixedUpdate）
3. 使用 RAII 工具类替代 new 操作
4. 使用对象池复用对象
5. 优化字符串拼接
```

### 代码示例

**RAII 模式优化**

```csharp
// ❌ 错误：每帧产生 GC
void Update()
{
    var list = new List<int>(); // 每帧分配
    ProcessData(list);
}

// ✅ 正确：使用 RAII 零 GC
void Update()
{
    using var raiiList = new RaiiUtilList<int>();
    var list = raiiList.Value;
    ProcessData(list);
    // 作用域结束自动归还到池
}
```

**字符串优化**

```csharp
// ❌ 错误：字符串拼接产生 GC
void LogPlayerInfo()
{
    string log = "";
    for (int i = 0; i < players.Count; i++)
    {
        log += "Player " + players[i].id + " score " + players[i].score;
    }
    Debuger.LogInfo(EDebugTag.Battle, log);
}

// ✅ 正确：使用 ZString 零 GC
void LogPlayerInfo()
{
    for (int i = 0; i < players.Count; i++)
    {
        var log = ZString.Format("Player {0} score {1}", players[i].id, players[i].score);
        Debuger.LogInfo(EDebugTag.Battle, log);
    }
}
```

**大数组池化**

```csharp
// ❌ 错误：频繁分配大数组
void ProcessData()
{
    byte[] buffer = new byte[1024 * 1024]; // 1MB
    ReadData(buffer);
}

// ✅ 正确：使用 ArrayPool
void ProcessData()
{
    byte[] buffer = ArrayPool<byte>.Shared.Rent(1024 * 1024);
    try
    {
        ReadData(buffer);
    }
    finally
    {
        ArrayPool<byte>.Shared.Return(buffer);
    }
}
```

### 性能优化工具

- **RaiiUtilList<T>**: 零 GC 的 List
- **RaiiUtilObject<T>**: 零 GC 的对象池
- **ZString.Format**: 零 GC 的字符串格式化
- **FastList<T>**: 高性能集合（O(1) 查找增删）
- **ArrayPool<T>**: 大数组池化
- **ThreadSafePoolHelper<T>**: 线程安全对象池

### 注意事项

- ⚠️ **RAII 对象必须使用 `using` 语句**
- ⚠️ **多线程场景（如 tlog）禁止使用 RAII**
- ✅ 热路径（Update/FixedUpdate）避免 GC 分配
- ✅ 使用 Unity Profiler 验证优化效果

---

## 9. 热更新代码

### 流程步骤

```
1. 编写热更新代码（放在指定目录）
2. 确保兼容 ILRuntime 限制
3. 测试热更新功能
4. 验证序列化兼容性
```

### ILRuntime 兼容性

**支持的特性**

```csharp
// ✅ 支持大部分 C# 语法
public class HotUpdateClass
{
    private int m_value;
    
    public void Method()
    {
        // 支持泛型
        var list = new List<int>();
        
        // ❌ 禁止使用 LINQ（项目规范）
        // var result = list.Where(x => x > 0).ToList();
        
        // ✅ 正确：使用循环替代
        var result = new List<int>();
        for (int i = 0; i < list.Count; i++)
        {
            if (list[i] > 0)
            {
                result.Add(list[i]);
            }
        }
        
        // 支持反射
        var type = typeof(HotUpdateClass);
    }
}
```

**不支持或有限制的特性**

```csharp
// ❌ 静态构造函数（需特殊处理）
static MyClass()
{
    // 可能不会被调用
}

// ❌ 某些 ref/out 参数用法（需适配器）
void Method(ref int value) { }

// ❌ 部分委托类型（需注册）
Action<int, string> callback = (a, b) => { };

// ❌ 跨域继承（需适配器）
public class MyClass : UnityEngine.MonoBehaviour { }
```

### 注意事项

- ⚠️ 避免使用不支持的特性
- ⚠️ 注意 ref/out 参数的兼容性
- ⚠️ 修改可序列化的类时保持版本兼容性
- ✅ 使用适配器处理跨域继承

---

## 10. 添加编辑器工具

### 流程步骤

```
1. 创建编辑器脚本（放在 Editor 目录）
2. 使用 Unity Editor API
3. 添加菜单项或自定义窗口
4. 测试编辑器功能
```

### 代码示例

**自定义菜单项**

```csharp
using UnityEditor;
using UnityEngine;

public class MyEditorTools
{
    [MenuItem("Soul/Tools/Clear Cache")]
    public static void ClearCache()
    {
        // 清理缓存逻辑
        PlayerPrefs.DeleteAll();
        EditorUtility.DisplayDialog("Success", "Cache cleared!", "OK");
    }
    
    [MenuItem("Soul/Tools/Build AssetBundles")]
    public static void BuildAssetBundles()
    {
        // AB 包构建逻辑
        BuildPipeline.BuildAssetBundles(
            "AssetBundles",
            BuildAssetBundleOptions.None,
            BuildTarget.StandaloneWindows64
        );
    }
}
```

**自定义编辑器窗口**

```csharp
using UnityEditor;
using UnityEngine;

public class MyEditorWindow : EditorWindow
{
    [MenuItem("Soul/Windows/My Tool")]
    public static void ShowWindow()
    {
        GetWindow<MyEditorWindow>("My Tool");
    }
    
    private void OnGUI()
    {
        GUILayout.Label("My Custom Tool", EditorStyles.boldLabel);
        
        if (GUILayout.Button("Execute"))
        {
            Execute();
        }
    }
    
    private void Execute()
    {
        // 工具逻辑
    }
}
```

### 注意事项

- ✅ 编辑器脚本必须放在 `Editor` 目录
- ✅ 使用 `EditorUtility` 提供用户反馈
- ⚠️ 编辑器代码不会打包到游戏中
- ⚠️ 注意跨平台兼容性

---

## 快速命令参考

```bash
# 生成协议代码
Tools/ProtoGenerate.bat

# 生成配置代码
Tools/ConfigGenerate.bat

# 清理缓存
rm -rf Library/

# 构建 AB 包
菜单 -> Build -> Build AssetBundles
```

---

## 常见问题排查

### 配置不生效
1. 检查是否运行了配置生成工具
2. 检查配置文件路径是否正确
3. 检查配置表格式是否正确

### 战斗回放异常
1. 检查战斗逻辑是否确定性执行
2. 检查是否使用了随机数或时间相关操作
3. 检查回放数据是否完整

### 网络同步问题
1. 检查 RPC 参数校验是否完整
2. 检查 SyncVar 同步模式是否正确
3. 检查网络消息是否正确注册

### 内存泄漏
1. 检查事件订阅是否配对取消
2. 检查资源加载是否配对卸载
3. 检查协程是否正确停止
4. 检查对象池对象是否正确归还

### 性能问题
1. 使用 Unity Profiler 分析热点
2. 检查是否在 Update 中产生 GC
3. 检查是否频繁查找对象或组件
4. 检查是否使用了对象池
