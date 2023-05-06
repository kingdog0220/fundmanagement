from abc import ABCMeta, abstractmethod


# 抽象クラス
class IWebSite(metaclass=ABCMeta):
    @abstractmethod
    def login(self):
        """サイトにログインする"""
        raise NotImplementedError

    @abstractmethod
    def get_account_info(self, account_code: str) -> dict:
        """口座情報を取得する"""
        raise NotImplementedError

    @abstractmethod
    def logout(self):
        """ログアウトする"""
        raise NotImplementedError
