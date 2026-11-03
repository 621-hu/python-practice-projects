#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""迷你留言板: 基于 Flask + SQLite 的轻量级 Web 应用。

运行:
    pip install -r requirements.txt
    python app.py
然后浏览器打开 http://127.0.0.1:5000
"""

import os
import sqlite3
from datetime import datetime

from flask import Flask, g, redirect, render_template, request, url_for

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
INSTANCE_DIR = os.path.join(BASE_DIR, "instance")
DB_PATH = os.path.join(INSTANCE_DIR, "board.db")

app = Flask(__name__, instance_path=INSTANCE_DIR, instance_relative_config=True)


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB_PATH)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(_exc):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    os.makedirs(INSTANCE_DIR, exist_ok=True)
    with sqlite3.connect(DB_PATH) as conn:
        conn.execute(
            """
            CREATE TABLE IF NOT EXISTS messages (
                id         INTEGER PRIMARY KEY AUTOINCREMENT,
                name       TEXT    NOT NULL DEFAULT '匿名',
                content    TEXT    NOT NULL,
                created_at TEXT    NOT NULL
            )
            """
        )


@app.route("/")
def index():
    db = get_db()
    messages = db.execute(
        "SELECT id, name, content, created_at FROM messages ORDER BY id DESC"
    ).fetchall()
    return render_template("index.html", messages=messages)


@app.route("/add", methods=["POST"])
def add():
    name = (request.form.get("name") or "").strip() or "匿名"
    content = (request.form.get("content") or "").strip()
    if content:
        db = get_db()
        db.execute(
            "INSERT INTO messages (name, content, created_at) VALUES (?, ?, ?)",
            (name, content, datetime.now().strftime("%Y-%m-%d %H:%M")),
        )
        db.commit()
    return redirect(url_for("index"))


@app.route("/delete/<int:mid>", methods=["POST"])
def delete(mid):
    db = get_db()
    db.execute("DELETE FROM messages WHERE id = ?", (mid,))
    db.commit()
    return redirect(url_for("index"))


if __name__ == "__main__":
    init_db()
    app.run(debug=True)
