#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""todo-cli: 一个纯标准库实现的命令行待办事项工具。

用法示例:
    python todo.py add "完成实习周报" -p high -d 2026-11-10
    python todo.py list
    python todo.py done 1
    python todo.py undone 1
    python todo.py edit 1 -t "新标题" -p high
    python todo.py remove 2
    python todo.py clear
"""

import argparse
import json
import os
import sys
from datetime import datetime

TODO_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "todo.json")

PRIORITIES = ("high", "medium", "low")

# ANSI 颜色（终端不支持时也能正常显示，只是无色）
COLORS = {
    "high": "\033[91m",     # 红
    "medium": "\033[93m",   # 黄
    "low": "\033[92m",      # 绿
    "reset": "\033[0m",
}


def load_tasks():
    """从 todo.json 读取任务列表；文件不存在或损坏时返回空列表。"""
    if not os.path.exists(TODO_FILE):
        return []
    try:
        with open(TODO_FILE, "r", encoding="utf-8") as f:
            data = json.load(f)
        return data if isinstance(data, list) else []
    except (json.JSONDecodeError, OSError):
        return []


def save_tasks(tasks):
    with open(TODO_FILE, "w", encoding="utf-8") as f:
        json.dump(tasks, f, ensure_ascii=False, indent=2)


def next_id(tasks):
    return max((t["id"] for t in tasks), default=0) + 1


def find_task(tasks, task_id):
    for t in tasks:
        if t["id"] == task_id:
            return t
    return None


def print_task(t, index=None):
    color = COLORS.get(t.get("priority", "low"), "")
    reset = COLORS["reset"]
    no = index if index is not None else t["id"]
    status = "✓" if t["done"] else " "
    line = "[{}] {:>3}. {}".format(status, no, t["title"])
    extras = []
    if t.get("priority"):
        extras.append("{}[{}]{}".format(color, t["priority"], reset))
    if t.get("due"):
        extras.append("截止 {}".format(t["due"]))
    if extras:
        line += "  " + " ".join(extras)
    print(line)


def cmd_add(args):
    tasks = load_tasks()
    task = {
        "id": next_id(tasks),
        "title": args.title,
        "priority": args.priority,
        "due": args.due,
        "done": False,
        "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    }
    tasks.append(task)
    save_tasks(tasks)
    print("已添加任务 #{}: {}".format(task["id"], task["title"]))


def _iter_filtered(tasks, args):
    result = tasks
    if getattr(args, "filter", "all") == "todo":
        result = [t for t in result if not t["done"]]
    elif getattr(args, "filter", "all") == "done":
        result = [t for t in result if t["done"]]
    if getattr(args, "priority", None):
        result = [t for t in result if t.get("priority") == args.priority]
    return result


def cmd_list(args):
    tasks = _iter_filtered(load_tasks(), args)
    if not tasks:
        print("（没有任务）")
        return
    # 未完成在前，同级按优先级 high > medium > low
    order = {p: i for i, p in enumerate(PRIORITIES)}
    tasks.sort(key=lambda t: (t["done"], order.get(t.get("priority", "low"), 2), t["id"]))
    for i, t in enumerate(tasks, 1):
        print_task(t, i)
    print("共 {} 项".format(len(tasks)))


def _set_done(args, done):
    tasks = load_tasks()
    task = find_task(tasks, args.id)
    if task is None:
        sys.exit("找不到任务 #{}".format(args.id))
    task["done"] = done
    save_tasks(tasks)
    print("任务 #{} 已标记为{}".format(args.id, "完成" if done else "未完成"))


def cmd_done(args):
    _set_done(args, True)


def cmd_undone(args):
    _set_done(args, False)


def cmd_edit(args):
    tasks = load_tasks()
    task = find_task(tasks, args.id)
    if task is None:
        sys.exit("找不到任务 #{}".format(args.id))
    if args.title is not None:
        task["title"] = args.title
    if args.priority is not None:
        task["priority"] = args.priority
    if args.due is not None:
        task["due"] = args.due
    save_tasks(tasks)
    print("任务 #{} 已更新".format(args.id))
    print_task(task)


def cmd_remove(args):
    tasks = load_tasks()
    task = find_task(tasks, args.id)
    if task is None:
        sys.exit("找不到任务 #{}".format(args.id))
    tasks.remove(task)
    save_tasks(tasks)
    print("已删除任务 #{}: {}".format(args.id, task["title"]))


def cmd_clear(args):
    tasks = load_tasks()
    if not tasks:
        print("（没有任务）")
        return
    if not args.yes:
        confirm = input("确定清空全部 {} 项任务? (y/N) ".format(len(tasks)))
        if confirm.strip().lower() != "y":
            print("已取消")
            return
    save_tasks([])
    print("已清空全部任务")


def build_parser():
    parser = argparse.ArgumentParser(prog="todo.py", description="命令行待办事项工具")
    sub = parser.add_subparsers(dest="command", required=True)

    p = sub.add_parser("add", help="新增任务")
    p.add_argument("title", help="任务标题")
    p.add_argument("-p", "--priority", choices=PRIORITIES, default="medium", help="优先级")
    p.add_argument("-d", "--due", default=None, help="截止日期，如 2026-11-10")
    p.set_defaults(func=cmd_add)

    p = sub.add_parser("list", help="列出任务")
    p.add_argument("-f", "--filter", choices=("all", "todo", "done"), default="all", help="按状态筛选")
    p.add_argument("-p", "--priority", choices=PRIORITIES, default=None, help="按优先级筛选")
    p.set_defaults(func=cmd_list)

    p = sub.add_parser("done", help="标记完成")
    p.add_argument("id", type=int, help="任务编号")
    p.set_defaults(func=cmd_done)

    p = sub.add_parser("undone", help="标记未完成")
    p.add_argument("id", type=int, help="任务编号")
    p.set_defaults(func=cmd_undone)

    p = sub.add_parser("edit", help="编辑任务")
    p.add_argument("id", type=int, help="任务编号")
    p.add_argument("-t", "--title", default=None, help="新标题")
    p.add_argument("-p", "--priority", choices=PRIORITIES, default=None, help="新优先级")
    p.add_argument("-d", "--due", default=None, help="新截止日期")
    p.set_defaults(func=cmd_edit)

    p = sub.add_parser("remove", help="删除任务")
    p.add_argument("id", type=int, help="任务编号")
    p.set_defaults(func=cmd_remove)

    p = sub.add_parser("clear", help="清空全部任务")
    p.add_argument("-y", "--yes", action="store_true", help="跳过确认")
    p.set_defaults(func=cmd_clear)

    return parser


def main():
    args = build_parser().parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
