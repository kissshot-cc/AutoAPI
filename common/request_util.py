from __future__ import annotations

import json
from typing import Any

import allure
import requests
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from common.logger import get_logger
from common.token_manager import TokenManager
from config.config_util import get_base_url, get_retries, get_timeout

logger = get_logger(__name__)


class ApiRequestError(Exception):
    """API 请求失败异常。"""

    def __init__(self, method: str, url: str, status_code: int, body: Any) -> None:
        self.method = method
        self.url = url
        self.status_code = status_code
        self.body = body
        super().__init__(f"{method} {url} -> {status_code}: {body}")


class RequestUtil:
    def __init__(self) -> None:
        self.session = requests.Session()
        self.base_url = get_base_url().rstrip("/")
        self._setup_retry()

    def _setup_retry(self) -> None:
        retries = get_retries()
        if retries > 0:
            retry_strategy = Retry(
                total=retries,
                backoff_factor=1,
                status_forcelist=[429, 500, 502, 503, 504],
                allowed_methods=["GET", "POST", "PUT", "DELETE", "PATCH"],
            )
            adapter = HTTPAdapter(max_retries=retry_strategy)
            self.session.mount("http://", adapter)
            self.session.mount("https://", adapter)

    def _headers(self, extra: dict[str, str] | None, no_token: bool) -> dict[str, str]:
        h = {"Content-Type": "application/json"}
        if extra:
            h.update(extra)
        if not no_token:
            token = TokenManager.get_token()
            h["Authorization"] = f"Bearer {token}"
        return h

    def _attach_request(self, method: str, url: str, json_body: Any, params: Any) -> None:
        allure.attach(
            json.dumps({"method": method, "url": url, "json": json_body, "params": params}, ensure_ascii=False),
            name="request",
            attachment_type=allure.attachment_type.JSON,
        )

    def _attach_response(self, status_code: int, body: Any) -> None:
        allure.attach(
            json.dumps({"status": status_code, "body": body}, ensure_ascii=False),
            name="response",
            attachment_type=allure.attachment_type.JSON,
        )

    def send(
        self,
        method: str,
        path: str,
        *,
        json_body: dict[str, Any] | None = None,
        params: dict[str, Any] | None = None,
        headers: dict[str, str] | None = None,
        no_token: bool = False,
    ) -> dict[str, Any]:
        url = path if path.startswith("http") else f"{self.base_url}/{path.lstrip('/')}"
        hdrs = self._headers(headers, no_token)
        timeout = get_timeout()

        logger.info("%s %s", method, url)
        logger.debug("Request headers: %s", hdrs)

        self._attach_request(method, url, json_body, params)

        try:
            resp = self.session.request(
                method.upper(), url, json=json_body, params=params, headers=hdrs, timeout=timeout
            )
        except requests.RequestException as e:
            logger.error("Request failed: %s", e)
            raise ApiRequestError(method, url, 0, str(e)) from e

        try:
            body = resp.json() if resp.content else {}
        except ValueError:
            body = {"_raw": resp.text}

        self._attach_response(resp.status_code, body)

        if resp.status_code >= 400:
            logger.error("%s %s -> %d: %s", method, url, resp.status_code, body)

        resp.raise_for_status()
        return body if isinstance(body, dict) else {"_data": body}

    def get(self, path: str, **kwargs: Any) -> dict[str, Any]:
        return self.send("GET", path, **kwargs)

    def post(self, path: str, **kwargs: Any) -> dict[str, Any]:
        json_body = kwargs.pop("json", None)
        return self.send("POST", path, json_body=json_body, **kwargs)
