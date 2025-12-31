# rules_config.json 配置说明

> 供本项目的分发脚本 `distribute_rules.py` 使用，放置于 `configs/` 目录。

## 顶层字段
- `workpath`: 分发输出的工作目录（相对脚本所在目录），如 `"./out/"`。
- `cleanpath`: 分发前清理的路径列表（相对于 `workpath`），如 `[".cursor/rules", ".claude/skills"]`。
- `content_rules`: 内容处理规则，按路径模式组织。
- `tasks`: 任务列表（如 `cursor`、`claude`），定义源、分发、特化行为。

## content_rules
键是路径或通配符模式，值为对象：
- `filter`: 过滤规则数组，全部通过才应用对应的 process。
  - 示例：`frontmatter_has`（需包含 name/description）
- `process`: 处理规则数组，按顺序应用。
  - 常见 operation：
    - `replace`：正则替换（可带 flags）
    - `append_start`/`append_end`：追加内容
    - `rewrite_links_to_claude`：重写相对链接，需指定 `target_task`、`link_prefix`
- `scope`：可选，限定规则适用的 task（如 `["cursor"]`）。未设置则对所有 task 生效。

示例（节选）：
```json
"skills/**/*.md": {
  "filter": [
    {
      "operation": "frontmatter_has",
      "fields": ["name", "description"],
      "scope": ["cursor"]
    }
  ],
  "process": [
    {
      "operation": "replace",
      "pattern": "^---\\s*\\n[\\s\\S]*?\\n---\\s*\\n",
      "replacement": "",
      "scope": ["cursor"]
    },
    {
      "operation": "append_start",
      "content": "---\nalwaysApply: true\n---\n\n",
      "scope": ["cursor"]
    },
    {
      "operation": "rewrite_links_to_claude",
      "target_task": "claude",
      "link_prefix": "../..",
      "scope": ["cursor"]
    }
  ]
}
```

## tasks
每个 task 定义一组分发规则：
- `name`: 任务名（如 `cursor` / `claude`）
- `generate_settings`（可选，仅 claude 用）：生成 `.claude/settings.local.json`
  - `target`: 目标文件，默认 `.claude/settings.local.json`
  - `default_permission`: 未指定 permission 时的默认值（如 `"allow"`)
- `distribute`: 分发单元数组
  - `source`: 源定义
    - `{ "type": "file", "path": "..." }`
    - `{ "type": "directory", "path": "...", "pattern": "**/*.md" }`
  - `filter`: 分发级过滤（同 content_rules 的 filter）
  - `rename_rule`: 重命名规则
    - `apply_to`: `["file"]` / `["parent"]` / `["file","parent"]`
    - `foldername`: true 时用父目录名作为基础名（文件重命名场景）
    - `lowercase`: 是否转小写
    - `replacements`: 字符串替换列表 `{ "from": "soul-", "to": "" }`
  - 其他：
    - `copy`: 目标子目录（相对 `workpath`）
    - `use_parent_dir`: 是否保留父目录层级
    - `suffix`: 生成文件后缀（如 `mdc`）
    - `rename`: 简单重命名（优先级高于 rename_rule）

示例（节选）：
```json
{
  "name": "claude",
  "generate_settings": {
    "target": ".claude/settings.local.json",
    "default_permission": "allow"
  },
  "distribute": [
    {
      "source": { "type": "file", "path": "remoteLLMReviewRules/CODEBUDDY.md" },
      "rename": "CLAUDE.md",
      "copy": ""
    },
    {
      "source": { "type": "directory", "path": "remoteLLMReviewRules/.codebuddy/skills", "pattern": "**/*.md" },
      "rename_rule": {
        "apply_to": ["parent"],
        "lowercase": true,
        "replacements": [
          { "from": "soul-", "to": "" },
          { "from": "_", "to": "-" }
        ]
      },
      "copy": ".claude/skills",
      "use_parent_dir": true
    }
  ]
}
```

