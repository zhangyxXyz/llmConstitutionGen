# 实施任务清单

## 1. 准备阶段

- [N/A] 1.1 为 `skills/token-savings/SKILL.md` 添加 `scope: generic` frontmatter 字段 - **实施时发现不需要 scope 字段**
- [N/A] 1.2 为 `skills/openspec-init/SKILL.md` 添加 `scope: generic` frontmatter 字段 - **实施时发现不需要 scope 字段**
- [x] 1.3 验证 frontmatter 格式正确 (YAML 合法性)

**注**: 实施过程中采用了更简化的方案，不使用 `scope` 字段区分skills，直接利用现有的 `claude` 任务分发机制。

## 2. 配置阶段

- [x] 2.1 配置 `claude` 任务支持自举分发 (添加 `workpath: "."`)
- [N/A] 2.2 单独的 self 任务 - **改为在 claude 任务中实现**
- [x] 2.3 验证 claude 任务已有 `skills/**/*.md` 分发规则

**实际实施**: 在 `claude` 任务中添加 `workpath: "."`,使其输出到项目根目录而不是 `./out`，从而实现自举分发。

## 3. 测试阶段

- [x] 3.1 运行 `python distribute_rules.py` 执行分发
- [x] 3.2 验证输出文件:
  - [x] 3.2.1 `.claude/skills/token-savings/SKILL.md` 存在且内容正确
  - [x] 3.2.2 `.claude/skills/openspec-init/SKILL.md` 存在且内容正确
  - [x] 3.2.3 `.claude/skills/project-info-generator/` 不存在 (该 skill 已在上一个变更中删除)
  - [x] 3.2.4 `.claude/settings.local.json` 包含 openspec-init 和 token-savings 的权限
- [x] 3.3 验证不影响其他 tasks 的分发 (cursor/codebuddy 任务正常输出到 ./out)

## 4. 文档阶段

- [~] 4.1 更新 `openspec/project.md` - **可选**
- [~] 4.2 更新 `README.md` - **可选**
- [N/A] 4.3 注释说明 - **不需要,实现足够简单明了**

## 5. 验证阶段

- [x] 5.1 验证自举分发成功 (`.claude/skills/` 存在两个 skills)
- [x] 5.2 验证 settings.local.json 包含正确权限
- [x] 5.3 验证功能完整性
- [x] 5.4 确认 AI 助手可以使用这些 skills (当前会话已可见)

## 实施总结

**最终方案**:
- 为 `claude` 任务添加 `"workpath": "."`
- 利用现有的第三个分发单元 (分发 `skills/**/*.md`)
- 无需 `scope` 字段，无需过滤器，无需独立的 `self` 任务

**代码修改**:
1. `rules_config.json`: 在 `claude` 任务中添加 `"workpath": "."`
2. `scripts/distributor.py`: 添加任务级别 `workpath` 支持
3. `scripts/filters.py`: 添加 frontmatter 值匹配支持 (为未来扩展保留)

**测试结果**: ✅ 所有验证通过
