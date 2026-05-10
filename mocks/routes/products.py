from __future__ import annotations

import sqlite3
from typing import Any

from flask import Blueprint, jsonify, request

from config.config_util import get_db_path

products_bp = Blueprint("products", __name__)


def _conn() -> sqlite3.Connection:
    return sqlite3.connect(get_db_path(), check_same_thread=False)


@products_bp.route("/api/products", methods=["GET", "POST"])
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
