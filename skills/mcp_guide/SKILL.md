---
name: MCP 服务使用指南
description: 简要说明特定mcp服务的常用调用与查询约定
allowed-tools: *
permission: allow
---

# MCP 相关服务基础使用指南

## gongfeng

- 文件版本管理：涵盖常规 SVN 操作及公司定制功能
- 当我询问某个函数/模块作者时，直接查询并汇总作者与提交信息，默认查看最新记录
- 当前项目地址：`https://tc-svn.tencent.com/soul/Soul_Client/trunk/SoulClient`

## tapd_mcp_http

- 若提供以 `https://tapd.woa.com/` 开头的需求链接，直接查询该需求详情
- 未提供链接但出现 `本周需求`、`本迭代`、`Tapd` 等关键词时，默认查询需求列表，并结合时间跨度等上下文匹配相关需求；信息不足时先询问
- 非常重要：默认目标用户包含 `seiunzhang`，除非明确指定其他目标；已完成/转测的单子只要操作人是我也计入
- 所有查询仅在 `SO` 空间范围内执行
