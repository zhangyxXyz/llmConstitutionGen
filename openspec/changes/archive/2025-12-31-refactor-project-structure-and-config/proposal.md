# 变更: 重构项目结构和配置传递机制

## 为什么

当前项目存在以下问题:

1. **目录结构分散**: `skills/` 目录直接位于项目根目录,未来可能还有其他 agent 资源(如 prompts、templates),导致项目根目录混乱

2. **配置文件硬编码**: `distribute_rules.py` 硬编码读取 `rules_config.json`,无法支持:
   - 使用不同配置文件进行分发
   - 创建自分发批处理 (self-bootstrap script)
   - 在不同环境中使用不同配置

3. **任务级别 workpath 不必要**: 当前代码支持任务级别的 `workpath` 覆盖,但实际使用场景中不需要这种复杂度:
   - `claude` 任务的 `workpath: "."` 用于自举分发,可以通过独立配置文件实现
   - 增加了代码复杂度和维护成本

4. **批处理脚本兼容性问题**: `update_all.bat` 中的 `chcp 65001 > nul` 会在 Git Bash 环境下生成错误文件 `nul`,内容为 `/usr/bin/bash: line 1: chcp: command not found`

## 变更内容

### 1. 目录结构重构

将所有 agent 相关资源整合到 `agent-resources/` 目录:

```
llmConstitutionGen/
├── agent-resources/           # 新增: agent 资源目录
│   └── skills/                # 移动: 从根目录移入
│       ├── openspec-init/
│       └── token-savings/
├── configs/                   # 新增: 配置文件目录
│   ├── rules_config.json      # 移动: 主配置文件
│   └── self_bootstrap.json    # 新增: 自举分发配置
├── scripts/                   # 保持不变
├── openspec/                  # 保持不变
├── distribute_rules.py        # 修改: 支持命令行参数
└── update_all.bat             # 修改: 移除 chcp 命令
```

**设计决策**: 使用 `agent-resources/` 而非 `agents/` 或 `resources/`:
- 明确表示这些是"供 AI 助手使用的资源"
- 避免与 OpenSpec 的 `AGENTS.md` 概念混淆
- 可扩展性强,未来可添加 `agent-resources/prompts/`、`agent-resources/templates/` 等

### 2. 配置文件参数化

**修改 `distribute_rules.py`**:
- 支持命令行参数传递配置文件路径
- 默认值为 `configs/rules_config.json`
- 示例: `python distribute_rules.py configs/self_bootstrap.json`

**新增 `configs/self_bootstrap.json`**:
- 专门用于项目自举分发的配置
- `workpath: "."`
- 仅包含 `claude` 任务,分发 skills 到本项目的 `.claude/skills/`

### 3. 简化代码 - 移除任务级别 workpath

**删除功能**:
- `distributor.py` 中任务级别 `workpath` 支持代码 (lines 114-118, 196-198)
- `rules_config.json` 的 `claude` 任务中的 `"workpath": "."` 字段

**替代方案**:
- 使用独立的 `configs/self_bootstrap.json` 配置文件
- 通过 `python distribute_rules.py configs/self_bootstrap.json` 执行自举分发

**优势**:
- 代码更简单,更易维护
- 配置更清晰,职责分离 (主配置 vs 自举配置)
- 符合"配置即真相"理念

### 4. 修复批处理脚本兼容性

**修改 `update_all.bat`**:
- 移除 `chcp 65001 > nul` 命令
- 直接调用 Python 脚本 (Python 已通过 `run_distribute.py` 处理编码)

## 影响

### 受影响的规范
- 无 (当前无 specs)

### 受影响的代码
- `distribute_rules.py` - 添加命令行参数支持
- `scripts/distributor.py` - 删除任务级别 workpath 支持代码
- `rules_config.json` - 移动到 `configs/` 并删除 `claude` 任务的 `workpath` 字段
- `update_all.bat` - 移除 `chcp` 命令
- 所有引用 `skills/` 或 `rules_config.json` 路径的文件

### 受影响的文档
- `README.md` - 更新配置说明 (移除项目结构部分)
- `openspec/project.md` - 更新项目结构和工作流程说明
- `openspec/AGENTS.md` - 如有路径引用需更新

