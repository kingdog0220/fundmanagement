import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.alert import Alert
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import auth
import settings
from fund.fundinfo import FundInfo
from scrapebeautifulsoup import ScrapeBeautifulSoup as scrapebeautifulsoup
from seleniumlauncher import SeleniumLauncher


class RakutenSecurities:
    # ログイン状態を表すフラグ
    __isLogin: bool

    @property
    def isLogin(self):
        return self.__isLogin

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

    def __init__(self):
        self.__isLogin = False

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

    def get_total_return_csv(self, logout_required: bool):
        self.login()
        self.go_to_target_page()
        self.download_total_return_csv()
        if logout_required:
            self.logout()

    def login(self):
        if self.__isLogin:
            return

        self.__isLogin = False
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

        # とりあえず待機
        wait.until(EC.presence_of_element_located((By.ID, "homeAssetsPanel")))
        self.__isLogin = True

    def go_to_target_page(self):
        if not self.__isLogin:
            self.login()

        driver = SeleniumLauncher()
        wait = WebDriverWait(driver, 10)
        # 保有商品一覧
        asset_page = driver.find_element(
            By.XPATH,
            "//*[@id="
            + '"str-container"'
            + "]/div[2]/main/form[2]/div[2]/div[1]/div[1]/div[2]/div[1]/a[1]/span",
        )
        asset_page.click()
        # トータルリターン
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "/html/body/div[1]/div/div[7]/div/ul/li[4]/a/span")
            )
        )
        total_return_page = driver.find_element(
            By.XPATH, "/html/body/div[1]/div/div[7]/div/ul/li[4]/a/span"
        )
        total_return_page.click()
        # 待機
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id="
                    + '"str-main-inner"'
                    + "]/table/tbody/tr/td/form/div[4]/table/tbody/tr/td[2]/a/img",
                )
            )
        )

    def download_total_return_csv(self):
        if not self.__isLogin:
            self.login()
            self.go_to_target_page()

        driver = SeleniumLauncher()
        button = driver.find_element(
            By.XPATH,
            "//*[@id="
            + '"str-main-inner"'
            + "]/table/tbody/tr/td/form/div[4]/table/tbody/tr/td[2]/a/img",
        )
        button.click()
        # 待機
        time.sleep(3)

    def logout(self):
        if self.isLogin:
            driver = SeleniumLauncher()
            button = driver.find_element(
                By.CLASS_NAME,
                "pcm-gl-s-header-logout__btn",
            )
            # 要素を画面内にスクロールする
            button.location_once_scrolled_into_view
            # 要素が表示されるまでスクロールする
            actions = ActionChains(driver)
            actions.move_to_element(button).perform()
            button.click()
            # 待機
            time.sleep(3)
            # ログアウト時のダイアログ
            Alert(driver).accept()
