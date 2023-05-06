import datetime
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import settings
from fund.iwebsite import IWebSite
from scrapebeautifulsoup import ScrapeBeautifulSoup as scrapebeautifulsoup
from seleniumlauncher import SeleniumLauncher


class MUFJBank(IWebSite):
    # ログイン状態を表すフラグ
    __isLogin: bool

    @property
    def isLogin(self):
        return self.__isLogin

    def __init__(self):
        self.__isLogin = False

    def login(self):
        """サイトにログインする"""
        if self.__isLogin:
            return

        url = settings.MUFJ_LOGIN_URL
        driver = SeleniumLauncher()
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "tx-contract-number")))
        # ログイン情報を入力
        contract_number = driver.find_element(By.ID, "tx-contract-number")
        password = driver.find_element(By.ID, "tx-ib-password")

        contract_number.send_keys(settings.MUFJ_CONTRACT_NUMBER)
        password.send_keys(settings.MUFJ_PASSWORD)

        login_button = driver.find_element(By.CLASS_NAME, "gonext")
        login_button.click()
        self.__isLogin = True

    def get_account_info(self, account_code: str) -> dict:
        """口座情報を取得する"""
        account_info_dic = self.get_amount(account_code, True)
        return account_info_dic

    def logout(self):
        """ログアウトする"""
        if self.__isLogin:
            driver = SeleniumLauncher()
            wait = WebDriverWait(driver, 10)
            wait.until(
                EC.presence_of_element_located(
                    (By.XPATH, "/html/body/div/header/nav/div[2]/a[2]")
                )
            )
            button = driver.find_element(
                By.XPATH, "/html/body/div/header/nav/div[2]/a[2]"
            )
            button.click()
            self.__isLogin = False
            # 待機
            time.sleep(3)

    def get_amount(self, account_code: str, logout_required: bool) -> dict:
        """口座情報を取得する

        Args:
            logout_required (bool): 処理終了後、ログアウトする場合はtrue

        Returns:
            dict: 口座情報のディクショナリ
        """
        if not self.__isLogin:
            self.login()

        driver = SeleniumLauncher()
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located((By.CLASS_NAME, "total-amount-unmask"))
        )
        scrapebs = scrapebeautifulsoup(driver.current_url, driver.page_source)
        amount = scrapebs.select_one(".total-amount-unmask")
        # データの設定
        account_info_dic = {
            settings.ACCOUNT_CODE: account_code,
            settings.AMOUNT: amount.text,
            settings.UPDATE_DATE: "{0:%Y/%m/%d}".format(datetime.datetime.now()),
        }

        if logout_required:
            self.logout()
        return account_info_dic