### 破坏性变更
- ✅ **破坏性变更**: 目录结构和配置文件路径变化
- **迁移方案**:
  1. 运行分发后,`skills/` 资源已在 `agent-resources/skills/`
  2. 配置文件已在 `configs/rules_config.json`
  3. 原有调用 `python distribute_rules.py` 的脚本需更新为 `python distribute_rules.py configs/rules_config.json` 或依赖默认值

## 设计决策

### Q1: 为什么创建 `configs/` 目录?

**方案 A**: 保持 `rules_config.json` 在根目录
**方案 B**: 创建 `configs/` 目录集中管理配置文件

**选择方案 B**,原因:
- ✅ 未来可能有多个配置文件 (生产环境、测试环境等)
- ✅ 配置文件集中管理,更清晰
- ✅ 与 `scripts/`、`openspec/` 等目录层级一致

### Q2: 是否完全移除任务级别 workpath?

**方案 A**: 保留任务级别 workpath 支持
**方案 B**: 完全移除,通过独立配置文件实现

**选择方案 B**,原因:
- ✅ 用户明确表示"真的不需要任务级别的分发规则"
- ✅ 代码更简单
- ✅ 职责分离: 主配置用于分发到外部项目,自举配置用于分发到本项目
- ✅ 更容易理解和维护

### Q3: 自举分发如何执行?

**方案 A**: 修改 `update_all.bat` 增加自举分发步骤
**方案 B**: 创建独立的 `self_bootstrap.bat`
**方案 C**: 在 README 说明,由用户手动执行

**选择方案 B**,原因:
- ✅ 职责分离: `update_all.bat` 用于分发到外部项目,`self_bootstrap.bat` 用于本项目自举
- ✅ 开发本项目时可独立执行自举分发
- ✅ 不增加主分发流程的复杂度

### Q4: 如何处理 `remoteLLMReviewRules/` 目录?

当前 `rules_config.json` 引用了 `remoteLLMReviewRules/CODEBUDDY.md` 和 `remoteLLMReviewRules/.codebuddy/skills`,但该目录不存在于项目中。

**用户反馈**: "这个是我之前的一个项目的遗留，留在这儿正好作为配置参考，因为有展示 scope 和 flags 的用法"

**已采取方案**:
- ✅ 将 `remoteLLMReviewRules` 相关配置示例提取到 `README.md` 的"高级特性"章节
- ✅ 从 `rules_config.json` 中移除这些配置单元,保持配置文件简洁
- ✅ README 中的示例展示了 `scope`、`flags: ["DOTALL"]`、`rewrite_links_to_claude` 等高级用法

**优势**:
- 配置文件更清爽,只包含当前项目实际使用的配置
- 高级特性有完整文档和示例供参考
- 用户可以根据需要将示例复制到配置文件中

## 实施计划

### 阶段 1: 目录结构重构
1. 创建 `agent-resources/` 和 `configs/` 目录
2. 移动 `skills/` 到 `agent-resources/skills/`
3. 移动 `rules_config.json` 到 `configs/rules_config.json`
4. 更新所有配置文件中的路径引用 (skills/ → agent-resources/skills/)

### 阶段 2: 配置传递机制
1. 修改 `distribute_rules.py` 支持命令行参数
2. 创建 `configs/self_bootstrap.json`
3. 创建 `self_bootstrap.bat` 批处理脚本
4. 测试主配置分发和自举分发

### 阶段 3: 代码简化
1. 删除 `distributor.py` 中任务级别 workpath 相关代码
2. 删除 `configs/rules_config.json` 中 `claude` 任务的 `workpath` 字段
3. 测试确保功能不受影响

### 阶段 4: 批处理脚本修复
1. 修改 `update_all.bat` 移除 `chcp 65001 > nul`
2. 更新配置文件路径引用
3. 测试 Windows 批处理执行
4. 删除项目根目录的 `nul` 文件

### 阶段 5: 文档更新
1. 更新 `README.md` - 仅保留配置说明,移除项目结构部分
2. 更新 `openspec/project.md` - 更新目录结构和工作流程
3. 检查并更新其他引用路径的文档

### 阶段 6: 验证和清理
1. 运行主配置分发: `python distribute_rules.py`
2. 运行自举分发: `python self_bootstrap.bat`
3. 验证所有输出文件正确
4. 删除旧目录和文件 (原 `skills/` 目录、根目录 `rules_config.json`)
