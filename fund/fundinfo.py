# 投資信託情報クラス
class FundInfo:

    # 商品名
    @property
    def name(self):
        return self.__name

    # 運用会社
    @property
    def company(self):
        return self.__company

    # 分類
    @property
    def category(self):
        return self.__category

    # 基準価額
    @property
    def baseprice(self):
        return self.__baseprice

    # 基準日
    @property
    def basedate(self):
        return self.__basedate

    # 直近分配金
    @property
    def allotment(self):
        return self.__allotment

    # 買付手数料
    @property
    def commision(self):
        return self.__commision

    # 信託報酬等の管理費
    @property
    def cost(self):
        return self.__cost

    # 純資産
    @property
    def assets(self):
        return self.__assets

    def __init__(
        self,
        name,
        company,
        category,
        baseprice,
        basedate,
        allotment,
        commision,
        cost,
        assets,
    ):
        self.__name = name
        self.__company = company
        self.__category = category
        self.__baseprice = baseprice
        self.__basedate = basedate
        self.__allotment = allotment
        self.__commision = commision
        self.__cost = cost
        self.__assets = assets
