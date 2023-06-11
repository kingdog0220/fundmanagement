from injector import Injector

import settings
from fund.website.common.iwebsite import IWebSite
from fund.website.dc import DCBank
from fund.website.gmo import GMO
from fund.website.mufj import MUFJBank
from fund.website.rakuten_bank import RakutenBank
from fund.website.rakuten_securities import RakutenSecurities
from fund.website.sbi_bank import SBIBank
from fund.website.sbi_securities import SBISecurities


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
        binder.bind(settings.RAKUTEN_BANK, RakutenBank)
        binder.bind(settings.SBI_BANK, SBIBank)
        binder.bind(settings.DC, DCBank)

    def resolve(self, cls) -> IWebSite:
        # injector.get()に引数を渡すと依存関係を解決してインスタンスを生成する
        return self.injector.get(cls)
