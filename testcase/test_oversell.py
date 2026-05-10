from __future__ import annotations

import threading
from concurrent.futures import ThreadPoolExecutor, as_completed

import allure
import pytest
import requests

from api.order_api import OrderApi
from api.product_api import ProductApi
from common.db_assert import get_product_stock
from common.factory import fake_product


@allure.epic("电商接口自动化")
@allure.feature("并发稳定性")
@allure.severity(allure.severity_level.CRITICAL)
@pytest.mark.concurrency
@pytest.mark.regression
def test_concurrent_orders_respect_stock() -> None:
    allure.title("并发下单：验证库存不超卖")
    product_data = fake_product()
    product_data["stock"] = 10

    papi = ProductApi()
    oapi = OrderApi()
    created = papi.add_product(**product_data)
    pid = int(created["id"])

    successes = 0
    lock = threading.Lock()

    def worker() -> None:
        nonlocal successes
        try:
            oapi.create_order(product_id=pid, quantity=1)
        except requests.HTTPError:
            return
        with lock:
            successes += 1

    with ThreadPoolExecutor(max_workers=24) as pool:
        futures = [pool.submit(worker) for _ in range(30)]
        for f in as_completed(futures):
            f.result()

    stock_left = get_product_stock(pid)
    assert successes <= 10
    assert stock_left >= 0
    assert stock_left == 10 - successes
