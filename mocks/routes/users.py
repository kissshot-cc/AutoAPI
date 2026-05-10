from __future__ import annotations

import sqlite3
from typing import Any

from flask import Blueprint, abort, jsonify, request

from common.db_init import init_db, seed_demo_data
from config.config_util import get_db_path

users_bp = Blueprint("users", __name__)
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


@users_bp.route("/api/register", methods=["GET", "POST"])
def register() -> Any:
    if request.method == "GET":
        return jsonify(
            {
                "method": "POST",
                "path": "/api/register",
                "body": {"username": "string", "password": "string"},
                "note": "注册请使用 POST + JSON。",
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


@users_bp.route("/api/login", methods=["GET", "POST"])
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
    import uuid

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


@users_bp.get("/api/users")
def list_users() -> Any:
    conn = _conn()
    try:
        rows = conn.execute("SELECT id, username FROM users ORDER BY id").fetchall()
    finally:
        conn.close()
    return jsonify([{"id": r[0], "username": r[1]} for r in rows])
