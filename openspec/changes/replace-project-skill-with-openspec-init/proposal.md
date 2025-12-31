# 变更:用 OpenSpec 初始化 skill 替换项目特定 skill

## 为什么

当前 `skills/project-info-generator/` 是为特定的 D2C 工作流设计的,仅适用于特定类型的项目,不具有通用性。

作为一个 AI 助手规则分发系统,本项目应该提供**通用 skills**,帮助用户初始化和配置 OpenSpec 环境,而不是绑定到特定的业务场景。

**当前问题**:
- `project-info-generator` 只适用于 D2C 项目
- 依赖特定的目录结构和工具链
- 不能帮助用户在新项目中配置 OpenSpec
- 作为通用分发系统,不应包含业务特定逻辑

**机会**:
- 创建 `openspec-init` skill 帮助用户初始化 OpenSpec 环境
- 指导填充 `openspec/project.md` 的标准流程
- 适用于任何使用 OpenSpec 的项目
- 成为真正的通用 skill,可分发到所有项目

## 变更内容

1. **删除** `skills/project-info-generator/`
   - 删除整个目录及其内容
   - 从分发配置中移除相关引用

2. **创建** `skills/openspec-init/skill.md`
   - Frontmatter 标记 `scope: generic`
   - 指导用户初始化 OpenSpec 环境
   - 帮助填充 `openspec/project.md` 的各个章节
   - 提供最佳实践和模板

3. **更新** `rules_config.json`
   - 无需修改 (自动通过 scope 过滤)

## 影响

- **受影响的规范**: 无 (当前无 specs)
- **受影响的代码**:
  - `skills/` 目录结构
  - 任何引用 `project-info-generator` 的文档
- **受影响的分发**:
  - `project-info-generator` 不再分发到任何目标
  - `openspec-init` 作为通用 skill 分发到所有项目

**破坏性变更**:
- **是** - 删除 `project-info-generator` skill
- **影响范围**: 仅影响使用该 skill 的 D2C 项目
- **迁移路径**: D2C 项目可以自行维护该 skill

## 新 Skill 设计

### openspec-init skill 职责

**核心定位**: OpenSpec 环境配置助手

**主要功能**:
1. 验证 OpenSpec CLI 已安装
2. 指导运行 `openspec init` (如未初始化)
3. 帮助填充 `openspec/project.md` 的各个章节:
   - 项目目的和目标
   - 技术栈信息
   - 代码风格约定
   - 架构模式
   - 测试策略
   - Git 工作流
   - 领域上下文
   - 重要约束
   - 外部依赖

**执行流程**:
1. 检查 `openspec/` 目录是否存在
2. 如不存在,提示运行 `openspec init`
3. 读取现有 `openspec/project.md`
4. 逐章节询问并填充内容
5. 提供模板和最佳实践建议

**触发时机**:
- 用户明确请求初始化 OpenSpec
- 用户询问如何配置项目上下文
- 检测到 `openspec/project.md` 为空或模板状态

### Frontmatter 示例

```yaml
---
name: OpenSpec 初始化助手
description: 指导初始化 OpenSpec 环境并填充 project.md 的标准流程,适用于任何使用 OpenSpec 规范驱动开发的项目
scope: generic
permission: allow
allowed-tools: Bash, Read, Edit, Write
---
```

## 设计决策

### 为什么删除而不是重构?

**考虑的方案**:
- 方案 A: 重构 `project-info-generator` 变为通用 skill
- 方案 B: 保留 `project-info-generator`,新增 `openspec-init`
- 方案 C: 删除 `project-info-generator`,创建 `openspec-init`

**选择方案 C**,原因:
- ✅ 两者目标完全不同 (D2C vs OpenSpec 通用)
- ✅ 避免维护两个功能重叠的 skills
- ✅ 清晰的职责划分
- ✅ `project-info-generator` 可以独立维护在 D2C 项目中

### Skill 的粒度

**聚焦点**: OpenSpec 环境初始化和 project.md 填充

**不包含**:
- ❌ 创建变更提案 (已由 OpenSpec CLI 和 AGENTS.md 覆盖)
- ❌ 验证规范格式 (由 `openspec validate` 处理)
- ❌ 归档变更 (由 `openspec archive` 处理)

**包含**:
- ✅ 验证 OpenSpec 环境
- ✅ 指导填充 project.md
- ✅ 提供模板和最佳实践
- ✅ 询问式交互流程

## 实施计划

1. 创建 `skills/openspec-init/skill.md`
2. 编写 skill 内容和执行流程
3. 删除 `skills/project-info-generator/`
4. 更新相关文档引用
5. 测试分发到本项目和外部项目
