from injector import Injector

import settings
from fund.gmo import GMO
from fund.mufj import MUFJBank
from fund.rakuten_securities import RakutenSecurities
from fund.sbi_securities import SBISecurities


class WebSiteDIContainer:
    def __init__(self):
        self.injector = Injector(self.__class__.config)

    @classmethod
    def config(cls, binder):
        # CODE値をキーにしてクラスを使うよう登録する
        binder.bind(settings.MUFJ_BANK, MUFJBank)
        binder.bind(settings.RAKUTEN_SECURITIES, RakutenSecurities)
        binder.bind(settings.GMO, GMO)
        binder.bind(settings.SBI_SECURITIES, SBISecurities)

    def resolve(self, cls):
        # injector.get()に引数を渡すと依存関係を解決してインスタンスを生成する
        return self.injector.get(cls)
