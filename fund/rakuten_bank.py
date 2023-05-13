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

        self.__isLogin = True

    def get_account_info_dic(self, account_code: str) -> dict:
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

    def logout(self):
        """ログアウトする"""
        if self.__isLogin:
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
            self.__isLogin = False
            wait.until(EC.presence_of_element_located((By.ID, "str-main")))
            close_button = driver.find_element(
                By.XPATH,
                "//*[@id=" + '"str-main"' + "]/p[8]/input",
            )
            # ウインドウが閉じられる
            close_button.click()
