# D2C 协同方案技术详解

> 本文档详细介绍 D2C 协同方案的技术架构、实现原理和最佳实践,供技能维护者和深度用户参考。

## 一、背景

由于AI模型越来越强,目前d2c效果越来越好,司内也有很多同学研究了d2c方案,总结各方技术方案优劣,开发符合各团队技术特点的d2c方案尤为重要。

本方案基于游可爱前端团队项目特点,针对已有的设计稿完整实践d2c方案并达到满意效果后,抽离了3个高复用性且实用的skill,以方便在不同项目中低成本、快速、高质量地运用好这些skill实现设计稿还原。

## 二、效果展示

用claude-4.5-opus,调用d2c skill去还原设计稿(自动调用获取项目信息以及获取设计稿信息的skill协同完成)

![](https://files.mdnice.com/user/111394/502d47b5-c732-4d62-b6e7-9a126f014de3.png)

会出一个checklist,包含项目特有的公共组件、工具等

![](https://files.mdnice.com/user/111394/e9b5b83c-dc84-481f-8d73-6dd223187ef8.png)

输入继续,完成设计稿还原

![](https://files.mdnice.com/user/111394/7fdd3fe1-755e-4ed0-83ec-ab5fce7eb24a.png)

- 还原效果

  ![](https://files.mdnice.com/user/111394/8726add9-9b9d-4fda-96d1-9c703846a794.png)

- 原设计稿

  ![](https://files.mdnice.com/user/111394/b1f3d755-2e29-4617-b065-0b740abbb867.png)

对比下来还原度是比较高的。

## 三、使用方式

### 1、资源下载

- figma-data-extractor: <https://knot.woa.com/skills/detail/88>
- project-info-generator: <https://knot.woa.com/skills/detail/94>
- d2c: <https://knot.woa.com/skills/detail/95>

### 2、如何使用

为了方便各种技术栈的项目快速接入d2c,提供了3个skill:
- figma-data-extractor: 获取设计稿数据和截图信息
- project-info-generator: 为了方便新项目接入d2c而准备的skill,一般只会用一次,将生成项目信息到d2c references文件夹并修改d2c项目相关信息
- d2c: figma设计稿转代码

可参考以下方式使用:

#### 1. 先配置figma-data-extractor的figma token

获取figma token

![](https://files.mdnice.com/user/111394/f3a44a68-0392-4fb2-95db-0d9009097537.png)

在对应skill下配置.env的FIGMA_TOKEN

![](https://files.mdnice.com/user/111394/d905b147-ecd5-4ca6-940a-143e2a9c373d.png)

```
FIGMA_TOKEN=
```

#### 2. 执行project-info-generator生成项目信息

会针对当前项目README.md、packages.json、.codebuddy/rules等项目信息,生成文件到d2c skill的references文件夹中,并修改d2c skill项目相关信息。

一般只使用一次,只在新项目中接入d2c skill的时候用,为d2c初始化项目信息。

#### 3. 执行d2c完成设计稿转代码流程

- 复制设计稿对应区域设计稿链接

  ![](https://files.mdnice.com/user/111394/ae40be9d-21d0-47eb-a796-ad3a9efd1c39.png)

- 执行create:设计稿转代码命令 command或者d2c skill

  ![](https://files.mdnice.com/user/111394/736eb144-1464-4c8b-8f2e-f0d00d8373b3.png)

- 粘贴设计稿链接调用

  ![](https://files.mdnice.com/user/111394/46fbdefe-8d91-402f-82b3-234d410c3d4f.png)

贴对应的设计稿链接,会调用figma-data-extractor获取设计稿数据,并参考project-info-generator生成的项目信息,高质量还原figma设计稿。

估计会重复修改skill,调整项目信息这一块,使其生成的代码更符合项目代码规范,更好地运用项目公共资源等。

## 四、D2C 协同方案技术详解

### 一、整体架构概览

这是一个基于 **三层分离架构** 的 Design to Code 解决方案:

```
┌─────────────────────────────────────────────────────────────────┐
│                     D2C 协同架构                                  │
└─────────────────────────────────────────────────────────────────┘

  ┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
  │  数据提取层       │      │  项目分析层       │      │  代码生成层       │
  │                  │      │                  │      │                  │
  │ figma-data-     │ ───▶ │ project-info-   │ ───▶ │      d2c        │
  │  extractor      │      │  generator      │      │                  │
  │                  │      │                  │      │                  │
  │ 设计稿数据       │      │ 项目上下文       │      │ 代码实现         │
  └──────────────────┘      └──────────────────┘      └──────────────────┘
         ↓                          ↓                          ↓
    Figma API              项目静态扫描                   Vue 3 代码
    本地脚本                文档生成                      Tailwind CSS
```

[继续包含原文档的所有技术详解内容...]

## 五、规划

- 可沿用这套里流程快速开发业务小程序d2c skill
- 接入antd-vue mcp,组件信息更加完整、规范
- 实现接口联调的skill(加入项目特别注意点,比如pb、金额字段的适配)
- 持续完善d2c的模板,加入更多项目特别注意点,提高还原度

## 六、问题

### 1、费用

没有开启figma dev mode,会有限流,后续估计得团队共用token。

申请dev mode付费: 2151.00元/年

https://8000.woa.com/v3/Software/Detail?software_guid=F4E95E3496864E26BB161C7B383737D2

### 2、效果

大模型还是有一定幻觉,目前claude-4.5-opus稍微比claude-4.5-sonnet效果好一点,但每次生成的效果都没法100%还原与一致。

本方案算是一定程度使还原效果更符合预期,尤其是针对项目技术信息。

## 九、总结

这是一个 **分层架构、职责清晰、高度协同** 的通用 D2C 解决方案:

- **figma-data-extractor**: 解决 Figma API → CSS 的转换问题
- **project-info-generator**: 解决项目上下文的获取和沉淀问题
- **d2c**: 解决设计稿 → 代码的还原问题

三者通过 **标准化的数据格式** 和 **明确的协同机制** 实现高效协作,最终输出 **高还原度、符合项目规范** 的 Vue 3 代码。

大伙可以立即复用到项目中看效果,目前行业痛点是Figma设计稿组件没有与业务组件相关联,司内有同学通过figma插件去做组件标志(一定程度使设计稿更规范),或者说直接让设计师按规范设计设计稿(这个设计师上手成本估计偏高),本文则通过项目信息去映射Figma组件与业务组件,实现组件复用,提高开发效率。效果没有直接设计稿做标注好,但是成本相对较低,是个方便不同项目快速复用的d2c方案。

欢迎大伙点赞、评论、分享,一起交流学习,共同进步!

特别鸣谢@damyxu针对获取设计稿数据的答疑解惑

> 参考:
> 1. 运用官方mcp的d2c skill: <https://git.woa.com/WGFE/doc-ai-knowledge>
> 2. 拒绝"一次性代码": D2C Next 如何攻克 UI 还原的持续迭代难题?: <https://km.woa.com/articles/show/648656?kmref=user_articles_list>
> 3. 打造稳定可靠的前端AI工程化: <https://km.woa.com/articles/show/647720?kmref=user_articles_list>
