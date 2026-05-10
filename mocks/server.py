from __future__ import annotations

from flask import Flask

from mocks.routes.orders import orders_bp
from mocks.routes.pay import pay_bp
from mocks.routes.products import products_bp
from mocks.routes.users import users_bp


def create_app() -> Flask:
    app = Flask(__name__)
    app.register_blueprint(users_bp)
    app.register_blueprint(products_bp)
    app.register_blueprint(orders_bp)
    app.register_blueprint(pay_bp)
    return app


app = create_app()
