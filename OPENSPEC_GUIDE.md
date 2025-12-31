# OpenSpec 使用指南

> 基于 [llmConstitutionGen](https://github.com/Fission-AI/llmConstitutionGen) 项目的实战经验总结

## 什么是 OpenSpec?

OpenSpec 是一个**规范驱动的 AI 协作开发框架**,让你和 AI 助手能够像专业团队一样协作:先规划、后执行、再归档。

- 📋 **GitHub**: https://github.com/Fission-AI/OpenSpec
- 📖 **知乎介绍**: https://zhuanlan.zhihu.com/p/1962579273299761060

## 核心理念

**不要让 AI 直接写代码,而是先让 AI 帮你做好设计**。

传统方式:
```
用户: "重构项目结构"
AI: 立即开始修改代码...
结果: 可能不符合预期,难以回滚
```

OpenSpec 方式:
```
用户: "重构项目结构"
AI: 创建变更提案 → 用户审阅 → 批准后执行 → 归档为规范
结果: 有计划、可追溯、形成文档
```

---

## 实战案例: llmConstitutionGen 项目

### 案例 1: 目录结构重构

**场景**: 项目文件散乱,想要规范化目录结构和配置管理。

#### 第 1 步: 创建提案

```bash
用户: "我想重构项目结构,将 skills 移到 agent-resources 目录,
      配置文件集中到 configs 目录"

AI: 使用 /openspec:proposal 创建提案
```

**生成的提案结构**:
```
openspec/changes/refactor-project-structure-and-config/
├── proposal.md      # 变更说明 (为什么改、改什么)
├── tasks.md         # 任务清单 (分 6 个阶段执行)
└── specs/           # 规范增量 (新增的规范定义)
    ├── config-loading/
    │   └── delta.md
    └── distribution-config/
        └── delta.md
```

#### 第 2 步: 多次迭代完善

**中途发现问题**:
```bash
用户: "tasks.md 中的 Phase 4 有问题,不应该移除 chcp 65001,
      这会导致中文显示乱码"

AI: 修改 tasks.md,调整实施计划
```

**新增需求**:
```bash
用户: "还需要创建 self_bootstrap.bat 来支持自举分发"

AI: 更新 tasks.md,添加新任务到 Phase 2
```

#### 第 3 步: 执行变更

```bash
用户: "帮我执行这个变更"

AI: 使用 /openspec:apply refactor-project-structure-and-config
    → 按 tasks.md 逐步执行
    → 实时更新任务状态
    → 遇到问题可随时调整
```

**执行过程中**:
- ✅ Phase 0: 配置简化 (已完成)
- ✅ Phase 1: 目录重构
- ✅ Phase 2: 配置传递机制
- ⚠️ Phase 3: 遇到 git mv 失败 → AI 自动切换方案
- ✅ Phase 4-6: 继续完成

#### 第 4 步: 归档为规范

```bash
用户: "/openspec:archive refactor-project-structure-and-config"

AI:
  1. 移动变更到 changes/archive/2025-12-31-refactor-*/
  2. 创建正式规范 openspec/specs/config-loading/spec.md
  3. 验证所有规范完整性
```

**成果**:
- ✅ 代码重构完成
- ✅ 形成正式规范文档
- ✅ 后续开发有章可循

---

### 案例 2: 同时管理多个变更

**场景**: 在项目中同时进行两个独立的功能开发。

```bash
# 查看所有变更
$ openspec list

Changes:
  refactor-project-structure-and-config     ✓ Complete
  add-self-bootstrap-distribution           ✓ Complete
  replace-project-skill-with-openspec-init  ⏸ In Progress
```

**工作流程**:
1. **并行提案**: 可以同时创建多个提案,互不影响
2. **独立执行**: 每个变更有自己的 tasks.md,按优先级执行
3. **分别归档**: 完成后分别归档,形成独立的规范

---

### 案例 3: 中途修正变更

**场景**: 执行过程中发现设计有误,需要调整。

```bash
用户: "等等,Phase 4 不应该删除 chcp 命令,需要保留"

AI:
  1. 暂停当前执行
  2. 修改 tasks.md 中的 Phase 4 说明
  3. 继续执行修正后的计划
```

**OpenSpec 的优势**:
- ✅ 任务清单随时可调整
- ✅ 不会因为 AI "记错"而出错
- ✅ 变更历史完整记录

---

## OpenSpec 工作流程图

```
┌─────────────────────────────────────────────────────────┐
│  1. 创建提案 (/openspec:proposal)                        │
│     - AI 分析需求,生成 proposal.md + tasks.md          │
│     - 用户审阅、讨论、修改                              │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  2. 执行变更 (/openspec:apply <id>)                     │
│     - AI 按 tasks.md 逐步执行                           │
│     - 实时更新任务状态                                  │
│     - 遇到问题可中途调整                                │
└──────────────────┬──────────────────────────────────────┘
                   │
                   ▼
┌─────────────────────────────────────────────────────────┐
│  3. 归档规范 (/openspec:archive <id>)                   │
│     - 移动到 changes/archive/                           │
│     - 创建/更新 specs/ 下的正式规范                     │
│     - 验证规范完整性                                    │
└─────────────────────────────────────────────────────────┘
```

---

## 核心命令速查

### 提案阶段

```bash
# AI 创建新提案
/openspec:proposal <change-id>

# 查看所有变更
openspec list

# 查看提案详情
openspec show <change-id>

# 验证提案
openspec validate <change-id>
```

### 执行阶段

```bash
# 执行变更
/openspec:apply <change-id>

# 查看执行进度
# 直接查看 changes/<change-id>/tasks.md
```

### 归档阶段

```bash
# 归档变更
/openspec:archive <change-id> --yes

# 查看所有规范
openspec list --specs

# 验证规范
openspec validate --specs
```

---

## 目录结构说明

### 提案阶段

```
openspec/
├── changes/
│   └── your-change-id/              # 进行中的变更
│       ├── proposal.md              # 变更提案 (Why + What)
│       ├── tasks.md                 # 任务清单 (How,可随时调整)
│       └── specs/                   # 规范增量 (要新增/修改的规范)
│           └── some-spec/
│               └── delta.md
└── specs/                           # 当前正式规范 (已归档的)
    └── existing-spec/
        └── spec.md
```

### 归档后

```
openspec/
├── changes/
│   └── archive/
│       └── 2025-12-31-your-change-id/    # 已归档的变更
│           ├── proposal.md
│           ├── tasks.md
│           └── specs/
└── specs/
    ├── existing-spec/
    │   └── spec.md
    └── new-spec/                          # 新增的正式规范
        └── spec.md                        # 从 delta.md 合并而来
```

---

## 最佳实践

### ✅ DO: 应该这样做

1. **复杂变更先提案**
   ```
   重构、新功能、架构变更 → 先用 /openspec:proposal
   ```

2. **提案阶段充分讨论**
   ```
   反复修改 proposal.md 和 tasks.md
   直到方案清晰、任务明确
   ```

3. **执行中发现问题立即调整**
   ```
   不要硬着头皮执行错误的计划
   随时修改 tasks.md 再继续
   ```

4. **完成后立即归档**
   ```
   趁着记忆清晰,将经验固化为规范
   ```

### ❌ DON'T: 不要这样做

1. **不要跳过提案直接编码**
   ```
   ❌ "帮我重构项目" → AI 立即开始改代码
   ✅ "帮我重构项目" → 先创建提案讨论方案
   ```

2. **不要忽略 tasks.md**
   ```
   ❌ tasks.md 写得模糊,执行时临时发挥
   ✅ tasks.md 详细具体,AI 照单执行
   ```

3. **不要忘记归档**
   ```
   ❌ 代码改完就结束,下次重复踩坑
   ✅ 归档为规范,积累项目知识库
   ```

---

## 实际效果对比

### 传统方式
```
用户: "重构项目结构"
AI: (直接开始改代码)
  - 移动文件...
  - 修改配置...
  - 遇到问题不知道怎么办
  - 用户发现不对,但已经改了一半
结果: 混乱、难以回滚、没有文档
```

### 使用 OpenSpec
```
用户: "重构项目结构"
AI: "让我先创建一个提案..."

[创建 proposal.md]
Why: 当前文件散乱,难以维护
What: 规范化目录结构,集中管理配置

[创建 tasks.md]
Phase 0: xxx
Phase 1: xxx
...

用户: "Phase 3 有问题,应该..."
AI: "好的,我修改一下 tasks.md"

用户: "现在可以了,开始执行"
AI: (按计划逐步执行,遇到问题自动调整)

结果: 有序、可控、形成文档
```

---

## 常见问题

### Q1: 什么时候需要用 OpenSpec?

**需要用**:
- 架构调整、目录重构
- 新功能开发 (需要多个文件修改)
- 破坏性变更
- 复杂的重构任务

**不需要用**:
- 修改一两行代码
- 简单的 bug 修复
- 临时的调试修改

### Q2: tasks.md 写多详细?

**经验法则**: 详细到 AI 不需要"发挥"就能执行。

```markdown
❌ 太模糊:
- [ ] 重构配置系统

✅ 刚好:
- [ ] 创建 configs/ 目录
- [ ] 移动 rules_config.json 到 configs/
- [ ] 修改 distribute_rules.py 中的配置路径引用
- [ ] 更新文档中的路径说明
```

### Q3: 中途发现方案有问题怎么办?

**直接告诉 AI 修改提案**:
```
用户: "等等,Phase 2 的方案不对,应该用 sys.argv 而不是环境变量"
AI: 修改 tasks.md → 继续执行
```

### Q4: 多个变更有依赖关系怎么办?

**按顺序执行**:
```
1. 先归档 change-a
2. 再创建和执行 change-b (基于已归档的规范)
```

---

## 在本项目中尝试 OpenSpec

### 1. 查看现有规范

```bash
openspec list --specs
```

输出:
```
Specs:
  config-loading          requirements 1
  distribution-config     requirements 3
```

### 2. 查看已归档的变更

```bash
ls openspec/changes/archive/
```

你会看到:
```
2025-12-31-refactor-project-structure-and-config/
2025-12-31-add-self-bootstrap-distribution/
```

### 3. 创建你自己的第一个提案

```bash
# 告诉 AI:
"我想添加一个新功能: 支持分发到 Windsurf AI 助手,
请帮我创建一个 OpenSpec 提案"

# AI 会:
1. 创建 openspec/changes/add-windsurf-support/
2. 生成 proposal.md 和 tasks.md
3. 等待你审阅和修改
```

---

## 总结

OpenSpec 的核心价值:

1. **📋 规范先行**: 不是直接写代码,而是先设计方案
2. **🔄 迭代优化**: 提案可以反复讨论修改
3. **✅ 可控执行**: 按清晰的任务清单执行,不会跑偏
4. **📚 知识沉淀**: 归档后形成正式规范,项目越来越"聪明"

**适合场景**:
- ✅ 团队协作项目 (需要规范和可追溯性)
- ✅ 长期维护项目 (需要积累知识库)
- ✅ 复杂重构任务 (需要分阶段执行)

**开始使用**:
1. 在项目中运行 `openspec init`
2. 遇到复杂需求时,让 AI 用 `/openspec:proposal` 创建提案
3. 讨论完善后,用 `/openspec:apply` 执行
4. 完成后用 `/openspec:archive` 归档

Happy coding with OpenSpec! 🚀
