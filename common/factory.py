from __future__ import annotations

import uuid
from datetime import datetime
from typing import Any

from faker import Faker

_fake = Faker()
_fake.seed_instance(42)  # 可重复性；如需完全随机可注释此行


def fake_user() -> dict[str, str]:
    return {
        "username": f"user_{_fake.user_name()}_{uuid.uuid4().hex[:6]}",
        "password": _fake.password(length=12, special_chars=True),
    }


def fake_product() -> dict[str, Any]:
    return {
        "name": f"{_fake.color()} {_fake.word().capitalize()}",
        "stock": _fake.random_int(min=1, max=100),
        "price": round(_fake.pyfloat(min_value=1, max_value=999, right_digits=2), 2),
    }


def fake_price() -> float:
    return round(_fake.pyfloat(min_value=0.01, max_value=9999.99, right_digits=2), 2)


def fake_order_quantity() -> int:
    return _fake.random_int(min=1, max=5)
