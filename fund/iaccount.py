from abc import ABCMeta, abstractmethod


# 抽象クラス
class IAccount(metaclass=ABCMeta):
    @abstractmethod
    def get_account(self) -> dict:
        """口座情報を取得する

        Returns:
            dict: 口座情報
        """
        raise NotImplementedError
