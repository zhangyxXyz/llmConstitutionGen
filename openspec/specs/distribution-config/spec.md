# distribution-config Specification

## Purpose
TBD - created by archiving change add-self-bootstrap-distribution. Update Purpose after archive.
## Requirements
### Requirement: 自举分发任务

系统 SHALL 支持将通用 skills 分发到本项目自身,以便 AI 助手在开发本项目时也能使用这些 skills。

#### Scenario: 分发通用 skill 到本项目

- **GIVEN** 项目中存在通用 skill (frontmatter 包含 `scope: generic`)
- **WHEN** 执行 `python distribute_rules.py`
- **THEN** 该 skill SHALL 被分发到 `.claude/skills/` 目录
- **AND** `.claude/settings.local.json` SHALL 包含该 skill 的权限配置

#### Scenario: 过滤项目特定 skill

- **GIVEN** 项目中存在项目特定 skill (frontmatter 包含 `scope: project-specific`)
- **WHEN** 执行自举分发任务
- **THEN** 该 skill SHALL NOT 被分发到本项目的 `.claude/skills/` 目录

#### Scenario: 保留 skill 目录结构

- **GIVEN** skill 位于 `skills/token-savings/skill.md`
- **WHEN** 分发到本项目
- **THEN** 输出路径 MUST 为 `.claude/skills/token-savings/skill.md` (保留父目录)

### Requirement: Skill Scope 标识

Skills SHALL 通过 frontmatter 的 `scope` 字段标识其适用范围。

#### Scenario: 通用 skill 的 scope 标识

- **GIVEN** skill 适用于所有项目
- **WHEN** 编写 skill 的 frontmatter
- **THEN** MUST 包含 `scope: generic` 字段

#### Scenario: 项目特定 skill 的 scope 标识

- **GIVEN** skill 仅适用于特定项目类型
- **WHEN** 编写 skill 的 frontmatter
- **THEN** MUST 包含 `scope: project-specific` 字段

#### Scenario: 缺少 scope 字段的默认行为

- **GIVEN** skill 的 frontmatter 未包含 `scope` 字段
- **WHEN** 系统读取 skill 配置
- **THEN** SHALL 视为项目特定 skill,不参与自举分发

### Requirement: 自举任务配置结构

`rules_config.json` SHALL 支持配置自举分发任务。

#### Scenario: 自举任务基本配置

- **GIVEN** 需要配置自举分发
- **WHEN** 在 `rules_config.json` 的 `tasks` 数组添加任务
- **THEN** 任务 MUST 包含以下字段:
  - `name: "self"` - 任务名称
  - `generate_settings` - Claude settings 生成配置
  - `distribute` - 分发规则数组

#### Scenario: 自举任务的过滤规则

- **GIVEN** 自举任务配置
- **WHEN** 定义 `distribute[].filter` 规则
- **THEN** MUST 使用 `frontmatter_has` 过滤器检查 `scope` 字段为 `generic`

#### Scenario: 自举任务的输出路径

- **GIVEN** 自举任务配置
- **WHEN** 定义 `distribute[].copy` 路径
- **THEN** MUST 设置为 `.claude/skills` (相对于项目根目录)

