# README

# 📝 Python CLI 待办工具（todo-cli）

一个简单的命令行待办事项（Todo）工具，使用**纯 Python 标准库**实现。
适合 Python 初学者 / 实习生练手，也可直接用于日常任务管理。

## ✨ 功能特性

- 新增 / 列出 / 完成 / 恢复 / 编辑 / 删除 / 清空任务
- 任务优先级（`high` / `medium` / `low`）与彩色展示
- 可选截止日期
- 数据保存在本地 `todo.json`，无需数据库
- **零第三方依赖**，clone 即可运行

## 🚀 快速开始

```bash
# 需要 Python 3.8+
python todo.py add "完成实习周报" -p high -d 2026-11-10
python todo.py list
python todo.py done 1
```

## 📖 命令说明

| 命令 | 说明 | 示例 |
| --- | --- | --- |
| `add` | 新增任务 | `python todo.py add "看书" -p low` |
| `list` | 列出任务（可筛选） | `python todo.py list -f todo` |
| `done` | 标记完成 | `python todo.py done 1` |
| `undone` | 标记未完成 | `python todo.py undone 1` |
| `edit` | 编辑任务 | `python todo.py edit 1 -t "新标题" -p high` |
| `remove` | 删除任务 | `python todo.py remove 2` |
| `clear` | 清空全部 | `python todo.py clear` |

## 🗂 数据格式

任务保存在 `todo.json`：

```json
[
  {
    "id": 1,
    "title": "完成实习周报",
    "priority": "high",
    "due": "2026-11-10",
    "done": false,
    "created_at": "2026-11-03 13:50:00"
  }
]
```

## 🧩 项目结构

```
python-cli-todo/
├── todo.py          # 主程序
├── todo.json        # 任务数据（自动生成，已忽略）
├── requirements.txt # 依赖说明（无第三方依赖）
└── README.md
```

## 📌 适合学习的技术点

- `argparse` 子命令式 CLI 设计
- JSON 文件持久化
- 列表排序、字典操作
- ANSI 彩色终端输出
- 模块化函数与 `main()` 入口约定
