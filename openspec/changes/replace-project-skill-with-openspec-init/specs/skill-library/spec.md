# Skill 库管理规范 - 增量

## REMOVED Requirements

### Requirement: D2C 项目信息生成器

**Reason**: 该 skill 专为 D2C 工作流设计,不具有通用性,不适合作为通用分发系统的默认 skill。

**Migration**: D2C 项目可以在自己的仓库中维护 `project-info-generator` skill。

## ADDED Requirements

### Requirement: OpenSpec 初始化助手

系统 SHALL 提供通用 skill 帮助用户初始化 OpenSpec 环境并填充 `openspec/project.md`。

#### Scenario: 验证 OpenSpec 环境

- **GIVEN** 用户请求初始化 OpenSpec
- **WHEN** skill 执行
- **THEN** MUST 检查 `openspec/` 目录是否存在
- **AND** 如目录不存在,MUST 提示用户运行 `openspec init`

#### Scenario: 填充 project.md 的目的章节

- **GIVEN** `openspec/project.md` 存在但目的章节为空或模板状态
- **WHEN** 用户请求填充项目上下文
- **THEN** skill SHALL 询问项目目的和核心目标
- **AND** SHALL 提供填充建议和示例

#### Scenario: 填充技术栈章节

- **GIVEN** 需要填充技术栈信息
- **WHEN** skill 执行
- **THEN** SHALL 询问主要编程语言、框架、数据库等
- **AND** SHALL 检测 `package.json`、`requirements.txt` 等配置文件并提供建议

#### Scenario: 填充项目约定章节

- **GIVEN** 需要填充项目约定
- **WHEN** skill 执行
- **THEN** SHALL 逐一指导填充:
  - 代码风格 (格式化工具、命名规范等)
  - 架构模式 (设计原则、模块划分等)
  - 测试策略 (测试框架、覆盖率要求等)
  - Git 工作流 (分支策略、提交规范等)

#### Scenario: 提供最佳实践建议

- **GIVEN** 用户填充任意章节
- **WHEN** skill 提供指导
- **THEN** MUST 包含最佳实践建议和常见模板
- **AND** SHALL 根据项目类型 (Web应用、CLI工具、库等) 调整建议

### Requirement: Skill Scope 标识一致性

所有通用 skills MUST 在 frontmatter 中声明 `scope: generic`。

#### Scenario: openspec-init skill 的 scope

- **GIVEN** `openspec-init` skill
- **WHEN** 查看其 frontmatter
- **THEN** MUST 包含 `scope: generic`
- **AND** SHALL 包含 `permission: allow`
- **AND** SHALL 列出所需工具 `allowed-tools`

#### Scenario: 已删除 skill 不应存在 scope

- **GIVEN** `project-info-generator` 已删除
- **WHEN** 扫描 `skills/` 目录
- **THEN** SHALL NOT 找到 `project-info-generator` 目录
- **AND** 分发系统 SHALL NOT 尝试分发该 skill

### Requirement: Skill 内容质量标准

通用 skills MUST 符合简洁、通用、可复用的原则。

#### Scenario: 遵循 token-savings 原则

- **GIVEN** 编写或更新通用 skill
- **WHEN** 审查 skill 内容
- **THEN** MUST 避免冗余说明和不必要的示例
- **AND** SHALL 提供关键指导而非详尽文档

#### Scenario: 适用性检查

- **GIVEN** skill 标记为 `scope: generic`
- **WHEN** 评估其适用范围
- **THEN** MUST 适用于多种项目类型
- **AND** SHALL NOT 依赖特定的业务逻辑或工具链

#### Scenario: 交互式引导

- **GIVEN** skill 需要用户输入信息
- **WHEN** skill 执行
- **THEN** SHALL 采用问答式交互,逐步收集信息
- **AND** SHALL 提供清晰的提示和示例
