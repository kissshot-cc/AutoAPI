from __future__ import annotations

from api.user_api import UserApi
from config.config_util import get_default_user


def default_login() -> str:
    u = get_default_user()
    api = UserApi()
    body = api.login(username=u["username"], password=u["password"], no_token=True)
    return str(body["token"])
