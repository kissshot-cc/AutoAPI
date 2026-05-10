from __future__ import annotations

import sqlite3
import uuid
from html import escape
from typing import Any

from flask import Flask, abort, jsonify, request

from common.db_init import init_db, seed_demo_data
from config.config_util import get_db_path

app = Flask(__name__)
_tokens: dict[str, str] = {}


def _conn() -> sqlite3.Connection:
    return sqlite3.connect(get_db_path(), check_same_thread=False)


def _auth_username() -> str:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        abort(401)
    token = auth[len("Bearer ") :].strip()
    username = _tokens.get(token)
    if not username:
        abort(401)
    return username


def _user_id(username: str) -> int:
    conn = _conn()
    try:
        row = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    finally:
        conn.close()
    if not row:
        abort(401)
    return int(row[0])


@app.get("/")
def index() -> str:
    conn = _conn()
    try:
        users = conn.execute("SELECT id, username FROM users ORDER BY id").fetchall()
        products = conn.execute("SELECT id, name, stock, price FROM products ORDER BY id").fetchall()
        orders = conn.execute(
            """
            SELECT o.id, u.username, p.name, o.quantity, o.status
            FROM orders o
            LEFT JOIN users u ON u.id = o.user_id
            LEFT JOIN products p ON p.id = o.product_id
            ORDER BY o.id
            """
        ).fetchall()
    finally:
        conn.close()

    api_links = """
    <section><h2>浏览器可读接口（JSON）</h2>
    <ul>
      <li><a href="/api/products">GET /api/products</a> — 商品列表</li>
      <li><a href="/api/orders">GET /api/orders</a> — 订单列表</li>
      <li><a href="/api/users">GET /api/users</a> — 用户列表（不含密码）</li>
      <li><a href="/api/register">GET /api/register</a> — 说明（注册请用 POST）</li>
      <li><a href="/api/login">GET /api/login</a> — 说明（登录请用 POST）</li>
      <li><a href="/api/pay">GET /api/pay</a> — 说明（支付请用 POST）</li>
    </ul></section>
    """

    def rows_users() -> str:
        lines = []
        for uid, name in users:
            lines.append(f"<tr><td>{uid}</td><td>{escape(str(name))}</td></tr>")
        return "\n".join(lines) if lines else "<tr><td colspan='2'>暂无</td></tr>"

    def rows_products() -> str:
        lines = []
        for pid, name, stock, price in products:
            lines.append(
                f"<tr><td>{pid}</td><td>{escape(str(name))}</td>"
                f"<td>{stock}</td><td>{price}</td></tr>"
            )
        return "\n".join(lines) if lines else "<tr><td colspan='4'>暂无</td></tr>"

    def rows_orders() -> str:
        lines = []
        for oid, uname, pname, qty, status in orders:
            lines.append(
                f"<tr><td>{oid}</td><td>{escape(str(uname or ''))}</td>"
                f"<td>{escape(str(pname or ''))}</td><td>{qty}</td>"
                f"<td>{escape(str(status))}</td></tr>"
            )
        return "\n".join(lines) if lines else "<tr><td colspan='5'>暂无</td></tr>"

    return f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="utf-8"/>
  <meta name="viewport" content="width=device-width, initial-scale=1"/>
  <title>APIAuto Mock</title>
  <style>
    body {{ font-family: system-ui, sans-serif; margin: 1.5rem; max-width: 960px; }}
    h1 {{ font-size: 1.35rem; }}
    h2 {{ font-size: 1.1rem; margin-top: 1.5rem; }}
    table {{ border-collapse: collapse; width: 100%; margin: 0.5rem 0 1rem; }}
    th, td {{ border: 1px solid #ccc; padding: 0.35rem 0.5rem; text-align: left; }}
    th {{ background: #f4f4f4; }}
    a {{ color: #0b57d0; }}
    section ul {{ line-height: 1.7; }}
  </style>
</head>
<body>
  <h1>Mock API 演示</h1>
  <p>下方为数据库当前快照；JSON 接口见链接。</p>
  {api_links}
  <section><h2>用户</h2>
  <table><thead><tr><th>id</th><th>username</th></tr></thead>
  <tbody>{rows_users()}</tbody></table></section>
  <section><h2>商品</h2>
  <table><thead><tr><th>id</th><th>name</th><th>stock</th><th>price</th></tr></thead>
  <tbody>{rows_products()}</tbody></table></section>
  <section><h2>订单</h2>
  <table><thead><tr><th>id</th><th>user</th><th>product</th><th>qty</th><th>status</th></tr></thead>
  <tbody>{rows_orders()}</tbody></table></section>
</body>
</html>"""


@app.route("/api/register", methods=["GET", "POST"])
def register() -> Any:
    if request.method == "GET":
        return jsonify(
            {
                "method": "POST",
                "path": "/api/register",
                "body": {"username": "string", "password": "string"},
                "note": "浏览器直接打开本页为说明；注册请使用 POST + JSON。",
            }
        )
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    if not username or not password:
        return jsonify({"error": "invalid"}), 400
    conn = _conn()
    try:
        conn.execute("INSERT INTO users (username, password) VALUES (?, ?)", (username, password))
        conn.commit()
    except sqlite3.IntegrityError:
        return jsonify({"ok": True, "exists": True})
    finally:
        conn.close()
    return jsonify({"ok": True})


@app.route("/api/login", methods=["GET", "POST"])
def login() -> Any:
    if request.method == "GET":
        return jsonify(
            {
                "method": "POST",
                "path": "/api/login",
                "body": {"username": "string", "password": "string"},
                "note": "登录请使用 POST；成功响应中含 token，后续接口需 Header: Authorization: Bearer <token>。",
            }
        )
    data = request.get_json(force=True, silent=True) or {}
    username = data.get("username")
    password = data.get("password")
    conn = _conn()
    try:
        row = conn.execute(
            "SELECT id FROM users WHERE username = ? AND password = ?",
            (username, password),
        ).fetchone()
    finally:
        conn.close()
    if not row:
        return jsonify({"error": "auth failed"}), 401
    token = str(uuid.uuid4())
    _tokens[token] = str(username)
    return jsonify({"token": token})


@app.route("/api/products", methods=["GET", "POST"])
def products() -> Any:
    if request.method == "GET":
        conn = _conn()
        try:
            rows = conn.execute(
                "SELECT id, name, stock, price FROM products ORDER BY id"
            ).fetchall()
        finally:
            conn.close()
        return jsonify(
            [
                {"id": r[0], "name": r[1], "stock": r[2], "price": r[3]}
                for r in rows
            ]
        )
    _auth_username()
    data = request.get_json(force=True, silent=True) or {}
    name = str(data.get("name", "item"))
    stock = int(data.get("stock", 0))
    price = float(data.get("price", 0))
    conn = _conn()
    try:
        cur = conn.execute(
            "INSERT INTO products (name, stock, price) VALUES (?, ?, ?)",
            (name, stock, price),
        )
        conn.commit()
        pid = int(cur.lastrowid)
    finally:
        conn.close()
    return jsonify({"id": pid})


@app.get("/api/users")
def list_users() -> Any:
    conn = _conn()
    try:
        rows = conn.execute("SELECT id, username FROM users ORDER BY id").fetchall()
    finally:
        conn.close()
    return jsonify([{"id": r[0], "username": r[1]} for r in rows])


@app.route("/api/orders", methods=["GET", "POST"])
def orders() -> Any:
    if request.method == "GET":
        conn = _conn()
        try:
            rows = conn.execute(
                """
                SELECT o.id, o.user_id, u.username, o.product_id, p.name,
                       o.quantity, o.status
                FROM orders o
                LEFT JOIN users u ON u.id = o.user_id
                LEFT JOIN products p ON p.id = o.product_id
                ORDER BY o.id
                """
            ).fetchall()
        finally:
            conn.close()
        return jsonify(
            [
                {
                    "id": r[0],
                    "user_id": r[1],
                    "username": r[2],
                    "product_id": r[3],
                    "product_name": r[4],
                    "quantity": r[5],
                    "status": r[6],
                }
                for r in rows
            ]
        )
    username = _auth_username()
    uid = _user_id(username)
    data = request.get_json(force=True, silent=True) or {}
    pid = int(data.get("product_id"))
    qty = int(data.get("quantity", 1))
    conn = _conn()
    try:
        conn.execute("BEGIN IMMEDIATE")
        cur = conn.execute(
            "UPDATE products SET stock = stock - ? WHERE id = ? AND stock >= ?",
            (qty, pid, qty),
        )
        if cur.rowcount != 1:
            conn.rollback()
            return jsonify({"error": "insufficient stock"}), 409
        cur = conn.execute(
            "INSERT INTO orders (user_id, product_id, quantity, status) VALUES (?, ?, ?, 'created')",
            (uid, pid, qty),
        )
        oid = int(cur.lastrowid)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
    return jsonify({"order_id": oid, "ok": True})


@app.route("/api/pay", methods=["GET", "POST"])
def pay() -> Any:
    if request.method == "GET":
        return jsonify(
            {
                "method": "POST",
                "path": "/api/pay",
                "headers": {"Authorization": "Bearer <token>"},
                "body": {"order_id": "integer"},
                "note": "支付请使用 POST；需登录 token。",
            }
        )
    _auth_username()
    data = request.get_json(force=True, silent=True) or {}
    oid = int(data.get("order_id"))
    conn = _conn()
    try:
        cur = conn.execute("UPDATE orders SET status = 'paid' WHERE id = ?", (oid,))
        if cur.rowcount != 1:
            return jsonify({"error": "not found"}), 404
        conn.commit()
    finally:
        conn.close()
    return jsonify({"ok": True, "status": "paid"})


if __name__ == "__main__":
    init_db()
    seed_demo_data()
    app.run(host="127.0.0.1", port=5000, debug=False)
