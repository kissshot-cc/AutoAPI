from __future__ import annotations

from typing import Any

from api.base_api import BaseApi


class ProductApi(BaseApi):
    def add_product(self, name: str, stock: int, price: float, *, no_token: bool = False) -> dict[str, Any]:
        return self.request_util.post(
            "/api/products",
            json={"name": name, "stock": stock, "price": price},
            no_token=no_token,
        )