## 生成设置说明
对 `claude` 任务，会根据每个 skill 的 `permission`（frontmatter 中设置，缺省 default_permission）汇总生成/更新 `.claude/settings.local.json` 的 `permissions.allow/deny/ask` 列表。

## 运行

**使用默认配置**:
```bash
python run_distribute.py
# 或
python distribute_rules.py
```
默认使用 `configs/rules_config.json` 配置文件。

**使用指定配置**:
```bash
python run_distribute.py configs/self_bootstrap.json
# 或
python distribute_rules.py configs/self_bootstrap.json
```

**自举分发** (分发 skills 到本项目):
```bash
.\self_bootstrap.bat
# 或
python run_distribute.py configs/self_bootstrap.json
```

脚本会先清理 `cleanpath`，再按 tasks 依次分发并生成目标文件。

## 高级特性

### content_rules 中的 scope 和 flags

**scope 限定规则适用范围**:
- 在 `filter` 或 `process` 中添加 `"scope": ["cursor"]` 限定仅对 cursor 任务生效
- 未设置 `scope` 则对所有任务生效

**flags 支持正则表达式标志**:
```json
{
  "operation": "replace",
  "description": "替换跨行内容",
  "pattern": "## 项目职责.*?(?=\\n##|\\Z)",
  "replacement": "## 项目职责\n\n新内容...\n",
  "flags": ["DOTALL"],
  "scope": ["*"]
}
```

支持的 flags:
- `"DOTALL"` - 使 `.` 匹配包括换行符
- `"MULTILINE"` - 使 `^` 和 `$` 匹配每行开头/结尾
- `"IGNORECASE"` - 忽略大小写

**完整示例** (来自历史项目):
```json
"remoteLLMReviewRules/CODEBUDDY.md": {
  "filter": [],
  "process": [
    {
      "operation": "replace",
      "description": "开头明确本文档的用途",
      "pattern": "^# 项目代码审查指南\\s+## 项目概览",
      "replacement": "# 项目代码审查指南\n\n\n> 本文档为 AI 助手提供项目快速理解所需的关键信息\n\n\n## 项目概览",
      "flags": [],
      "scope": ["*"]
    },
    {
      "operation": "replace",
      "description": "替换项目职责部分，支持跨行匹配",
      "pattern": "## 项目职责.*?(?=\\n##|\\Z)",
      "replacement": "## 项目职责\n\n你是一个专业的游戏开发专家，你的主要职责是使用本文档和相关的skill/rule执行工作计划或者代码review。\n",
      "flags": ["DOTALL"],
      "scope": ["*"]
    },
    {
      "operation": "append_end",
      "description": "文档末尾追加特别声明",
      "content": "\n\n## 特别声明\n\n- 推理的过程和最终的结果需要使用简体中文。\n",
      "scope": ["*"]
    }
  ]
}
```

### 更多 content_rules 操作

**rewrite_links_to_claude** - 重写相对链接:
```json
{
  "operation": "rewrite_links_to_claude",
  "description": "将同目录相对链接指向 claude 任务的目标路径",
  "target_task": "claude",
  "link_prefix": "../..",
  "scope": ["cursor"]
}
```
用于将 skills 中的相对链接 (如 `[文档](../other/doc.md)`) 重写为指向 claude 任务输出路径的绝对链接。

### rename_rule 高级用法

**多层级重命名**:
```json
{
  "rename_rule": {
    "apply_to": ["parent"],
    "lowercase": true,
    "replacements": [
      { "from": "soul-", "to": "" },
      { "from": "_", "to": "-" }
    ]
  }
}
```
- `apply_to: ["parent"]` - 重命名父目录而非文件名
- `apply_to: ["file", "parent"]` - 同时重命名文件和目录
- `lowercase: true` - 转换为小写
- `replacements` - 按顺序执行字符串替换

**foldername 用法**:
```json
{
  "rename_rule": {
    "foldername": true,
    "lowercase": true,
    "replacements": [
      { "from": "_", "to": "-" }
    ]
  },
  "suffix": "mdc"
}
```
使用父目录名作为文件名基础，生成 `<dirname>.mdc` 文件。


