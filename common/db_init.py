from __future__ import annotations

import sqlite3

from config.config_util import get_db_path


def init_db() -> None:
    path = get_db_path()
    conn = sqlite3.connect(path)
    try:
        conn.executescript(
            """
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT UNIQUE NOT NULL,
                password TEXT NOT NULL
            );

            CREATE TABLE IF NOT EXISTS products (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                stock INTEGER NOT NULL DEFAULT 0,
                price REAL NOT NULL DEFAULT 0
            );

            CREATE TABLE IF NOT EXISTS orders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id INTEGER,
                product_id INTEGER NOT NULL,
                quantity INTEGER NOT NULL,
                status TEXT NOT NULL DEFAULT 'created'
            );
            """
        )
        conn.commit()
    finally:
        conn.close()


def seed_demo_data() -> None:
    """插入演示用初始数据（幂等：可重复调用）。"""
    init_db()
    path = get_db_path()
    conn = sqlite3.connect(path)
    try:
        conn.execute(
            "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
            ("demo", "demo123"),
        )
        conn.execute(
            "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
            ("alice", "alice123"),
        )
        n_products = conn.execute("SELECT COUNT(*) FROM products").fetchone()[0]
        if n_products == 0:
            conn.executemany(
                "INSERT INTO products (name, stock, price) VALUES (?, ?, ?)",
                [
                    ("无线鼠标", 120, 89.0),
                    ("机械键盘", 45, 399.0),
                    ("USB-C 扩展坞", 30, 259.0),
                ],
            )
        n_orders = conn.execute("SELECT COUNT(*) FROM orders").fetchone()[0]
        if n_orders == 0:
            row_u = conn.execute("SELECT id FROM users WHERE username = ?", ("demo",)).fetchone()
            row_p = conn.execute("SELECT id FROM products ORDER BY id LIMIT 1").fetchone()
            if row_u and row_p:
                uid, pid = int(row_u[0]), int(row_p[0])
                conn.execute(
                    "INSERT INTO orders (user_id, product_id, quantity, status) VALUES (?, ?, ?, ?)",
                    (uid, pid, 2, "created"),
                )
        conn.commit()
    finally:
        conn.close()
