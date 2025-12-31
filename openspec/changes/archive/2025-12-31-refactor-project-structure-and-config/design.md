# 设计文档: 重构项目结构和配置传递机制

## 架构变更概述

本变更涉及项目的目录结构重组和配置加载机制改进,不涉及功能规范变更,因此不需要 spec deltas。

## 目录结构重构

### 当前结构 (Before)

```
llmConstitutionGen/
├── distribute_rules.py
├── rules_config.json          # 配置文件在根目录
├── skills/                    # agent 资源在根目录
│   ├── openspec-init/
│   └── token-savings/
├── scripts/
└── openspec/
```

### 新结构 (After)

```
llmConstitutionGen/
├── distribute_rules.py
├── configs/                   # 新增: 配置目录
│   ├── rules_config.json      # 移动: 主配置
│   └── self_bootstrap.json    # 新增: 自举配置
├── agent-resources/           # 新增: agent 资源目录
│   └── skills/                # 移动: skills
│       ├── openspec-init/
│       └── token-savings/
├── scripts/
└── openspec/
```

### 架构决策

**为什么创建 `agent-resources/` 目录?**

1. **关注点分离**: 明确区分"项目代码"和"agent 使用的资源"
2. **可扩展性**: 未来可添加其他类型的 agent 资源
   - `agent-resources/prompts/` - AI 提示词模板
   - `agent-resources/templates/` - 代码生成模板
   - `agent-resources/knowledge/` - 领域知识库
3. **避免命名冲突**: 避免与 `openspec/AGENTS.md` 等概念混淆

**为什么创建 `configs/` 目录?**

1. **配置集中管理**: 将所有配置文件放在一个目录
2. **多环境支持**: 支持不同配置文件用于不同用途:
   - `configs/rules_config.json` - 主配置 (分发到外部项目)
   - `configs/self_bootstrap.json` - 自举配置 (分发到本项目)
   - 未来可扩展: `configs/test.json`, `configs/production.json`
3. **清晰的职责**: 根目录只保留核心脚本和重要文档

## 配置传递机制

### 当前实现 (Before)

```python
# distribute_rules.py
def main():
    script_dir = Path(__file__).parent
    config_file = script_dir / "rules_config.json"  # 硬编码
    loader = ConfigLoader(config_file)
    # ...
```

**问题**:
- 配置文件路径硬编码
- 无法使用不同配置文件
- 自举分发需要修改代码或配置中的 task-level workpath

### 新实现 (After)

```python
# distribute_rules.py
import sys

def main():
    script_dir = Path(__file__).parent

    # 支持命令行参数传递配置文件
    if len(sys.argv) > 1:
        config_file = Path(sys.argv[1])
    else:
        config_file = script_dir / "configs" / "rules_config.json"

    loader = ConfigLoader(config_file)
    print(f"⚙️  已加载配置: {config_file}")
    # ...
```

**用法**:
```bash
# 使用默认配置 (分发到外部项目)
python distribute_rules.py

# 使用显式配置
python distribute_rules.py configs/rules_config.json

# 使用自举配置 (分发到本项目)
python distribute_rules.py configs/self_bootstrap.json
```

### 自举分发配置

**configs/self_bootstrap.json** 结构:

```json
{
    "workpath": ".",
    "cleanpath": [".claude/skills"],
    "tasks": [
        {
            "name": "claude",
            "generate_settings": {
                "target": ".claude/settings.local.json",
                "default_permission": "allow"
            },
            "distribute": [
                {
                    "source": {
                        "type": "directory",
                        "path": "agent-resources/skills",
                        "pattern": "**/*.md"
                    },
                    "copy": ".claude/skills",
                    "use_parent_dir": true
                }
            ]
        }
    ]
}
```

**关键特性**:
- `workpath: "."` - 输出到项目根目录
- `cleanpath` 仅清理 `.claude/skills` (不影响 `out/` 目录)
- 仅包含 `claude` 任务 (无需分发到 cursor、codebuddy)

