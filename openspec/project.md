# 项目上下文

## 目的

本项目是一个 **AI 助手规则分发系统**,用于将统一维护的规则(rules/skills)自动分发到不同的 AI 编程助手工具。

**核心目标**:
- 在单一仓库中统一管理所有 AI 助手的规则和 skills
- 自动将规则转换并分发到不同平台 (Cursor、Claude Code、CodeBuddy 等)
- 根据目标平台自动调整内容格式、frontmatter 和链接
- 为 Claude Code 自动生成权限配置文件

## 技术栈

- **Python 3.x** - 主要编程语言,用于分发系统核心逻辑
- **JSON** - 配置文件格式 (`rules_config.json`)
- **Batch Script** - Windows 自动化脚本 (`update_all.bat`)
- **Markdown** - 规则和文档格式

**关键 Python 库**:
- `pathlib` - 路径处理
- `json` - 配置解析
- `re` - 正则表达式处理 (内容转换)

## 项目约定

### 代码风格

**Python 代码规范**:
- UTF-8 编码,文件头部添加编码声明 `# -*- coding: utf-8 -*-`
- 遵循 PEP 8 命名规范
- 函数和变量使用 `snake_case`
- 类名使用 `PascalCase`
- 使用类型提示 (例: `Path`, `dict`, `list`)
- 每个模块顶部添加 docstring 说明用途

**配置文件规范**:
- JSON 使用 4 空格缩进
- 所有路径使用正斜杠 `/` (即使在 Windows 上)
- 正则表达式中的反斜杠需要双重转义 `\\`
- 添加 `description` 字段说明复杂规则的用途

**Markdown 规范**:
- Skill 文件必须包含 YAML frontmatter (至少包含 `name` 和 `description`)
- 使用相对链接引用同项目的其他文件
- 中文内容统一使用简体中文
- 代码块明确指定语言类型

### 架构模式

**配置驱动架构**:
- 系统通过 `rules_config.json` 配置文件驱动所有行为
- 配置分为四个核心部分:
  - `workpath`: 分发输出目标目录
  - `cleanpath`: 分发前清理路径列表
  - `content_rules`: 内容转换规则 (按路径模式匹配)
  - `tasks`: 分发任务定义

**模块化设计**:
```
distribute_rules.py (入口)
    ↓
scripts/
├── config_loader.py      # 配置加载
├── distributor.py        # 主控制器
├── paths.py              # 路径映射和文件收集
├── filters.py            # 过滤器逻辑
├── content_rules.py      # 内容转换
├── rename_rules.py       # 重命名规则
├── link_resolver.py      # 链接重写
└── settings_gen.py       # Claude settings 生成
```

**处理流水线**:
```
源文件 → 路径映射 → 过滤器 → 内容规则处理 → 分发规则处理 → 重命名 → 输出文件
```

**关注点分离**:
- 配置解析与业务逻辑分离
- 每个模块单一职责
- 通过回调函数注入依赖 (如 `settings_resolver`)

### 测试策略

**手动测试流程**:
1. 修改代码后运行 `python distribute_rules.py`
2. 检查控制台输出,确认文件收集、过滤、处理步骤正常
3. 验证所有目标平台的输出文件:
   - Cursor: `out/.cursor/rules/*.mdc`
   - Claude: `out/.claude/skills/**/skill.md`
   - Claude settings: `out/.claude/settings.local.json`

**关键检查点**:
- [ ] 文件数量是否符合预期
- [ ] frontmatter 是否正确转换
- [ ] 链接重写是否正确
- [ ] 文件重命名是否符合规则
- [ ] Claude settings.local.json 权限配置正确

**调试技巧**:
- 查看"📁 分发单元 X: Y 个文件"消息确认文件收集
- 查看"⏭️ 过滤未通过"消息定位过滤问题
- 在 `distributor.py` 的 `run()` 中添加 `print(self.path_mappings)` 查看路径映射
- 使用 `--json` 输出调试规则解析

### Git 工作流

