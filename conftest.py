from __future__ import annotations

import sqlite3
import threading
import time

import pytest
from werkzeug.serving import make_server

from common.auth import default_login
from common.db_init import init_db
from common.token_manager import TokenManager
from config.config_util import get_db_path, get_default_user, get_env, get_base_url


def pytest_sessionstart(session: pytest.Session) -> None:
    env = get_env()
    base = get_base_url()
    print(f"\n[env] API_ENV={env}, base_url={base}")

    path = get_db_path()
    if path.exists():
        path.unlink()
    init_db()
    u = get_default_user()
    conn = sqlite3.connect(path)
    try:
        conn.execute(
            "INSERT OR IGNORE INTO users (username, password) VALUES (?, ?)",
            (u["username"], u["password"]),
        )
        conn.commit()
    finally:
        conn.close()


@pytest.fixture(scope="session", autouse=True)
def _session_runtime() -> None:
    from mock_server import app

    server = make_server("127.0.0.1", 5000, app, threaded=True)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    time.sleep(0.4)

    TokenManager.register_login(default_login)
    TokenManager.clear()
    TokenManager.get_token()

    yield

    server.shutdown()

