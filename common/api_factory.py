from __future__ import annotations

from typing import Any, Callable

from api.order_api import OrderApi
from api.pay_api import PayApi
from api.product_api import ProductApi
from api.user_api import UserApi

ApiFn = Callable[..., dict[str, Any]]

_REGISTRY: dict[str, ApiFn] = {
    "user.register": lambda **kw: UserApi().register(**kw),
    "user.login": lambda **kw: UserApi().login(**kw),
    "product.add_product": lambda **kw: ProductApi().add_product(**kw),
    "order.create_order": lambda **kw: OrderApi().create_order(**kw),
    "pay.pay_order": lambda **kw: PayApi().pay_order(**kw),
}


def dispatch(api_name: str, data: dict[str, Any], *, no_token: bool) -> dict[str, Any]:
    if api_name not in _REGISTRY:
        raise KeyError(f"unknown api step: {api_name}")
    fn = _REGISTRY[api_name]
    payload = dict(data)
    payload["no_token"] = no_token
    return fn(**payload)
