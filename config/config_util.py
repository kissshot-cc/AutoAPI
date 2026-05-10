from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import yaml

try:
    from dotenv import load_dotenv
except ImportError:
    def load_dotenv(*args: Any, **kwargs: Any) -> None: ...

_ROOT = Path(__file__).resolve().parent.parent
_CONFIG_PATH = _ROOT / "config" / "config.yaml"
_ENV_DIR = _ROOT / "config" / "env"
_cache: dict[str, Any] | None = None


def _deep_merge(base: dict, override: dict) -> dict:
    """递归合并两个字典，override 优先级更高。"""
    result = base.copy()
    for key, val in override.items():
        if key in result and isinstance(result[key], dict) and isinstance(val, dict):
            result[key] = _deep_merge(result[key], val)
        else:
            result[key] = val
    return result


def _load() -> dict[str, Any]:
    global _cache
    if _cache is None:
        # 加载 .env
        dotenv_path = _ROOT / ".env"
        if dotenv_path.exists():
            load_dotenv(dotenv_path)

        # 读取公共配置
        with open(_CONFIG_PATH, encoding="utf-8") as f:
            base_cfg = yaml.safe_load(f) or {}

        # 读取环境覆盖配置
        env_name = os.environ.get("API_ENV", "dev")
        env_path = _ENV_DIR / f"{env_name}.yaml"
        if env_path.exists():
            with open(env_path, encoding="utf-8") as f:
                env_cfg = yaml.safe_load(f) or {}
            base_cfg = _deep_merge(base_cfg, env_cfg)

        _cache = base_cfg
    return _cache


def reload_config() -> None:
    global _cache
    _cache = None


def get_env() -> str:
    return os.environ.get("API_ENV", "dev")


def get_base_url() -> str:
    cfg = _load()
    url = (cfg.get("base") or {}).get("url") or "http://127.0.0.1:5000"
    override = os.environ.get("API_BASE_URL")
    return override or url


def get_timeout() -> int:
    cfg = _load()
    override = os.environ.get("API_REQUEST_TIMEOUT")
    if override:
        return int(override)
    return int(cfg.get("timeout", 30))


def get_retries() -> int:
    cfg = _load()
    override = os.environ.get("API_REQUEST_RETRIES")
    if override:
        return int(override)
    return int(cfg.get("retries", 0))


def get_log_level() -> str:
    cfg = _load()
    log_cfg = cfg.get("log") or {}
    override = os.environ.get("LOG_LEVEL")
    if override:
        return override.upper()
    return (log_cfg.get("level") or "INFO").upper()


def get_db_path() -> Path:
    cfg = _load()
    rel = (cfg.get("database") or {}).get("path") or "test.db"
    p = Path(rel)
    if not p.is_absolute():
        p = _ROOT / p
    return p


def get_default_user() -> dict[str, str]:
    cfg = _load()
    u = cfg.get("user") or {}
    return {
        "username": u.get("username", "admin"),
        "password": u.get("password", "admin123"),
    }