**分支策略**:
- `master` - 主分支,稳定版本
- 功能开发直接在 master 或创建短期分支

**提交规范**:
- 提交消息使用简体中文
- 格式: `<类型>: <描述>`
  - 类型: `add`(新功能)、`fix`(修复)、`update`(更新)、`refactor`(重构)
  - 示例: `add: 支持新的链接重写规则`、`fix: 修复 frontmatter 解析问题`

**提交前检查**:
1. 运行 `python distribute_rules.py` 确保分发成功
2. 检查输出文件无异常
3. 更新相关文档

**大变更流程**:
- 创建 OpenSpec 提案 (参见 `openspec/AGENTS.md`)
- 在 `openspec/changes/` 下创建变更目录
- 编写 `proposal.md`、`tasks.md`、规范增量
- 验证通过后实施

## 领域上下文

### AI 助手工具生态

本项目处理三种主流 AI 编程助手:

1. **Cursor**
   - 使用 `.cursor/rules/*.mdc` 存放规则
   - frontmatter 需要 `alwaysApply: true`
   - 不需要复杂的权限管理

2. **Claude Code**
   - 使用 `.claude/skills/*/skill.md` 存放 skills
   - 保留完整的 frontmatter (name、description、permission)
   - 需要 `.claude/settings.local.json` 配置权限
   - 支持目录层级结构

3. **CodeBuddy**
   - 类似 Claude Code 的结构
   - 使用 `.codebuddy/skills/` 目录

### 关键概念

**Content Rules (内容规则)**:
- 按路径模式匹配文件并应用转换
- 支持操作: `replace`、`append_start`、`append_end`、`rewrite_links_to_claude`
- 可通过 `scope` 字段限定适用的 task

**Tasks (分发任务)**:
- 定义如何将源文件分发到目标平台
- 每个 task 包含 `distribute` 数组,定义多个分发单元
- 可选的 `generate_settings` 用于生成 Claude settings

**Rename Rules (重命名规则)**:
- `apply_to`: 应用于文件名或父目录名
- `foldername`: 使用目录名作为文件名
- `lowercase`: 转换为小写
- `replacements`: 字符串替换列表

**Filters (过滤器)**:
- 在文件级别和分发级别执行过滤
- 常用: `frontmatter_has` (检查 frontmatter 字段)
- 支持 `negate` 反转过滤逻辑

### 项目结构

```
llmConstitutionGen/
├── distribute_rules.py          # 分发入口脚本
├── run_distribute.py            # UTF-8 编码包装器
├── update_all.bat                # Windows 一键执行脚本
├── self_bootstrap.bat            # 自举分发脚本
├── configs/                      # 配置文件目录
│   ├── rules_config.json         # 主配置文件 (分发到外部项目)
│   └── self_bootstrap.json       # 自举配置 (分发到本项目)
├── agent-resources/              # Agent 资源目录
│   └── skills/                   # Skills 资源库 (仅作为分发源)
│       ├── openspec-init/        # OpenSpec 初始化助手 (通用 skill)
│       └── token-savings/        # token 省流原则 (通用 skill)
├── scripts/                      # 核心处理模块
│   ├── config_loader.py          # 配置加载器
│   ├── distributor.py            # 分发主控制器 (217行)
│   ├── content_rules.py          # 内容规则处理
│   ├── filters.py                # 过滤器 (frontmatter 检测等)
│   ├── link_resolver.py          # 链接重写处理
│   ├── paths.py                  # 路径映射和文件收集
│   ├── rename_rules.py           # 文件/目录重命名规则
│   └── settings_gen.py           # Claude settings.local.json 生成器
├── openspec/                     # OpenSpec 规范驱动开发
│   ├── AGENTS.md                 # AI 助手开发指南
│   ├── project.md                # 本文件
│   ├── specs/                    # 当前规范 (已部署功能)
│   └── changes/                  # 变更提案 (待部署功能)
└── out/                          # 分发输出目录 (由 workpath 配置)
```

