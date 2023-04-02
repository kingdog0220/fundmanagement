from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import auth
import settings
from fund.fundinfo import FundInfo
from scrapebeautifulsoup import ScrapeBeautifulSoup as scrapebeautifulsoup
from seleniumlauncher import SeleniumLauncher


class RakutenSecurities:

    # 名称
    @property
    def css_selector_name(self):
        return ".fund-name"

    # 分類
    @property
    def css_selector_category(self):
        return ".fund-type"

    # 純資産
    @property
    def css_selector_assets(self):
        return ".tbl-fund-summary"

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

        fundinfolist = []
        for url in url_list:
            scrapebs = scrapebeautifulsoup(url)
            name = scrapebs.get_name(self.css_selector_name)
            company = scrapebs.get_company(self.css_selector_tbl_data)
            category = scrapebs.get_category(self.css_selector_category)
            baseprice = scrapebs.get_baseprice(self.css_selector_tbl_data)
            assets = scrapebs.get_assets(self.css_selector_assets)
            allotment = scrapebs.get_allotment(self.css_selector_tbl_data)
            commision = scrapebs.get_commision(self.css_selector_commision)
            cost = scrapebs.get_cost(self.css_selector_cost)
            fundinfo = FundInfo(
                name, company, category, baseprice, assets, allotment, commision, cost
            )
            fundinfolist.append(fundinfo)
        return fundinfolist

    def Login(self):
        url = settings.RAKUTEN_LOGIN_URL
        driver = SeleniumLauncher()
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "s3-form-login__login"))
        )
        # ユーザー名とパスワードを入力
        login_id = driver.find_element(By.ID, "form-login-id")
        password = driver.find_element(By.ID, "form-login-pass")

        login_id.send_keys(auth.RAKUTEN_LOGIN_ID)
        password.send_keys(auth.RAKUTEN_PASSWORD)

        login_button = driver.find_element(By.ID, "login-btn")
        login_button.click()
