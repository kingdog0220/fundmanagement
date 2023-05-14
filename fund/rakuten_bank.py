import datetime

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import settings
from fund.iwebsite import IWebSite
from seleniumlauncher import SeleniumLauncher


class RakutenBank(IWebSite):
    """楽天銀行のサイト"""

    # ログイン状態を表すフラグ
    __is_login: bool

    @property
    def is_login(self):
        return self.__is_login

    def __init__(self):
        self.__is_login = False

    def login(self):
        """サイトにログインする"""
        if self.__is_login:
            return

        url = settings.RAKUTEN_BANK_LOGIN_URL
        driver = SeleniumLauncher()
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        # 最大化しないと要素が特定できない
        driver.maximize_window()
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "//*[@id="
                    + '"main-contents"'
                    + "]/header/header/div[1]/div/div/div[2]/ul/li[5]/a[1]",
                )
            )
        )
        button = driver.find_element(
            By.XPATH,
            "//*[@id="
            + '"main-contents"'
            + "]/header/header/div[1]/div/div/div[2]/ul/li[5]/a[1]",
        )
        button.click()
        # 別ウィンドウが開く
        WebDriverWait(driver, 3).until(lambda d: len(d.window_handles) > 1)
        driver.switch_to.window(driver.window_handles[1])

        wait.until(EC.presence_of_element_located((By.ID, "LOGIN")))
        # ユーザー名とパスワードを入力
        login_id = driver.find_element(By.ID, "LOGIN:USER_ID")
        password = driver.find_element(By.ID, "LOGIN:LOGIN_PASSWORD")

        login_id.send_keys(settings.RAKUTEN_BANK_LOGIN_ID)
        password.send_keys(settings.RAKUTEN_BANK_PASSWORD)

        login_button = driver.find_element(By.ID, "LOGIN:_idJsp43")
        login_button.click()

        self.__is_login = True

    def get_account(self, account_code: str) -> dict:
        """口座情報を取得する

        Args:
            account_code (str): アカウントコード

        Returns:
            dict: 口座情報
        """
        account_info_dic = self.get_account_dic(account_code)
        return account_info_dic

    def logout(self):
        """ログアウトする"""
        if self.__is_login:
            driver = SeleniumLauncher()
            wait = WebDriverWait(driver, 10)
            button = driver.find_element(
                By.ID,
                "HEADER:j_id_u6",
            )
            button.click()
            wait.until(
                EC.presence_of_element_located((By.ID, "LOGOUT_COMFIRM:_idJsp19"))
            )
            confirm_button = driver.find_element(
                By.ID,
                "LOGOUT_COMFIRM:_idJsp19",
            )
            confirm_button.click()
            self.__is_login = False
            wait.until(EC.presence_of_element_located((By.ID, "str-main")))
            close_button = driver.find_element(
                By.XPATH,
                "//*[@id=" + '"str-main"' + "]/p[8]/input",
            )
            # ウインドウを閉じて最初のウインドウに戻す
            close_button.click()
            driver.switch_to.window(driver.window_handles[0])

    def get_account_dic(self, account_code: str) -> dict:
        """口座情報を取得する

        Args:
            account_code (str): アカウントコード

        Returns:
            dict: 口座情報
        """
        if not self.__is_login:
            self.login()

        driver = SeleniumLauncher()
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.ID, "lyt-deposit")))
        driver.maximize_window()
        amount = driver.find_element(
            By.XPATH,
            "//*[@id="
            + '"lyt-deposit"'
            + "]/div/div[2]/div/div[3]/div[1]/table/tbody/tr/td/span[1]",
        ).text
        # データの設定
        account_info_dic = {
            settings.ACCOUNT_CODE: account_code,
            settings.AMOUNT: amount,
            settings.UPDATE_DATE: "{0:%Y/%m/%d}".format(datetime.datetime.now()),
        }
        return account_info_dic