**特别说明**:
- `agent-resources/skills/` 目录中的文件**仅作为分发源资源**
- AI 助手应关注分发系统的代码逻辑,而非 skills 的具体业务内容
- `out/` 目录通过配置文件的 `workpath` 配置,实际可指向其他项目
- `configs/` 目录集中管理所有配置文件,支持多环境配置

## 重要约束

### 技术约束

1. **平台依赖**:
   - 需要 Python 3.x 运行环境
   - `update_all.bat` 仅支持 Windows 系统
   - 路径处理兼容 Windows 和 Unix

2. **配置约束**:
   - `rules_config.json` 必须是有效的 JSON 格式
   - 正则表达式模式需要符合 Python `re` 模块规范
   - 路径模式使用 glob 语法 (`**` 表示递归匹配)

3. **文件结构约束**:
   - Skill 文件必须是 Markdown 格式
   - frontmatter 必须是有效的 YAML 格式
   - 链接必须是相对路径才能被重写

### 业务约束

1. **单向分发**:
   - 分发是单向的,从源到目标
   - 目标文件的修改不会回流到源
   - 每次分发会清理目标目录 (由 `cleanpath` 控制)

2. **配置优先级**:
   - `rename` 规则优先于 `rename_rule`
   - 分发级别的 `process` 在内容规则之后执行
   - `scope` 为空表示适用于所有 task

3. **权限管理**:
   - Claude settings 仅在 `generate_settings` 存在时生成
   - `default_permission` 作为未指定 permission 的后备值
   - 支持三种权限: `allow`、`deny`、`ask`

## 外部依赖

### 文件系统依赖

- **源文件路径**: 由 `rules_config.json` 的 `tasks[].distribute[].source.path` 配置
  - 默认约定使用 `skills/` 目录,但可配置为任意路径
  - 支持相对路径和绝对路径
  - 可以从多个不同目录收集源文件
- **输出路径**: 由 `workpath` 配置,通常指向其他项目目录
- **临时文件**: 无,所有处理在内存中完成

### 配置依赖

- **rules_config.json**: 核心配置文件,必须存在于项目根目录
- **frontmatter**: Skill 文件的 YAML 前置元数据

### 运行时依赖

- **Python 标准库**: `pathlib`、`json`、`re`、`shutil`
- **无第三方依赖**: 项目不依赖任何 PyPI 包

---

## 常见工作流程

### 开发新 Skill

1. 在 `agent-resources/skills/` 创建新目录: `mkdir agent-resources/skills/my-new-skill`
2. 创建 `SKILL.md` 并添加 frontmatter:
   ```markdown
   ---
   name: My New Skill
   description: Description of what this skill does
   permission: allow
   ---

   Skill content here...
   ```
3. 运行分发: `python run_distribute.py` 或 `update_all.bat`
4. 检查输出并测试

### 自举分发 (Self-Bootstrap)

将通用 skills 分发到本项目,供开发本项目时使用:

1. 运行自举分发: `.\self_bootstrap.bat` 或 `python run_distribute.py configs/self_bootstrap.json`
2. Skills 将分发到 `.claude/skills/`
3. `.claude/settings.local.json` 自动更新权限配置

### 添加新的目标平台

1. 在 `rules_config.json` 的 `tasks` 数组添加新任务
2. 定义 `distribute` 规则 (source、copy、rename_rule 等)
3. 如需特定内容转换,在 `content_rules` 添加规则并设置 `scope`
4. 测试分发并验证输出

### 调试分发问题

1. **文件未被收集**: 检查 source `path` 和 `pattern` 是否正确
2. **过滤器阻止**: 查看控制台"⏭️ 过滤未通过"消息
3. **内容未转换**: 验证 `scope` 匹配、正则表达式语法、规则顺序
4. **链接重写失败**: 确认 `target_task` 存在、`link_prefix` 配置正确

---

**记住**: 本项目的核心是**配置驱动的文件分发系统**,重点关注分发逻辑、内容转换规则和路径映射机制。
