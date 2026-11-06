# Task Manager v2.0 设计文档 (Web + 数据库)

## 1. 目标与范围
将 v1.0 的 CLI 添加任务功能，升级为 **Web API + 数据库持久化**。
**本期只实现“添加任务”闭环**，验证 FastAPI 与数据库的联通。

## 2. 技术选型（Web 与数据库的合并）
- **Web 框架**：FastAPI（负责接收 HTTP 请求）
- **ORM 框架**：SQLAlchemy（负责把 Python 对象变成 SQL 语句）
- **数据库**：SQLite（轻量级关系型数据库，无需额外安装）
- **数据校验**：Pydantic（负责验证请求的 JSON 格式）

## 3. 架构与数据流向
当用户发送 POST 请求添加任务时，数据流向如下：
`客户端 (HTTP POST)` 
`FastAPI (路由)`
`Pydantic (校验参数)`
`SQLAlchemy (ORM 映射)`
`SQLite (持久化存入硬盘)`
`返回 201 Created 及任务详情`

## 4. 数据库表设计

表名：`tasks`
| 字段名      | 数据类型 | 约束         | 说明               |
| ----------- | -------- | ------------ | ------------------ |
| id          | String   | 主键         | 使用 UUID 自动生成 |
| title       | String   | 非空         | 任务标题           |
| description | String   | 可空         | 任务备注           |
| completed   | Boolean  | 默认 False   | 状态               |
| created_at  | DateTime | 默认当前时间 | 创建时间           |

## 5. 接口契约

**功能**：添加新任务
- **接口路径**：`/tasks`
- **请求方法**：`POST`
- **请求体（JSON）**：
  ```json
  {
    "title": "买牛奶",
    "description": "去超市买两盒低脂的"
  }