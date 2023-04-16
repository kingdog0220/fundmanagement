from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import settings
from fund.fundinfo import FundInfo
from scrapebeautifulsoup import ScrapeBeautifulSoup as scrapebeautifulsoup
from seleniumlauncher import SeleniumLauncher


class WealthAdvisor:
    def get_fundinfolist(self) -> list:
        url_list = [
            settings.NISSAY_TOPIX_URL,
            settings.TAWARA_DEVELOPED_COUNTRY_URL,
            settings.E_MAXIS_SLIM_EMERGING_URL,
            settings.E_MAXIS_SLIM_SP500_URL,
        ]

        driver = SeleniumLauncher()
        fundinfolist = []
        for url in url_list:
            driver.get(url)
            wait = WebDriverWait(driver, 10)
            wait.until(
                # 信託報酬のレンダリング待ち
                EC.presence_of_element_located((By.CSS_SELECTOR, "#graph21 div"))
            )
            scrapebs = scrapebeautifulsoup(driver.current_url, driver.page_source)
            name = self.get_name(scrapebs)
            company = self.get_company(scrapebs)
            category = self.get_category(scrapebs)
            baseprice = self.get_baseprice(scrapebs)
            basedate = self.get_basedate(scrapebs)
            allotments = self.get_allotments(scrapebs)
            commision = self.get_commision(scrapebs)
            cost = self.get_cost(scrapebs)
            assets = self.get_assets(scrapebs)
            # 加工が必要な項目（会社、基準価額、分配金、純資産）
            company_alt = company.replace("投信会社名：", "")
            baseprice_alt = baseprice + "円"
            allotment_alt = allotments[1]
            assets_alt = self.convert_to_billion(assets)
            fundinfo = FundInfo(
                name,
                company_alt,
                category,
                baseprice_alt,
                basedate,
                allotment_alt,
                commision,
                cost,
                assets_alt,
            )
            fundinfolist.append(fundinfo)
        return fundinfolist

    def get_name(self, scrapebs: scrapebeautifulsoup) -> str:
        return scrapebs.select_one(".fundname").text

    def get_company(self, scrapebs: scrapebeautifulsoup) -> str:
        return scrapebs.select_one(".comp").text

    def get_category(self, scrapebs: scrapebeautifulsoup) -> str:
        return scrapebs.select_one(".fcate").text

    def get_baseprice(self, scrapebs: scrapebeautifulsoup) -> str:
        return scrapebs.select_one(".fprice").text

    def get_basedate(self, scrapebs: scrapebeautifulsoup) -> str:
        # ptdateは2つあるが最初の1つ目が欲しい情報なのでこれでOK
        return scrapebs.select_one(".ptdate").text

    def get_allotments(self, scrapebs: scrapebeautifulsoup) -> list:
        element = scrapebs.select_one(".table5b")
        my_td = element.find_all("td")
        # 分配金履歴を返却。分配日と分配金額で1セット
        values = []
        for value in my_td:
            values.append(value.text)
        return values

    def get_commision(self, scrapebs: scrapebeautifulsoup) -> str:
        element = scrapebs.select_one(".table1b")
        my_td = element.find_all("td")
        # 5行目が買付手数料
        return my_td[4].text

    def get_cost(self, scrapebs: scrapebeautifulsoup) -> str:
        element = scrapebs.select_one("#graph21")
        my_div = element.find_all("div")
        # 2つ目の要素が信託報酬率
        value = my_div[3].text.strip()
        return value

    def get_assets(self, scrapebs: scrapebeautifulsoup) -> str:
        return scrapebs.select_one(".price2").text

    def convert_to_billion(self, value: str) -> float:
        new_str_value = value.replace("百万円", "").replace(",", "")
        try:
            new_value = int(new_str_value) / 100
            return round(float(new_value), 2)
        except ValueError:
            raise ValueError("error-convert_to_billion method is ValueError")
