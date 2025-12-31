# 变更:添加自举分发功能

## 为什么

本项目是一个 AI 助手规则分发系统,本身也需要 AI 助手辅助开发。当前配置仅将 skills 分发到外部项目,但未将通用 skills 分发到自身的 `.claude/skills/` 目录。

这导致:
- AI 助手在开发本项目时无法使用通用 skills (如 `token-savings`)
- 需要手动复制 skills 到 `.claude/skills/`
- 不符合"配置即真相"的理念

## 变更内容

在 `rules_config.json` 的 `tasks` 数组中添加新任务 `self`,用于将**通用 skills** 分发到本项目自身:

- 源路径: `skills/` 目录
- 目标路径: `.claude/skills/` (本项目)
- 分发范围: **仅通用 skills**,排除项目特定的 skills
- 过滤规则: 通过 frontmatter 的 `scope` 字段区分通用/项目特定

**通用 skills** (需要分发到自身):
- `token-savings` - token 省流原则,适用所有项目
- `openspec-init` - OpenSpec 环境初始化助手,适用所有使用 OpenSpec 的项目

**注**: `project-info-generator` 已在 `replace-project-skill-with-openspec-init` 变更中删除。当前所有 skills 均为通用 skills。

## 影响

- **受影响的规范**: 无 (当前无 specs)
- **受影响的代码**:
  - `rules_config.json` - 添加 `self` 任务配置
  - `skills/*/skill.md` - 可能需要添加 `scope` frontmatter 字段
- **受影响的输出**:
  - `.claude/skills/` - 新增通用 skills 目录
  - `.claude/settings.local.json` - 自动更新权限配置

**破坏性变更**: 无

## 设计决策

### 如何区分通用 vs 项目特定 skills?

**方案 A**: 使用 frontmatter `scope` 字段
```yaml
---
name: token-savings
scope: generic  # generic=通用, project-specific=项目特定
---
```

**方案 B**: 使用目录结构
```
skills/
├── generic/          # 通用 skills
│   ├── token-savings/
│   └── openspec-init/
└── project-specific/ # 项目特定 skills
    └── (空 - 无项目特定 skills)
```

**选择方案 A**,原因:
- ✅ 不需要重构现有目录结构
- ✅ frontmatter 已被广泛使用
- ✅ 可通过 `frontmatter_has` 过滤器实现
- ✅ 更灵活,支持未来扩展

### workpath 配置

**自举任务的 workpath**:
- 设置为 `.` (当前项目根目录)
- 或复用全局 `workpath`,但通过相对路径覆盖

**选择**: 在 `self` 任务中不设置 `workpath`,使用相对路径 `.claude/skills/` 相对于项目根目录。

## 实施计划

1. 为现有 skills 添加 `scope` frontmatter 字段
2. 在 `rules_config.json` 添加 `self` 任务配置
3. 配置过滤规则,仅分发 `scope: generic` 的 skills
4. 测试分发,验证输出
5. 更新文档说明自举分发功能
