# Turtle-Soup-AI-Flask

海龟汤（Turtle Soup）推理小游戏：Flask 后端 + 纯静态前端页面，通过 REST API 交互；对局提问由大模型根据“题面 + 谜底”生成回答（需自行配置 `ARK_API_KEY`）。

## 功能简介

- 用户注册/登录（JWT）
- 题目列表与题面展示（支持 `zh/en`）
- 三种对局模式：`free` / `timed` / `limited_questions`
- 对局提问 `/api/play/chat`（依赖大模型配置）
- 结算得分与排行榜
- 管理员后台：题库 CRUD、用户管理

## 快速开始

### 1) 安装依赖

```bash
pip install -r requirements.txt
```

### 2) 配置大模型（必需）

本项目使用 `openai` SDK 调用 Volcengine Ark 兼容接口（通过环境变量配置）：

- `ARK_API_KEY`：必填
- `ARK_BASE_URL`：可选，默认 `https://ark.cn-beijing.volces.com/api/v3`
- `ARK_MODEL`：可选，默认 `doubao-seed-1-6-251015`

Windows PowerShell（仅对当前终端生效）：

```powershell
$env:ARK_API_KEY="你的key"
$env:ARK_MODEL="doubao-seed-1-6-251015"   # 可选
$env:ARK_BASE_URL="https://ark.cn-beijing.volces.com/api/v3"  # 可选
```

如果不配置 `ARK_API_KEY`，对局提问接口会失败（`/api/play/chat`）。

### 3) 启动服务

```bash
python backend/app.py
```

访问：
- 首页：`http://127.0.0.1:5000/`
- 登录：`/login.html`
- 排行榜：`/scoreboard.html`
- 管理后台：`/admin.html`

首次启动会自动建表并写入示例题；同时会确保存在开发管理员账号：
- 用户名：`admin`
- 密码：`admin123`

## 项目结构（简要）

```
backend/   # Flask 后端（Blueprint + Service + Model）
frontend/  # 静态前端页面（HTML/CSS/JS）
instance/  # SQLite 数据库（开发环境）
docs/      # 文档
```

## 常用接口（简要）

- `POST /api/auth/register` / `POST /api/auth/login`
- `GET /api/puzzles?lang=zh|en`
- `POST /api/play/start`（需登录）
- `POST /api/play/chat`（需登录 + 已配置 `ARK_API_KEY`）
- `POST /api/play/finish`（需登录）
- `GET /api/scores?limit=20&lang=zh|en`
- `GET/POST/PUT/DELETE /api/admin/*`（需管理员）

