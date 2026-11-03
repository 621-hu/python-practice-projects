# README

# 💬 迷你留言板（flask-mini-board）

一个基于 **Flask + SQLite** 的轻量级 Web 应用：访客可以发布留言、查看留言列表、删除留言。
适合实习生展示**Web 后端 + 模板渲染 + 数据库**的基础能力。

## ✨ 功能特性

- 发布留言（昵称可选，内容必填）
- 首页按时间倒序展示所有留言
- 一键删除留言
- 使用 SQLite 持久化，零额外数据库依赖
- 仅依赖 Flask，安装简单

## 🚀 快速开始

```bash
pip install -r requirements.txt
python app.py
```

然后浏览器打开 http://127.0.0.1:5000 即可使用。

## 🧩 项目结构

```
flask-mini-board/
├── app.py              # Flask 应用（路由 + 数据库操作）
├── templates/
│   └── index.html      # Jinja2 模板（前端页面）
├── instance/
│   └── board.db        # SQLite 数据库（自动生成，已忽略）
├── requirements.txt
└── README.md
```

## 🛠 主要路由

| 方法 | 路径 | 说明 |
| --- | --- | --- |
| GET | `/` | 展示留言列表 |
| POST | `/add` | 发布一条留言 |
| POST | `/delete/<id>` | 删除指定留言 |

## 📌 适合学习的技术点

- Flask 路由与 `render_template` 模板渲染
- 表单提交（`request.form`）与重定向
- SQLite 基础 CRUD（标准库 `sqlite3`）
- Jinja2 模板语法（`{% for %}` / `{{ }}`）
- Web 项目的基本目录结构与 `.gitignore` 配置
