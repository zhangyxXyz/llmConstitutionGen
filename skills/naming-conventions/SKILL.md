---
name: Soul 项目命名规范
description: 规定 C#/Unity 代码的文件、类型、成员等命名准则，统一风格并降低维护成本
allowed-tools: *
permission: allow
---

# Soul 项目命名规范

## 文件命名

- **C# 文件名**：与最重要的类名一致，使用 PascalCase
  - ✅ `BattleManager.cs`
  - ✅ `PlayerController.cs`
  - ❌ `battle_manager.cs`
  - ❌ `player-controller.cs`

## 类型命名

### 类（Class）

```csharp
/// <summary>
/// 类名使用大驼峰式（PascalCase）
/// </summary>
public class BattleManager : MonoBehaviour
{
    // ...
}

public class NetworkMessageHandler
{
    // ...
}
```

### 接口（Interface）

```csharp
/// <summary>
/// 接口名使用 I 前缀 + PascalCase
/// </summary>
public interface IPoolable
{
    void OnReturnToPool();
}

public interface IDamageable
{
    void TakeDamage(int damage);
}
```

### 枚举（Enum）

```csharp
/// <summary>
/// 枚举类名使用 PascalCase
/// 枚举值使用 PascalCase
/// </summary>
public enum BattleState
{
    Idle,
    Starting,
    InProgress,
    Ended
}

public enum WeaponType
{
    Melee,
    Ranged,
    Magic
}
```

### 结构体（Struct）

```csharp
/// <summary>
/// 结构体名使用 PascalCase
/// </summary>
public struct PlayerData
{
    public int playerId;
    public string playerName;
}
```

## 成员变量命名

### Private/Protected 成员变量

```csharp
public class MyComponent : MonoBehaviour
{
    /// <summary>
    /// private/protected 成员变量：m_ 开头 + camelCase
    /// </summary>
    private int m_health;
    private GameObject m_targetObject;
    private List<Enemy> m_enemyList;
    
    protected float m_moveSpeed;
    protected Transform m_cachedTransform;
}
```

### Private/Protected Static 成员变量

```csharp
public class GameConfig
{
    /// <summary>
    /// private/protected static 成员变量：s_ 开头 + camelCase
    /// </summary>
    private static int s_instanceCount;
    private static Dictionary<int, Player> s_playerCache;
    
    protected static bool s_isInitialized;
}
```

### Public 成员变量

```csharp
public class ActorData
{
    /// <summary>
    /// public 成员变量：camelCase（小驼峰式）
    /// </summary>
    public int actorId;
    public string actorName;
    public float moveSpeed;
}
```

### Public Static 成员变量

```csharp
public class GlobalSettings
{
    /// <summary>
    /// public static 成员变量：camelCase（小驼峰式）
    /// </summary>
    public static int maxPlayers;
    public static float gravity;
}
```

## 属性命名

### Public 属性

```csharp
public class Player
{
    private int m_health;
    private float m_moveSpeed;
    
    /// <summary>
    /// public 属性：PascalCase（大驼峰式）
    /// </summary>
    public int Health 
    { 
        get { return m_health; } 
        set { m_health = value; }
    }
    
    public float MoveSpeed => m_moveSpeed;
    
    public bool IsAlive { get; set; }
    
    public Transform CachedTransform { get; private set; }
}
```

## 常量命名

### 两种风格（都支持）

```csharp
public class Constants
{
    /// <summary>
    /// 风格1：PascalCase（大驼峰式）
    /// </summary>
    public const int MaxHealthValue = 100;
    public const float DefaultMoveSpeed = 5.0f;
    public const string DefaultPlayerName = "Player";
    
    /// <summary>
    /// 风格2：UPPER_SNAKE_CASE（全大写蛇形式）
    /// 推荐用于全局常量、配置常量
    /// </summary>
    public const int MAX_PLAYERS = 100;
    public const float GRAVITY_VALUE = -9.8f;
    public const string DEFAULT_SCENE_NAME = "MainScene";
}
```

**使用建议**：
- **全局常量/配置常量**：推荐 `UPPER_SNAKE_CASE`（如 `MAX_PLAYERS`）
- **类内部常量**：推荐 `PascalCase`（如 `MaxHealthValue`）
- 同一个类内保持一致风格

