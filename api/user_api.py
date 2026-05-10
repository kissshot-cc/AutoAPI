from __future__ import annotations

from typing import Any

from api.base_api import BaseApi


class UserApi(BaseApi):
    def register(self, username: str, password: str, *, no_token: bool = True) -> dict[str, Any]:
        return self.request_util.post(
            "/api/register",
            json={"username": username, "password": password},
            no_token=no_token,
        )

    def login(self, username: str, password: str, *, no_token: bool = True) -> dict[str, Any]:
        return self.request_util.post(
            "/api/login",
            json={"username": username, "password": password},
            no_token=no_token,
        )
