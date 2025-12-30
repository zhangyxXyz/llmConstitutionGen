## 技能文档

### 基本信息
- 技能名: `project-info-generator`
- 创建人: @yiqiuzheng (yiqiuzheng@tencent.com)
- 版本: v2.0.0
- 更新时间: 2025-12-24

### 适用场景

此技能适用于以下场景:

1. **新项目首次接入 D2C**
   - 扫描项目结构和技术栈
   - 生成项目特定的参考文档
   - 初始化 d2c skill 配置

2. **项目技术栈发生重大变更**
   - 更新技术栈版本信息
   - 同步更新 d2c SKILL.md
   - 刷新公共资源清单

3. **新增大量公共组件或模块**
   - 重新扫描公共资源
   - 更新组件文档
   - 生成最新的导入路径

### 前置条件

- ✅ 项目已存在 `.codebuddy/skills/create/d2c/` 目录
- ✅ 项目采用 Monorepo 架构(有 `packages/` 目录)
- ✅ 项目有 `package.json` 文件
- ⚠️ 可选:项目有 `.codebuddy/rules/` 规范文档

### 使用示例

#### 触发方式

```
执行 project-info-generator 生成项目信息
```

或

```
为当前项目初始化 d2c 配置
```

或

```
更新 d2c 的项目技术栈信息
```

#### 执行流程

1. **确认执行**
   ```
   检测到这是 YKA 项目,将生成项目信息到 d2c skill。
   
   将执行以下操作:
   1. 扫描项目结构和公共资源
   2. 生成文档到 .codebuddy/skills/create/d2c/references/
   3. 更新 d2c SKILL.md 中的关键章节
   
   是否继续?(回复"是"或"继续")
   ```

2. **扫描项目**
   - 读取 README.md、package.json
   - 扫描 packages/components/、packages/utils/
   - 提取组件 Props、Events

3. **生成文档**
   - 生成 project-overview.md
   - 生成 component-templates.md
   - 生成 code-generation-guide.md
   - 更新 d2c SKILL.md

4. **验证输出**
   - 检查文档完整性
   - 验证组件信息准确性

### 输出文件

生成的文档位于 `.codebuddy/skills/create/d2c/references/`:

| 文件名 | 用途 | 必需 |
|-------|------|-----|
| `README.md` | 文件索引 | ✅ |
| `project-overview.md` | 项目概述和技术栈 | ✅ |
| `component-templates.md` | 公共组件清单 | ✅ |
| `code-generation-guide.md` | 代码生成规范 | ✅ |
| `amount-formatting-guide.md` | 金额格式化规范 | 可选 |
| `image-resource-guide.md` | 图片资源规范 | 可选 |
| `download-button-template.md` | DownloadButton 模板 | 可选 |

### 注意事项

⚠️ **执行频率**
- 此 skill **一般只使用一次**
- 避免频繁执行,以免覆盖手动调整的内容

⚠️ **手动调整**
- 生成的文档可能需要手动调整
- 特别是组件用途说明、使用示例等

⚠️ **版本管理**
- 生成的文档建议提交到 Git
- 方便团队共享和版本追溯

⚠️ **D2C SKILL.md 更新**
- 会自动更新 d2c SKILL.md 中的关键章节
- 如有冲突,需要手动解决

### 已知问题

- [ ] 组件 Props 类型提取可能不完整(复杂泛型)
- [ ] Events 参数提取依赖源码格式规范
- [ ] 不支持非 Vue 3 Composition API 组件

### 相关技能

- `figma-data-extractor`: 获取 Figma 设计稿数据
- `d2c`: 设计稿转代码(依赖本 skill 生成的项目信息)
- `yka-figma-to-code`: YKA 项目专用的 D2C skill

### 技术架构

此 skill 是 D2C 协同方案的**项目分析层**:

```
figma-data-extractor → project-info-generator → d2c
    (数据提取)            (项目分析)          (代码生成)
```

### 维护指南

#### 如何更新生成逻辑

1. 修改 SKILL.md 中的执行流程
2. 调整组件文档模板格式
3. 增加新的可选文档类型

#### 如何适配新项目

1. 检查项目目录结构是否符合 Monorepo
2. 确认 packages/ 目录下的子包名称
3. 调整路径别名和导入规则

#### 测试方法

1. 在测试项目中执行此 skill
2. 检查生成的文档内容
3. 验证 d2c skill 能否正常读取
4. 测试 d2c 生成代码时能否正确复用组件
