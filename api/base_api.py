from __future__ import annotations

from common.request_util import RequestUtil
from config.config_util import get_base_url


class BaseApi:
    def __init__(self) -> None:
        self.request_util = RequestUtil()
        self.base_url = get_base_url().rstrip("/")
