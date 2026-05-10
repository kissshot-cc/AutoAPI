from __future__ import annotations

import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path
from typing import Any

from config.config_util import get_log_level

_ROOT = Path(__file__).resolve().parent.parent
_LOG_DIR = _ROOT / "logs"
_LOG_DIR.mkdir(exist_ok=True)

_loggers: dict[str, logging.Logger] = {}


def _mask_token(value: str) -> str:
    """对 Authorization 头做掩码。"""
    if "Bearer " in value and len(value) > 16:
        return value[:13] + "..." + value[-4:]
    return value


class MaskedFormatter(logging.Formatter):
    """自定义 Formatter，对日志中的 token 做掩码。"""

    def format(self, record: logging.LogRecord) -> str:
        msg = super().format(record)
        if "Authorization" in msg:
            import re

            msg = re.sub(
                r"(Authorization[=:\"']\s*(?:Bearer\s*)?)([A-Za-z0-9_-]{6})\S+",
                r"\1\2***",
                msg,
            )
        return msg


def get_logger(name: str) -> logging.Logger:
    if name in _loggers:
        return _loggers[name]

    logger = logging.getLogger(name)
    level = getattr(logging, get_log_level(), logging.INFO)
    logger.setLevel(level)
    logger.propagate = False

    fmt = MaskedFormatter(
        "%(asctime)s | %(levelname)-8s | %(name)-20s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # 控制台 handler
    ch = logging.StreamHandler(sys.stdout)
    ch.setLevel(level)
    ch.setFormatter(fmt)
    logger.addHandler(ch)

    # 文件 handler（轮转，单文件 5MB，保留 3 个备份）
    fh = RotatingFileHandler(
        _LOG_DIR / "run.log",
        maxBytes=5 * 1024 * 1024,
        backupCount=3,
        encoding="utf-8",
    )
    fh.setLevel(level)
    fh.setFormatter(fmt)
    logger.addHandler(fh)

    _loggers[name] = logger
    return logger
