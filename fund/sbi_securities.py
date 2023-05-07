import datetime
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import settings
from fund.iwebsite import IWebSite
from seleniumlauncher import SeleniumLauncher


class SBISecurities(IWebSite):
    """SBI証券のサイト"""

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

        url = settings.SBI_LOGIN_URL
        driver = SeleniumLauncher()
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "user_input")))
        # ユーザー名とパスワードを入力
        login_id = driver.find_element(By.NAME, "user_id")
        password = driver.find_element(By.NAME, "user_password")

        login_id.send_keys(settings.SBI_LOGIN_ID)
        password.send_keys(settings.SBI_PASSWORD)

        login_button = driver.find_element(By.CLASS_NAME, "sb-position-c")
        login_button.click()

        # とりあえず待機
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id=" + '"my-assets-button"' + "]/img")
            )
        )
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
                By.ID,
                "logoutM",
            )
            button.click()
            # 待機
            time.sleep(3)
            self.__isLogin = False

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
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id=" + '"my-assets-button"' + "]/img")
            )
        )
        button = driver.find_element(
            By.XPATH, "//*[@id=" + '"my-assets-button"' + "]/img"
        )
        button.click()

        # 新しいタブが開く
        first_tab_handle = driver.current_window_handle
        new_tab_handle = driver.window_handles[-1]
        driver.switch_to.window(new_tab_handle)
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id=" + '"balance"' + "]/ul")
            )
        )
        # 外賀建MMF
        mmf_element_link = driver.find_element(
            By.XPATH, "//*[@id=" + '"balance"' + "]/ul/li[2]/div[1]/div[1]/div/a"
        )
        mmf_element_link.click()

        wait.until(EC.presence_of_element_located((By.ID, "summary_USD")))
        quantity = driver.find_element(
            By.XPATH, "//*[@id=" + '"summary_USD"' + "]/td[3]/table/tbody/tr[1]/td[2]/b"
        )
        amount = driver.find_element(
            By.XPATH, "//*[@id=" + '"summary_USD"' + "]/td[3]/table/tbody/tr[2]/td[2]/b"
        )
        # タブを閉じて最初のタブへ
        driver.close()
        driver.switch_to.window(first_tab_handle)
        # データの設定
        account_info_dic = {
            settings.ACCOUNT_CODE: account_code,
            settings.AMOUNT: amount.text,
            settings.QUANTITY: quantity.text,
            settings.UPDATE_DATE: "{0:%Y/%m/%d}".format(datetime.datetime.now()),
        }
        return account_info_dic