## 代码简化 - 移除任务级别 workpath

### 当前实现 (Before)

`distributor.py` 支持任务级别 `workpath` 覆盖:

```python
# distributor.py lines 114-118
task_workpath = task.get("workpath")
if task_workpath:
    original_workpath = self.workpath
    self.workpath = Path(task_workpath)

# ... 分发逻辑 ...

# lines 196-198
if task_workpath:
    self.workpath = original_workpath
```

`configs/rules_config.json`:
```json
{
    "workpath": "./out",
    "tasks": [
        {
            "name": "claude",
            "workpath": ".",  // 覆盖全局 workpath
            // ...
        }
    ]
}
```

**问题**:
1. 增加了代码复杂度
2. 配置文件中任务职责不清晰 (既分发到外部又分发到自身)
3. 用户反馈"真的不需要任务级别的分发规则"

### 新实现 (After)

**删除代码**:
- 移除 `distributor.py` lines 114-118 和 196-198
- 移除 `configs/rules_config.json` 中的 `"workpath": "."`

**替代方案**:
- 使用独立的 `configs/self_bootstrap.json` 配置文件
- 通过命令行参数调用: `python distribute_rules.py configs/self_bootstrap.json`

**优势**:
1. **代码更简单**: `Distributor` 类不需要处理 workpath 覆盖逻辑
2. **职责分离**:
   - `configs/rules_config.json` - 负责分发到外部项目
   - `configs/self_bootstrap.json` - 负责本项目自举
3. **更容易理解**: 每个配置文件有明确的用途
4. **符合 KISS 原则**: 保持简单,避免过度设计

## 批处理脚本兼容性修复

### 问题根因

`update_all.bat` line 2:
```batch
chcp 65001 > nul
```

在 Git Bash 环境下执行时:
- Git Bash 将 `chcp` 视为 Bash 命令 (但不存在)
- 将 `> nul` 解释为重定向到文件 `nul` (而非 Windows 的 NUL 设备)
- 生成错误文件 `nul`,内容为错误信息

### 解决方案

**方案 A**: 检测环境,仅在 CMD 中执行 `chcp`
```batch
@echo off
if "%ComSpec%"=="%SYSTEMROOT%\system32\cmd.exe" (
    chcp 65001 > NUL
)
```

**方案 B**: 完全移除 `chcp` 命令,依赖 Python 的 UTF-8 处理

**选择方案 B**,原因:
1. ✅ 编码问题已在 `run_distribute.py` 中通过 Python 解决
2. ✅ 简化批处理脚本,减少环境依赖
3. ✅ 避免跨环境兼容性问题
4. ✅ 用户可以在 Git Bash、PowerShell、CMD 中执行

**修改后的 `update_all.bat`**:
```batch
@echo off
echo.
echo ============================================
echo   🚀 Soul LLM Rules - 一键分发工具
echo ============================================
echo.
python distribute_rules.py configs/rules_config.json
if %errorlevel% neq 0 (
    echo ❌ 规则分发失败
    exit /b 1
)
echo ✅ 所有操作完成！规则已更新！
pause
```

## 路径引用更新策略

### 受影响的路径

1. **配置文件中的源路径**:
   - `skills/` → `agent-resources/skills/`
   - 需更新: `configs/rules_config.json`、`configs/self_bootstrap.json`

2. **文档中的路径引用**:
   - `README.md` - 配置说明
   - `openspec/project.md` - 项目结构、工作流程
   - `openspec/AGENTS.md` - 可能的路径引用
   - 其他 OpenSpec 变更文档

### 更新流程

1. **搜索所有引用**: 使用 `rg "skills/" openspec` 和 `rg "rules_config.json"`
2. **逐个审查**: 确认每个引用是否需要更新
3. **保持一致性**: 确保所有路径使用新的目录结构

