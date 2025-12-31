# 实施任务清单

## 1. 创建新 Skill

- [x] 1.1 创建 `skills/openspec-init/` 目录
- [x] 1.2 创建 `skills/openspec-init/skill.md` 文件
- [x] 1.3 编写 frontmatter
  - [x] 1.3.1 设置 `name: OpenSpec 初始化助手`
  - [x] 1.3.2 设置 `scope: generic`
  - [x] 1.3.3 设置 `permission: allow`
  - [x] 1.3.4 设置 `allowed-tools: Bash, Read, Edit, Write`
- [x] 1.4 编写 skill 核心内容
  - [x] 1.4.1 核心定位和职责说明
  - [x] 1.4.2 执行流程 (检查环境 → 初始化 → 填充 project.md)
  - [x] 1.4.3 各章节填充指导
    - [x] 目的
    - [x] 技术栈
    - [x] 项目约定 (代码风格、架构模式、测试策略、Git 工作流)
    - [x] 领域上下文
    - [x] 重要约束
    - [x] 外部依赖
  - [x] 1.4.4 最佳实践和模板示例
  - [x] 1.4.5 常见问题和注意事项

## 2. 删除旧 Skill

- [x] 2.1 删除 `skills/project-info-generator/` 目录及其所有内容
- [x] 2.2 验证目录已完全删除

## 3. 更新文档

- [x] 3.1 检查 `README.md` 是否引用 `project-info-generator`
  - [x] 3.1.1 如有引用,更新为 `openspec-init` (无引用,跳过)
- [x] 3.2 检查 `openspec/project.md` 是否引用 `project-info-generator`
  - [x] 3.2.1 如有引用,更新为 `openspec-init` (已更新)
- [x] 3.3 检查其他 Markdown 文件是否有相关引用
  - [x] 3.3.1 使用 `rg "project-info-generator"` 搜索
  - [x] 3.3.2 更新所有找到的引用 (仅 proposal/spec 文件,符合预期)

## 4. 测试分发

- [x] 4.1 运行 `python distribute_rules.py`
- [x] 4.2 验证输出:
  - [x] 4.2.1 `project-info-generator` 不再出现在任何输出目录
  - [~] 4.2.2 `.claude/skills/openspec-init/skill.md` 存在 (自举分发) - **需等待 add-self-bootstrap-distribution 变更实施**
  - [x] 4.2.3 外部项目的 `.claude/skills/openspec-init/` 存在
  - [x] 4.2.4 `.claude/settings.local.json` 包含 openspec-init 权限
- [~] 4.3 测试 skill 功能 - **跳过(需实际环境测试)**
  - [~] 4.3.1 在新项目中触发 skill
  - [~] 4.3.2 验证 OpenSpec 环境检查逻辑
  - [~] 4.3.3 验证 project.md 填充流程

## 5. Skill 内容质量检查

- [x] 5.1 验证 skill 符合 token-savings 原则 (简洁、不冗余)
- [x] 5.2 验证所有章节都有清晰的填充指导
- [x] 5.3 验证提供的模板和示例准确且实用
- [x] 5.4 验证 skill 适用于不同类型的项目 (Web、CLI、库等)

## 6. 最终验证

- [~] 6.1 在本项目中运行 skill,验证可以正确识别已初始化的 OpenSpec - **跳过(需实际环境测试)**
- [~] 6.2 在空项目中模拟运行,验证初始化指导清晰 - **跳过(需实际环境测试)**
- [x] 6.3 验证 skill 与其他通用 skills (如 token-savings) 无冲突
- [~] 6.4 验证分发到所有配置的目标 (cursor/claude/codebuddy/self) - **self 部分需等待 add-self-bootstrap-distribution 变更实施**

## 依赖关系

- 1.x 必须在 2.x 之前完成 (先创建新 skill)
- 2.x 必须在 4.x 之前完成 (先删除旧 skill 再测试)
- 3.x 可以与 1.x 和 2.x 并行
- 5.x 依赖 1.4 完成 (内容必须先写好)
- 6.x 必须在所有其他任务完成后执行

## 可并行执行

- 1.3 (frontmatter) 和 1.4 (内容) 可以部分并行
- 3.1、3.2、3.3 可以并行 (不同文件)
- 4.2.1、4.2.2、4.2.3、4.2.4 可以并行检查 (不同输出)