## 方法命名

```csharp
public class PlayerController
{
    /// <summary>
    /// 方法名：PascalCase（大驼峰式）
    /// 参数名：camelCase（小驼峰式）
    /// </summary>
    public void InitializeBattle(int playerId, string playerName)
    {
        // ...
    }
    
    private void UpdatePlayerState()
    {
        // ...
    }
    
    protected virtual void OnPlayerDeath()
    {
        // ...
    }
}
```

## 局部变量命名

```csharp
void ProcessData()
{
    /// <summary>
    /// 局部变量：camelCase（小驼峰式）
    /// </summary>
    int playerCount = 10;
    float deltaTime = Time.deltaTime;
    string playerName = "Player1";
    
    for (int i = 0; i < playerCount; i++)
    {
        var player = GetPlayer(i);
        ProcessPlayer(player);
    }
}
```

## 事件命名

```csharp
public class GameEvents
{
    /// <summary>
    /// 事件名：On + PascalCase
    /// </summary>
    public event Action OnGameStarted;
    public event Action<int> OnPlayerDied;
    public event Action<float, float> OnHealthChanged;
    
    public delegate void BattleEventHandler(BattleEventArgs args);
    public event BattleEventHandler OnBattleEvent;
}
```

## 宏定义命名

```csharp
/// <summary>
/// 宏定义：UPPER_SNAKE_CASE（全大写蛇形式）
/// </summary>
#if UNITY_EDITOR
    #define ENABLE_DEBUG_MODE
    #define USE_CUSTOM_RENDERER
#endif

#if ENABLE_PROFILING
    // 性能分析代码
#endif
```

## 命名空间

```csharp
/// <summary>
/// 命名空间：PascalCase，按层级组织
/// </summary>
namespace Soul.Battle.Royale
{
    public class BattleRoyaleManager
    {
        // ...
    }
}

namespace Soul.Camera
{
    public class SoulCameraManager
    {
        // ...
    }
}

namespace Com.Morefun.KHEngine.Logic
{
    public class LogicManager
    {
        // ...
    }
}
```

## 代码格式规范

### 大括号换行

```csharp
// ✅ 正确：大括号单独一行
public class MyClass
{
    public void MyMethod()
    {
        if (condition)
        {
            DoSomething();
        }
    }
}

// ❌ 错误：大括号不换行
public class MyClass {
    public void MyMethod() {
        if (condition) {
            DoSomething();
        }
    }
}
```

### 关键字和括号之间的空格

```csharp
// ✅ 正确：if, for, while 等关键字和开括号之间有空格
if (condition)
{
    // ...
}

for (int i = 0; i < count; i++)
{
    // ...
}

while (isRunning)
{
    // ...
}

switch (state)
{
    case 1:
        break;
}

// ❌ 错误：缺少空格
if(condition)
for(int i = 0; i < count; i++)
while(isRunning)
```

### 运算符空格

```csharp
// ✅ 正确：运算符前后有空格
int result = a + b;
bool isValid = (x > 0) && (y < 10);
float value = speed * deltaTime;

// ❌ 错误：缺少空格
int result=a+b;
bool isValid=(x>0)&&(y<10);
```

## Unity 特定命名

### MonoBehaviour 生命周期方法

```csharp
public class MyBehaviour : MonoBehaviour
{
    // Unity 生命周期方法保持原名
    private void Awake()
    {
        // ...
    }
    
    private void Start()
    {
        // ...
    }
    
    private void Update()
    {
        // ...
    }
    
    private void OnDestroy()
    {
        // ...
    }
}
```

### 序列化字段

```csharp
public class MyComponent : MonoBehaviour
{
    /// <summary>
    /// 序列化字段使用 m_ 前缀
    /// </summary>
    [SerializeField]
    private int m_maxHealth = 100;
    
    [SerializeField]
    private GameObject m_targetPrefab;
    
    [Header("Movement Settings")]
    [SerializeField]
    private float m_moveSpeed = 5.0f;
}
```

## 网络同步相关命名