## 迁移影响分析

### 对现有用户的影响

1. **目录结构变化**: 用户需要了解新的目录布局
2. **配置文件位置变化**: 从根目录移到 `configs/`
3. **命令行调用可能变化**: 如果用户有脚本调用 `distribute_rules.py`,需要更新

### 迁移步骤

1. **拉取更新后**:
   - 旧的 `skills/` 和 `rules_config.json` 仍在版本控制中被移除
   - Git 会自动处理文件移动

2. **验证分发**:
   - 运行 `python distribute_rules.py` (使用新默认路径)
   - 或 `update_all.bat` (已更新配置路径)

3. **自举分发** (可选):
   - 运行 `python distribute_rules.py configs/self_bootstrap.json`
   - 或 `self_bootstrap.bat`

### 向后兼容性

**破坏性变更**:
- ✅ 目录结构变化
- ✅ 配置文件路径变化
- ✅ 需要更新引用这些路径的外部脚本

**无破坏性**:
- 分发输出格式不变
- 配置文件结构不变 (仅路径字段更新)
- 核心功能逻辑不变

## 测试策略

### 单元测试级别

**配置加载测试**:
- [ ] 测试默认配置路径加载
- [ ] 测试命令行参数配置路径加载
- [ ] 测试不存在的配置文件错误处理

**路径映射测试**:
- [ ] 验证 `agent-resources/skills/` 路径正确映射
- [ ] 验证 glob 模式匹配正确

### 集成测试级别

**主配置分发测试**:
- [ ] 运行 `python distribute_rules.py`
- [ ] 验证 `out/.cursor/rules/` 输出
- [ ] 验证 `out/.claude/skills/` 输出
- [ ] 验证 `out/.codebuddy/skills/` 输出

**自举配置分发测试**:
- [ ] 运行 `python distribute_rules.py configs/self_bootstrap.json`
- [ ] 验证 `.claude/skills/` 输出 (项目根目录)
- [ ] 验证 `.claude/settings.local.json` 生成

**批处理脚本测试**:
- [ ] 在 Windows CMD 中运行 `update_all.bat`
- [ ] 在 Git Bash 中运行 `update_all.bat`
- [ ] 验证无 `nul` 文件生成

### 回归测试

- [ ] 对比新旧输出文件内容一致性
- [ ] 验证所有现有功能不受影响
- [ ] 检查 settings.local.json 权限配置正确

## 风险评估

### 高风险项

1. **路径引用遗漏**:
   - **风险**: 配置文件中仍引用旧路径导致分发失败
   - **缓解**: 使用 `rg "skills/"` 全局搜索,逐个检查

2. **Git 文件移动历史丢失**:
   - **风险**: 使用 `rm` + `add` 而非 `git mv` 导致历史记录丢失
   - **缓解**: 使用 `git mv` 移动文件

### 中等风险项

1. **用户脚本失效**:
   - **风险**: 用户有外部脚本调用 `python distribute_rules.py`,无法找到新配置
   - **缓解**: 设置默认路径为 `configs/rules_config.json`,向后兼容性好

2. **文档更新不完整**:
   - **风险**: 部分文档仍引用旧路径
   - **缓解**: 搜索所有文档,建立更新清单

### 低风险项

1. **批处理脚本兼容性**:
   - **风险**: 移除 `chcp` 后某些环境编码问题
   - **缓解**: Python 已通过 `run_distribute.py` 处理编码,风险低

## 总结

本变更通过重构目录结构和改进配置传递机制:

1. **提升可维护性**: 配置和资源集中管理
2. **增强可扩展性**: 为未来的 agent 资源类型预留空间
3. **简化代码**: 移除不必要的任务级别 workpath 支持
4. **修复问题**: 解决批处理脚本跨环境兼容性问题

变更涉及目录结构调整,但核心功能逻辑保持不变,风险可控。
