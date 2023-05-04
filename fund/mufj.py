import settings
from fund.iwebsite import IWebSite


class MUFJBank(IWebSite):
    # ログイン状態を表すフラグ
    __isLogin: bool

    # サイトのCODE
    __code = settings.MUFJ_BANK

    @property
    def isLogin(self):
        return self.__isLogin

    def __init__(self):
        self.__isLogin = False

    def login(self):
        """サイトにログインする"""
        pass

    def get_account_info(self):
        """口座情報を取得する"""
        pass

    def logout(self):
        """ログアウトする"""
        pass
