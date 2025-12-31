# config-loading Specification

## Purpose
定义配置文件加载机制的行为规范,支持通过命令行参数指定配置文件路径,实现灵活的多环境配置管理。
## Requirements
### Requirement: 配置文件路径可配置
配置文件路径 MUST 支持通过命令行参数指定,默认使用 `configs/rules_config.json`。

#### Scenario: 使用默认配置文件路径
**Given** 用户未提供命令行参数
**When** 运行 `python distribute_rules.py`
**Then** 系统应加载 `configs/rules_config.json` 作为配置文件

#### Scenario: 使用显式指定的配置文件
**Given** 用户提供配置文件路径参数
**When** 运行 `python distribute_rules.py configs/self_bootstrap.json`
**Then** 系统应加载 `configs/self_bootstrap.json` 作为配置文件

#### Scenario: 配置文件不存在时的错误处理
**Given** 用户指定的配置文件不存在
**When** 运行 `python distribute_rules.py nonexistent.json`
**Then** 系统应显示错误信息并退出

