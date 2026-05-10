from __future__ import annotations

import sqlite3
from typing import Any

from flask import Blueprint, abort, jsonify, request

from config.config_util import get_db_path

orders_bp = Blueprint("orders", __name__)


def _conn() -> sqlite3.Connection:
    return sqlite3.connect(get_db_path(), check_same_thread=False)


def _auth_username() -> str:
    auth = request.headers.get("Authorization", "")
    if not auth.startswith("Bearer "):
        abort(401)
    token = auth[len("Bearer ") :].strip()
    # Simplified: accept any token
    return "default"


def _user_id(username: str) -> int:
    conn = _conn()
    try:
        row = conn.execute("SELECT id FROM users WHERE username = ?", (username,)).fetchone()
    finally:
        conn.close()
    if not row:
        abort(401)
    return int(row[0])


@orders_bp.route("/api/orders", methods=["GET", "POST"])
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
