import hashlib
import hmac
import time
from datetime import datetime

import requests

import settings
from fund.iwebsite import IWebSite


class GMO(IWebSite):
    """GMOコインのサイト"""

    __apiKey = settings.GMO_API_KEY
    __secretKey = settings.GMO_API_SECRET
    __timestamp = "{0}000".format(int(time.mktime(datetime.now().timetuple())))
    __method = "GET"
    __endPoint = "https://api.coin.z.com/private"
    __path = "/v1/account/assets"

    __text = __timestamp + __method + __path
    __sign = hmac.new(
        bytes(__secretKey.encode("ascii")),  # type: ignore
        bytes(__text.encode("ascii")),
        hashlib.sha256,
    ).hexdigest()
    __headers = {"API-KEY": __apiKey, "API-TIMESTAMP": __timestamp, "API-SIGN": __sign}

    def login(self):
        """サイトにログインする"""
        pass

    def get_account_info(self, account_code: str) -> dict:
        """口座情報を取得する"""
        res = requests.get(self.__endPoint + self.__path, headers=self.__headers)
        data = res.json()
        return data

    def logout(self):
        """ログアウトする"""
        pass
