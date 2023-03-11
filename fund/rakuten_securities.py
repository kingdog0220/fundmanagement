from fundinfo import FundInfo

import settings
from scrapebeautifulsoup import ScrapeBeautifulSoup as scrapebeautifulsoup


class RakutenSecurities:

    # 名称
    @property
    def css_selector_name(self):
        return ".fund-name"

    # 分類
    @property
    def css_selector_category(self):
        return ".fund-type"

    # 買付手数料
    @property
    def css_selector_commision(self):
        return ".no-fee"

    # 信託報酬等の管理費
    @property
    def css_selector_cost(self):
        return ".trust-fee"

    # その他の項目
    @property
    def css_selector_tbl_data(self):
        return ".tbl-data-01"

    def get_fundinfolist(self) -> list:
        url_list = [
            settings.NISSAY_TOPIX_URL,
            settings.TAWARA_DEVELOPED_COUNTRY_URL,
            settings.E_MAXIS_SLIM_EMERGING_URL,
            settings.E_MAXIS_SLIM_SP500_URL,
        ]
        scrapebs = scrapebeautifulsoup()
        fundinfolist = []
        for url in url_list:
            scrapebs.get_html(url)
            name = scrapebs.select_one(self.css_selector_name)
            company = scrapebs.get_company(self.css_selector_tbl_data)
            category = scrapebs.select_one(self.css_selector_category)
            baseprice = scrapebs.get_baseprice(self.css_selector_tbl_data)
            assets = scrapebs.get_assets(self.css_selector_tbl_data)
            allotment = scrapebs.get_allotment(self.css_selector_tbl_data)
            commision = scrapebs.select_one(self.css_selector_commision)
            cost = scrapebs.get_cost(self.css_selector_cost)
            fundinfo = FundInfo(
                name, company, category, baseprice, assets, allotment, commision, cost
            )
            fundinfolist.append(fundinfo)
        return fundinfolist
