# 实施任务清单

## 阶段 0: 配置文件简化 (预先完成)

- [x] 0.1 简化 `rules_config.json`
  - [x] 0.1.1 移除 `remoteLLMReviewRules` 相关的 content_rules
  - [x] 0.1.2 移除所有任务中的 `remoteLLMReviewRules` 分发单元
  - [x] 0.1.3 验证 JSON 格式正确性
  - [x] 0.1.4 测试分发功能正常

- [x] 0.2 文档化历史配置示例
  - [x] 0.2.1 在 README.md 添加"高级特性"章节
  - [x] 0.2.2 提取 scope 使用示例
  - [x] 0.2.3 提取 flags (DOTALL) 使用示例
  - [x] 0.2.4 提取 rewrite_links_to_claude 示例
  - [x] 0.2.5 提取 rename_rule 高级用法示例

## 阶段 1: 目录结构重构

- [x] 1.1 创建新目录结构
  - [x] 1.1.1 创建 `agent-resources/` 目录
  - [x] 1.1.2 创建 `configs/` 目录
  - [x] 1.1.3 移动 `skills/` → `agent-resources/skills/`
  - [x] 1.1.4 移动 `rules_config.json` → `configs/rules_config.json`

- [x] 1.2 更新配置文件中的路径引用
  - [x] 1.2.1 更新 `configs/rules_config.json` 中所有 `skills/` → `agent-resources/skills/`
  - [x] 1.2.2 验证 JSON 格式正确性
  - [x] 1.2.3 验证路径引用正确 (使用 `rg "\"skills/"` 检查遗漏)

## 阶段 2: 配置传递机制

- [x] 2.1 修改 `distribute_rules.py` 支持命令行参数
  - [x] 2.1.1 添加 `sys.argv` 处理
  - [x] 2.1.2 设置默认值为 `configs/rules_config.json`
  - [x] 2.1.3 更新 `ConfigLoader` 调用,传递配置文件路径
  - [x] 2.1.4 添加帮助信息 (如何使用命令行参数)

- [x] 2.2 创建自举分发配置
  - [x] 2.2.1 创建 `configs/self_bootstrap.json`
  - [x] 2.2.2 设置 `workpath: "."`
  - [x] 2.2.3 设置 `cleanpath: [".claude/skills"]`
  - [x] 2.2.4 添加 `claude` 任务,仅分发 skills
  - [x] 2.2.5 添加 `generate_settings` 配置

- [x] 2.3 创建自举分发批处理脚本
  - [x] 2.3.1 创建 `self_bootstrap.bat`
  - [x] 2.3.2 调用 `python run_distribute.py configs/self_bootstrap.json`
  - [x] 2.3.3 添加友好的提示信息

- [x] 2.4 测试配置传递
  - [x] 2.4.1 测试默认配置: `python run_distribute.py`
  - [x] 2.4.2 测试显式配置: `python run_distribute.py configs/rules_config.json`
  - [x] 2.4.3 测试自举配置: `python run_distribute.py configs/self_bootstrap.json`
  - [x] 2.4.4 验证所有输出文件正确

## 阶段 3: 代码简化 - 移除任务级别 workpath

- [x] 3.1 删除 `distributor.py` 中的任务级别 workpath 支持
  - [x] 3.1.1 删除 lines 114-118 (设置 task_workpath)
  - [x] 3.1.2 删除 lines 196-198 (恢复 original_workpath)
  - [x] 3.1.3 删除相关变量定义

- [x] 3.2 更新主配置文件
  - [x] 3.2.1 删除 `configs/rules_config.json` 中 `claude` 任务的 `"workpath": "."`

- [x] 3.3 测试简化后的功能
  - [x] 3.3.1 运行主配置分发: `python run_distribute.py`
  - [x] 3.3.2 验证输出到 `./out` 正确
  - [x] 3.3.3 运行自举分发: `python run_distribute.py configs/self_bootstrap.json`
  - [x] 3.3.4 验证输出到 `./.claude/skills/` 正确

## 阶段 4: 批处理脚本修复

- [x] 4.1 修改 `update_all.bat`
  - [x] 4.1.1 移除 `chcp 65001 > nul` (line 2)
  - [x] 4.1.2 更新 Python 调用为 `python run_distribute.py` (使用包装器)
  - [x] 4.1.3 保持依赖默认值 `configs/rules_config.json`

- [x] 4.2 测试批处理脚本
  - [x] 4.2.1 测试分发功能正常
  - [x] 4.2.2 验证无 `nul` 文件生成 (移除 chcp 命令后)
  - [x] 4.2.3 验证分发输出正确

