from __future__ import annotations

from typing import Any

from api.base_api import BaseApi


class PayApi(BaseApi):
    def pay_order(self, order_id: int, *, no_token: bool = False) -> dict[str, Any]:
        return self.request_util.post(
            "/api/pay",
            json={"order_id": order_id},
            no_token=no_token,
        )
