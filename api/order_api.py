from __future__ import annotations

from typing import Any

from api.base_api import BaseApi


class OrderApi(BaseApi):
    def create_order(self, product_id: int, quantity: int, *, no_token: bool = False) -> dict[str, Any]:
        return self.request_util.post(
            "/api/orders",
            json={"product_id": product_id, "quantity": quantity},
            no_token=no_token,
        )