- [x] 4.3 清理错误文件
  - [x] 4.3.1 删除项目根目录的 `nul` 文件
  - [x] 4.3.2 将 `nul` 添加到 `.gitignore`

## 阶段 5: 文档更新

- [x] 5.1 更新 `README.md`
  - [x] 5.1.1 添加"高级特性"章节 (scope、flags、rewrite_links_to_claude 等)
  - [x] 5.1.2 从历史配置提取示例到文档
  - [x] 5.1.3 更新配置文件路径: `configs/rules_config.json`
  - [x] 5.1.4 说明如何传递配置文件参数
  - [x] 5.1.5 项目结构说明保留在 README (配置说明文档)
  - [x] 5.1.6 添加自举分发说明

- [x] 5.2 更新 `openspec/project.md`
  - [x] 5.2.1 更新"项目结构"章节,反映新目录布局
  - [x] 5.2.2 更新"常见工作流程"中的路径引用
  - [x] 5.2.3 更新"外部依赖"中的配置路径说明
  - [x] 5.2.4 添加"自举分发"工作流说明

- [x] 5.3 检查其他文档
  - [x] 5.3.1 openspec/AGENTS.md 无需更新 (无路径引用)
  - [x] 5.3.2 其他 OpenSpec 变更文档中的引用属于历史记录
  - [x] 5.3.3 所有主要文档已更新

## 阶段 6: 验证和清理

- [x] 6.1 综合功能测试
  - [x] 6.1.1 运行主配置分发: `python run_distribute.py`
  - [x] 6.1.2 验证 `out/.cursor/rules/` 输出正确 (2个文件)
  - [x] 6.1.3 验证 `out/.claude/skills/` 输出正确 (2个目录)
  - [x] 6.1.4 验证 `out/.codebuddy/skills/` 输出正确
  - [x] 6.1.5 验证 settings.local.json 文件正确

- [x] 6.2 自举分发测试
  - [x] 6.2.1 运行 `python run_distribute.py configs/self_bootstrap.json`
  - [x] 6.2.2 验证 `.claude/skills/openspec-init/` 存在且内容正确
  - [x] 6.2.3 验证 `.claude/skills/token-savings/` 存在且内容正确
  - [x] 6.2.4 验证 `.claude/settings.local.json` 包含正确权限

- [x] 6.3 批处理脚本测试
  - [x] 6.3.1 批处理脚本已更新,功能正常
  - [x] 6.3.2 确认无 `nul` 文件生成 (移除 chcp)
  - [x] 6.3.3 确认所有输出正确

- [x] 6.4 Git 状态检查
  - [x] 6.4.1 运行 `git status` 检查修改
  - [x] 6.4.2 确认修改符合预期
  - [x] 6.4.3 确认旧文件已通过 git rm 移除

- [x] 6.5 清理旧文件
  - [x] 6.5.1 `skills/` 目录已移动到 `agent-resources/skills/`
  - [x] 6.5.2 `rules_config.json` 已移动到 `configs/rules_config.json`
  - [x] 6.5.3 使用 `git rm -r skills/` 从版本控制中移除旧目录

## 依赖关系

- 1.x 必须首先完成 (目录结构基础)
- 2.x 依赖 1.x 完成 (配置文件已移动)
- 3.x 可以与 2.x 并行 (独立的代码修改)
- 4.x 依赖 1.2 和 2.1 完成 (批处理脚本需要知道新路径)
- 5.x 可以与其他阶段并行 (文档更新)
- 6.x 必须在所有其他阶段完成后执行 (综合验证)

## 可并行执行

- 1.2 (配置更新) 可与 2.1 (代码修改) 并行
- 3.1 (删除代码) 与 4.1 (修改脚本) 可并行
- 5.1、5.2、5.3 (不同文档) 可并行更新
- 6.1、6.2、6.3 (不同测试场景) 可并行验证

## 注意事项

1. **路径引用**: 所有 `skills/` → `agent-resources/skills/` 的替换必须完整,否则分发会失败
2. **配置文件格式**: JSON 修改后务必验证格式正确性
3. **自举分发**: `self_bootstrap.json` 的 `workpath` 必须是 `"."`,`cleanpath` 不能包含 `out/` 目录
4. **破坏性变更**: 此变更会修改目录结构,需要通知项目使用者
5. **Git 操作**: 使用 `git mv` 移动文件以保留历史记录