### RPC 方法命名

```csharp
public class NetworkPlayer : NetworkBehaviour
{
    /// <summary>
    /// ServerRPC：使用 Cmd 或 RpcServer 前缀
    /// ClientRPC：使用 Rpc 或 RpcClient 前缀
    /// </summary>
    
    // 客户端 -> 服务器
    [ServerRPC(RPCMask.WithValidation)]
    public void CmdAttack(int targetId)
    {
        // ...
    }
    
    [ServerRPC]
    public void RpcServerUseItem(int itemId)
    {
        // ...
    }
    
    // 服务器 -> 客户端
    [ClientRPC]
    public void RpcTakeDamage(int damage)
    {
        // ...
    }
    
    [ClientRPC]
    public void RpcClientUpdateHealth(int newHealth)
    {
        // ...
    }
}
```

### SyncVar 命名

```csharp
public class SyncedData : NetworkBehaviour
{
    /// <summary>
    /// SyncVar 使用普通成员变量命名规则
    /// </summary>
    [SyncVar(syncMode = ESyncMode.ServerAll)]
    private int m_health;
    
    [SyncVar(syncMode = ESyncMode.ClientLocal)]
    public int displayScore;
}
```

## 完整示例

```csharp
// BattleManager.cs

using UnityEngine;
using System.Collections.Generic;

namespace Soul.Battle
{
    /// <summary>
    /// 战斗管理器 - 负责战斗流程控制
    /// </summary>
    public class BattleManager : MonoBehaviour
    {
        #region Constants
        
        /// <summary>
        /// 全局常量使用 UPPER_SNAKE_CASE
        /// </summary>
        public const int MAX_PLAYERS = 100;
        public const float BATTLE_DURATION = 300.0f;
        
        /// <summary>
        /// 类内常量使用 PascalCase
        /// </summary>
        private const int DefaultRespawnTime = 5;
        
        #endregion
        
        #region Static Fields
        
        /// <summary>
        /// 私有静态成员变量：s_ + camelCase
        /// </summary>
        private static BattleManager s_instance;
        private static int s_battleCount;
        
        /// <summary>
        /// 公共静态成员变量：camelCase
        /// </summary>
        public static int currentBattleId;
        
        #endregion
        
        #region Serialized Fields
        
        /// <summary>
        /// 序列化字段：m_ + camelCase
        /// </summary>
        [SerializeField]
        private GameObject m_playerPrefab;
        
        [SerializeField]
        private float m_respawnDelay = 3.0f;
        
        #endregion
        
        #region Private Fields
        
        /// <summary>
        /// 私有成员变量：m_ + camelCase
        /// </summary>
        private int m_currentPlayerCount;
        private List<Player> m_playerList;
        private Dictionary<int, Enemy> m_enemyDict;
        private Transform m_cachedTransform;
        
        #endregion
        
        #region Public Fields
        
        /// <summary>
        /// 公共成员变量：camelCase
        /// </summary>
        public int battleId;
        public float battleTime;
        
        #endregion
        
        #region Properties
        
        /// <summary>
        /// 公共属性：PascalCase
        /// </summary>
        public static BattleManager Instance => s_instance;
        
        public int CurrentPlayerCount 
        { 
            get { return m_currentPlayerCount; } 
            private set { m_currentPlayerCount = value; }
        }
        
        public bool IsBattleActive { get; set; }
        
        #endregion
        
        #region Events
        
        /// <summary>
        /// 事件：On + PascalCase
        /// </summary>
        public event System.Action OnBattleStarted;
        public event System.Action<int> OnPlayerJoined;
        public event System.Action OnBattleEnded;
        
        #endregion
        
        #region Unity Lifecycle
        
        private void Awake()
        {
            if (s_instance == null)
            {
                s_instance = this;
            }
            
            m_cachedTransform = transform;
            m_playerList = new List<Player>();
        }
        
        private void Start()
        {
            InitializeBattle();
        }
        
        private void Update()
        {
            if (IsBattleActive)
            {
                UpdateBattleState();
            }
        }
        
        private void OnDestroy()
        {
            CleanupBattle();
        }
        
        #endregion
        
        #region Public Methods
        
        /// <summary>
        /// 公共方法：PascalCase
        /// 参数：camelCase
        /// </summary>
        public void StartBattle(int playerId, string battleName)
        {
            // 局部变量：camelCase
            int maxPlayers = MAX_PLAYERS;
            float duration = BATTLE_DURATION;
            
            // if, for, while 关键字和括号之间有空格
            if (m_playerList.Count < maxPlayers)
            {
                for (int i = 0; i < m_playerList.Count; i++)
                {
                    var player = m_playerList[i];
                    player.Initialize();
                }
            }
            
            IsBattleActive = true;
            OnBattleStarted?.Invoke();
        }
        
        public void AddPlayer(Player player)
        {
            if (player != null)
            {
                m_playerList.Add(player);
                CurrentPlayerCount++;
                OnPlayerJoined?.Invoke(player.PlayerId);
            }
        }
        
        #endregion
        
        #region Private Methods
        
        /// <summary>
        /// 私有方法：PascalCase
        /// </summary>
        private void InitializeBattle()
        {
            s_battleCount++;
            battleId = s_battleCount;
            
            #if UNITY_EDITOR
            Debuger.LogInfo(EDebugTag.Battle, $"Battle {battleId} initialized");
            #endif
        }
        
        private void UpdateBattleState()
        {
            battleTime += Time.deltaTime;
            
            if (battleTime >= BATTLE_DURATION)
            {
                EndBattle();
            }
        }
        
        private void EndBattle()
        {
            IsBattleActive = false;
            OnBattleEnded?.Invoke();
        }
        
        private void CleanupBattle()
        {
            m_playerList?.Clear();
            m_enemyDict?.Clear();
        }
        
        #endregion
    }
    
    /// <summary>
    /// 枚举：PascalCase
    /// 枚举值：PascalCase
    /// </summary>
    public enum BattleState
    {
        Idle,
        Starting,
        InProgress,
        Ending,
        Ended
    }
}
```

