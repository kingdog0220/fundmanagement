import settings
from fund.fundinfo import FundInfo
from scrapebeautifulsoup import ScrapeBeautifulSoup as scrapebeautifulsoup


class MorningStar:
    # 名称
    @property
    def css_selector_name(self):
        return ".fundname"

    # 会社
    @property
    def css_selector_comp(self):
        return ".comp"

    # 分類
    @property
    def css_selector_category(self):
        return ".fcate"

    # 基準価額
    @property
    def css_selector_baseprice(self):
        return ".fprice"

    # 直近分配金
    @property
    def css_selector_allotment(self):
        return ".table5b"

    # 買付手数料
    @property
    def css_selector_commision(self):
        return ".table1b"

    # 管理費用率
    @property
    def css_selector_cost(self):
        return "#graph21"

    # 純資産
    @property
    def css_selector_assets(self):
        return ".price2"

    def get_fundinfolist(self):
        url_list = [
            settings.NISSAY_TOPIX_URL,
            settings.TAWARA_DEVELOPED_COUNTRY_URL,
            settings.E_MAXIS_SLIM_EMERGING_URL,
            settings.E_MAXIS_SLIM_SP500_URL,
        ]

        fundinfolist = []
        for url in url_list:
            scrapebs = scrapebeautifulsoup(url)
            name = scrapebs.get_name(self.css_selector_name)
            company = scrapebs.get_company(self.css_selector_comp)
            category = scrapebs.get_category(self.css_selector_category)
            baseprice = scrapebs.get_baseprice(self.css_selector_baseprice)
            allotments = scrapebs.get_allotments(self.css_selector_allotment)
            commision = scrapebs.get_commision(self.css_selector_commision)
            cost = scrapebs.get_cost(self.css_selector_cost)
            assets = scrapebs.get_assets(self.css_selector_assets)
            # 加工が必要な項目（会社、分配金、純資産）
            company_alt = company.replace("投信会社名：", "")
            allotment_alt = allotments[1]
            assets_alt = self.convert_to_billion(assets)
            fundinfo = FundInfo(
                name,
                company_alt,
                category,
                baseprice + "円",
                allotment_alt,
                commision,
                cost,
                assets_alt,
            )
            fundinfolist.append(fundinfo)
        return fundinfolist

    def convert_to_billion(self, value: str) -> float:
        new_str_value = value.replace("百万円", "").replace(",", "")
        try:
            new_value = int(new_str_value) / 10000
            return round(float(new_value), 2)
        except ValueError:
            raise ValueError("error-convert_to_billion method is ValueError")
