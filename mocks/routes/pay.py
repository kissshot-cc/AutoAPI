from __future__ import annotations

import sqlite3
from typing import Any

from flask import Blueprint, jsonify, request

from config.config_util import get_db_path

pay_bp = Blueprint("pay", __name__)


def _conn() -> sqlite3.Connection:
    return sqlite3.connect(get_db_path(), check_same_thread=False)


@pay_bp.route("/api/pay", methods=["GET", "POST"])
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
