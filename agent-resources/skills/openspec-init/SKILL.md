---
name: OpenSpec 初始化助手
description: 指导初始化 OpenSpec 环境并填充 project.md 的标准流程,适用于任何使用 OpenSpec 规范驱动开发的项目
permission: allow
allowed-tools: Bash, Read, Edit, Write
---

# OpenSpec 初始化助手

## 🎯 核心定位

**OpenSpec 环境配置助手** - 帮助团队初始化 OpenSpec 规范驱动开发环境,并填充项目上下文信息到 `openspec/project.md`。

## 🚀 执行流程

### 阶段一:环境检查

#### 步骤 1:验证 OpenSpec CLI

```bash
openspec --version
```

- 如果命令失败,提示安装:
  ```bash
  npm install -g @fission-ai/openspec@latest
  ```

#### 步骤 2:检查项目初始化状态

```bash
ls openspec/
```

- 如果 `openspec/` 目录不存在:
  ```
  检测到项目未初始化 OpenSpec。

  请运行以下命令初始化:
  ```bash
  cd <项目根目录>
  openspec init
  ```

  初始化后会创建:
  - openspec/project.md  # 项目上下文(需填充)
  - openspec/specs/      # 当前规范(已部署功能)
  - openspec/changes/    # 变更提案(待部署功能)
  - AGENTS.md 或相应的工具配置文件
  ```

### 阶段二:填充 project.md

#### 步骤 1:读取当前状态

```bash
read_file openspec/project.md
```

检查各章节是否为空或模板状态。

#### 步骤 2:逐章节填充

**2.1 项目目的**

询问:
- 项目解决什么问题?
- 核心目标是什么?

建议格式:
```markdown
## 目的

[项目简介 - 1-2 句话]

**核心目标**:
- [目标 1]
- [目标 2]
```

**2.2 技术栈**

自动检测(如果存在):
- `package.json` → Node.js/前端项目
- `requirements.txt` / `pyproject.toml` → Python 项目
- `pom.xml` / `build.gradle` → Java 项目
- `go.mod` → Go 项目

询问确认并补充:
- 主要编程语言和版本
- 框架和库(Web 框架、数据库、工具等)

**2.3 项目约定**

逐项询问:

**代码风格**:
- 使用什么格式化工具? (Prettier、Black、gofmt 等)
- 命名规范? (camelCase、snake_case、kebab-case)
- 文件组织规则?

**架构模式**:
- 使用什么架构模式? (MVC、微服务、分层架构等)
- 模块划分原则?
- 设计原则? (SOLID、DRY 等)

**测试策略**:
- 使用什么测试框架?
- 覆盖率要求?
- 测试类型? (单元测试、集成测试、E2E 测试)

**Git 工作流**:
- 分支策略? (Git Flow、GitHub Flow、Trunk-Based)
- 提交消息格式? (Conventional Commits)
- PR/MR 流程?

**2.4 领域上下文**

询问:
- 业务领域特点? (电商、金融、游戏等)
- 特定术语和概念?
- AI 助手需要理解的领域知识?

**2.5 重要约束**

询问:
- 技术约束? (浏览器兼容性、平台限制等)
- 业务约束? (合规要求、SLA 要求等)
- 资源约束? (性能预算、成本限制等)

**2.6 外部依赖**

询问:
- 依赖哪些外部服务? (API、数据库、云服务)
- 是否有关键的第三方库?
- 开发/生产环境依赖差异?

### 阶段三:验证和完成

#### 步骤 1:验证填充完整性

检查每个章节是否已填充实质内容(非模板占位符)。

#### 步骤 2:提供后续建议

```
✅ project.md 已填充完成!

建议下一步:
1. 如有现有功能,在 openspec/specs/ 创建规范
2. 有新需求时,使用 openspec 创建变更提案
3. 让 AI 助手阅读 openspec/project.md 理解项目上下文

参考文档:
- OpenSpec 文档: https://github.com/Fission-AI/OpenSpec
- 工作流程: openspec/AGENTS.md
```

## 📋 最佳实践

### 模板示例

**技术栈示例** (Web 应用):
```markdown
## 技术栈

- **前端**: React 18.x + TypeScript 5.x
- **构建工具**: Vite 5.x
- **状态管理**: Zustand
- **UI 框架**: Tailwind CSS 3.x
- **后端**: Node.js 20.x + Express
- **数据库**: PostgreSQL 15.x
- **部署**: Docker + Kubernetes
```

**代码风格示例**:
```markdown
### 代码风格

- **格式化**: Prettier (自动格式化)
- **Linting**: ESLint + 项目自定义规则
- **命名规范**:
  - 组件: PascalCase (UserProfile)
  - 函数/变量: camelCase (getUserData)
  - 常量: UPPER_SNAKE_CASE (API_URL)
  - 文件: kebab-case (user-profile.tsx)
```

### 项目类型适配

**Web 应用**:
- 强调前端框架、API 设计、状态管理
- 测试策略包含 E2E 测试

**CLI 工具**:
- 强调参数解析、错误处理、输出格式
- 测试策略聚焦单元测试和集成测试

**库/SDK**:
- 强调 API 设计、向后兼容性、文档
- 测试策略包含示例和兼容性测试

## ⚠️ 注意事项

### 避免过度详细

- project.md 应简洁,聚焦核心约定
- 详细规范应在 `openspec/specs/` 中维护
- 避免重复 README.md 的内容

### 保持更新

- 技术栈升级时更新版本号
- 架构重构时更新架构模式
- 新增约定时补充到相应章节

### 触发时机

仅在以下情况执行:
1. 用户明确请求初始化 OpenSpec
2. 用户询问如何配置项目上下文
3. 检测到 `openspec/project.md` 内容为模板占位符

---

**记住**: 简洁但完整 - 给 AI 助手足够的上下文,但不要写成详尽文档。
