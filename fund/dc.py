import datetime
import time

from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import settings
from fund.iwebsite import IWebSite
from seleniumlauncher import SeleniumLauncher


class DCBank(IWebSite):
    """DC(りそな銀行)のサイト"""

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

        url = settings.DC_LOGIN_URL
        driver = SeleniumLauncher()
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "navTop")))
        # ユーザー名とパスワードを入力
        login_id = driver.find_element(
            By.XPATH,
            "//*[@id=" + '"navTop"' + "]/div[2]/div[2]/div/div/form/p[1]/input",
        )
        password = driver.find_element(
            By.XPATH,
            "//*[@id=" + '"navTop"' + "]/div[2]/div[2]/div/div/form/p[2]/input",
        )

        login_id.send_keys(settings.DC_LOGIN_ID)
        password.send_keys(settings.DC_LOGIN_PASSWORD)

        login_button = driver.find_element(
            By.XPATH,
            "//*[@id=" + '"navTop"' + "]/div[2]/div[2]/div/div/form/p[3]/input",
        )
        login_button.click()
        # 待機
        time.sleep(3)
        self.__isLogin = True

    def get_account_info_dic(self, account_code: str) -> dict:
        """口座情報を取得する

        Args:
            account_code (str): アカウントコード

        Returns:
            dict: 口座情報
        """
        account_info_dic = self.get_account(account_code)
        return account_info_dic

    def logout(self):
        """ログアウトする"""
        if self.__isLogin:
            driver = SeleniumLauncher()
            button = driver.find_element(
                By.XPATH,
                "//*[@id=" + '"headerGlobal"' + "]/div[2]/ul/li[3]/a",
            )
            button.click()
            # 待機
            time.sleep(3)

    def get_account(self, account_code: str) -> dict:
        """口座情報を取得する

        Args:
            account_code (str): アカウントコード

        Returns:
            dict: 口座情報
        """
        if not self.__isLogin:
            self.login()

        driver = SeleniumLauncher()
        wait = WebDriverWait(driver, 10)
        # 適当な位置をクリックしてお知らせを消す
        ActionChains(driver).move_by_offset(1, 1).click().perform()
        wait.until(EC.presence_of_element_located((By.ID, "DB_EVALUTION_KINGAKU_3")))
        amount = driver.find_element(By.ID, "DB_EVALUTION_KINGAKU_3").text
        # データの設定
        account_info_dic = {
            settings.ACCOUNT_CODE: account_code,
            settings.AMOUNT: amount,
            settings.UPDATE_DATE: "{0:%Y/%m/%d}".format(datetime.datetime.now()),
        }
        return account_info_dic
