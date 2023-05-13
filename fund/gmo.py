import datetime
import hashlib
import hmac
import time

import requests

import settings
from fund.iwebsite import IWebSite


class GMO(IWebSite):
    """GMOコインのサイト"""

    __data: dict

    __apiKey = settings.GMO_API_KEY
    __secretKey = settings.GMO_API_SECRET

    __method = "GET"
    __endPoint = "https://api.coin.z.com/private"
    __path = "/v1/account/assets"

    def __init__(self):
        self.__data = {}

    def login(self):
        """サイトにログインする"""
        pass

    def get_account_info_dic(self, account_code: str) -> dict:
        """口座情報を取得する

        Args:
            account_code (str): アカウントコード

        Returns:
            dict: 口座情報
        """
        # APIの実行は最初の1回だけ
        if not self.__data:
            self.__data = self.get_assets()
        # JSONなのでいったん文字列で受ける
        amount = ""
        available = ""
        conversionRate = ""
        symbol = account_code.replace("GMO", "")
        for item in self.__data["data"]:
            if item["symbol"] == symbol:
                amount = item["amount"]
                available = item["available"]
                conversionRate = item["conversionRate"]
                break

        # データの設定
        account_info_dic = {
            settings.ACCOUNT_CODE: account_code,
            settings.AMOUNT: str(self.calc_amount(amount, conversionRate)),
            settings.QUANTITY: available,
            settings.UPDATE_DATE: "{0:%Y/%m/%d}".format(datetime.datetime.now()),
        }
        return account_info_dic

    def logout(self):
        """ログアウトする"""
        pass

    def get_assets(self) -> dict:
        """資産残高を取得する

        Returns:
            dict: 資産残高
        """
        timestamp = "{0}000".format(
            int(time.mktime(datetime.datetime.now().timetuple()))
        )
        text = timestamp + self.__method + self.__path
        sign = hmac.new(
            bytes(self.__secretKey.encode("ascii")),  # type: ignore
            bytes(text.encode("ascii")),
            hashlib.sha256,
        ).hexdigest()
        headers = {
            "API-KEY": self.__apiKey,
            "API-TIMESTAMP": timestamp,
            "API-SIGN": sign,
        }
        res = requests.get(self.__endPoint + self.__path, headers=headers)
        return res.json()

    def calc_amount(self, amount: str, conversionRate: str) -> int:
        """口座残高（円）の値を計算する

        Args:
            amount (str): 残高
            conversionRate (str): 円転レート

        Raises:
            ValueError: 数値変換できない場合

        Returns:
            int: 口座残高（円）
        """
        try:
            num_amount = float(amount)
            num_conversionRate = float(conversionRate)
            return int(round(num_amount * num_conversionRate, 0))
        except ValueError:
            raise ValueError("error-calc_amount method is ValueError")
