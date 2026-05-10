from __future__ import annotations

import sqlite3
from typing import Any

from config.config_util import get_db_path


def query_one(sql: str, params: tuple[Any, ...] = ()) -> tuple[Any, ...] | None:
    conn = sqlite3.connect(get_db_path())
    try:
        cur = conn.execute(sql, params)
        row = cur.fetchone()
        return row
    finally:
        conn.close()


def query_all(sql: str, params: tuple[Any, ...] = ()) -> list[tuple[Any, ...]]:
    conn = sqlite3.connect(get_db_path())
    try:
        cur = conn.execute(sql, params)
        return cur.fetchall()
    finally:
        conn.close()


def execute(sql: str, params: tuple[Any, ...] = ()) -> None:
    conn = sqlite3.connect(get_db_path())
    try:
        conn.execute(sql, params)
        conn.commit()
    finally:
        conn.close()