## 命名规范检查清单

### 类型命名
- [ ] 类名使用 PascalCase
- [ ] 接口名使用 I + PascalCase
- [ ] 枚举类名和枚举值使用 PascalCase
- [ ] 文件名与主类名一致

### 成员变量命名
- [ ] private/protected 成员变量使用 m_ + camelCase
- [ ] private/protected static 成员变量使用 s_ + camelCase
- [ ] public 成员变量使用 camelCase
- [ ] public static 成员变量使用 camelCase

### 其他命名
- [ ] 公共属性使用 PascalCase
- [ ] 方法名使用 PascalCase
- [ ] 参数和局部变量使用 camelCase
- [ ] 常量使用 PascalCase 或 UPPER_SNAKE_CASE
- [ ] 事件使用 On + PascalCase
- [ ] 宏定义使用 UPPER_SNAKE_CASE

### 代码格式
- [ ] 大括号独占一行
- [ ] if/for/while 关键字和括号之间有空格
- [ ] 运算符前后有空格
- [ ] 代码缩进统一（4 空格或 1 Tab）

## 常见错误示例

```csharp
// ❌ 错误示例
public class battle_manager  // 类名应该用 PascalCase
{
    private int _health;  // 应该用 m_health
    public int Health;    // 公共属性应该用 Property 形式
    private static int m_count;  // 静态变量应该用 s_count
    
    public void update_state() { }  // 方法名应该用 PascalCase
    
    public event Action onDied;  // 事件应该用 OnDied
    
    private const int max_value = 100;  // 常量应该用 MaxValue 或 MAX_VALUE
}

// ✅ 正确示例
public class BattleManager
{
    private int m_health;
    public int Health { get; private set; }
    private static int s_count;
    
    public void UpdateState() { }
    
    public event Action OnDied;
    
    private const int MaxValue = 100;
    // 或
    private const int MAX_VALUE = 100;
}
```

---

**注意事项**：
1. 保持命名风格在整个项目中的一致性
2. 优先使用有意义的描述性名称，避免缩写（除非是广为人知的缩写如 HP、MP）
3. 遵循 C# 和 Unity 的命名约定
4. 代码审查时严格检查命名规范
