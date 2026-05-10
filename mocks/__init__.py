from __future__ import annotations

from mocks.routes.orders import orders_bp
from mocks.routes.pay import pay_bp
from mocks.routes.products import products_bp
from mocks.routes.users import users_bp
from mocks.server import create_app

__all__ = ["create_app", "users_bp", "products_bp", "orders_bp", "pay_bp"]
