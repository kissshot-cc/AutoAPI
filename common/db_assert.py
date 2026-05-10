from __future__ import annotations

from common.db_util import query_one


def assert_product_stock(product_id: int, expected_min: int = 0) -> None:
    row = query_one("SELECT stock FROM products WHERE id = ?", (product_id,))
    assert row is not None, f"product {product_id} not found"
    stock = int(row[0])
    assert stock >= expected_min, f"stock {stock} < {expected_min}"


def get_product_stock(product_id: int) -> int:
    row = query_one("SELECT stock FROM products WHERE id = ?", (product_id,))
    assert row is not None
    return int(row[0])
