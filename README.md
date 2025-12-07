# rules_config.json 配置说明

> 供本项目的分发脚本 `distribute_rules.py` 使用，放置于项目根目录。

## 顶层字段
- `workpath`: 分发输出的工作目录（相对脚本所在目录），如 `"../SoulClient/"`。
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
```bash
python distribute_rules.py
```
脚本会先清理 `cleanpath`，再按 tasks 依次分发并生成目标文件。


