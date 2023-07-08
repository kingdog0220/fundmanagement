import datetime
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import settings
from application.seleniumlauncher import SeleniumLauncher
from fund.website.common.iaccount import IAccount
from fund.website.common.iwebsite import IWebSite


class SBISecurities(IWebSite):
    """SBI証券のサイト"""

    # ログイン状態を表すフラグ
    __is_login: bool

    # 口座情報のインスタンス
    __account_instance: IAccount

    @property
    def is_login(self):
        return self.__is_login

    def __init__(self):
        self.__is_login = False

    def login(self):
        """サイトにログインする"""
        if self.__is_login:
            return

        url = str(settings.SBI_LOGIN_URL)
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
        time.sleep(3)
        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id=" + '"navi01P"' + "]/ul/li[1]/a/img")
            )
        )
        home_button = driver.find_element(
            By.XPATH, "//*[@id=" + '"navi01P"' + "]/ul/li[1]/a/img"
        )
        home_button.click()

        wait.until(
            EC.presence_of_element_located(
                (By.XPATH, "//*[@id=" + '"my-assets-button"' + "]/img")
            )
        )
        self.__is_login = True

    def get_account(self, account_code: str) -> dict:
        """口座情報を取得する

        Args:
            account_code (str): アカウントコード

        Returns:
            dict: 口座情報
        """
        if not self.__is_login:
            self.login()
        self.create_account_instance(account_code)
        if self.__account_instance is None:
            raise ValueError(
                "error-SBISecurities account instance {0} is None".format(account_code)
            )
        account_info_dic = self.__account_instance.get_account_dic()
        return account_info_dic

    def logout(self):
        """ログアウトする"""
        if self.__is_login:
            driver = SeleniumLauncher()
            button = driver.find_element(
                By.ID,
                "logoutM",
            )
            button.click()
            # 待機
            time.sleep(3)
            self.__is_login = False

    # ファクトリーメソッド
    def create_account_instance(self, account_code: str):
        """口座情報を取得する具象インスタンスを生成する

        Args:
            account_code (str): アカウントコード

        Raises:
            NotImplementedError: 想定外のアカウントコードが渡された場合
        """
        account_class_dic = {
            settings.SBI_SECURITIES_MMF_ACCOUNT: SBISecuritiesMMF,
            settings.SBI_SECURITIES_FX_ACCOUNT: SBISecuritiesFX,
        }
        account_class = account_class_dic.get(account_code)
        if account_class is None:
            # 不正な値の場合などのデフォルト処理
            raise NotImplementedError()
        self.__account_instance = account_class(account_code)


class SBISecuritiesMMF(IAccount):
    __account_code: str

    def __init__(self, account_code: str):
        self.__account_code = account_code

    def get_account_dic(self) -> dict:
        """口座情報を取得する

        Returns:
            dict: 口座情報
        """
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
        ).text
        amount = driver.find_element(
            By.XPATH, "//*[@id=" + '"summary_USD"' + "]/td[3]/table/tbody/tr[2]/td[2]/b"
        ).text
        # タブを閉じて最初のタブへ
        driver.close()
        driver.switch_to.window(first_tab_handle)
        # データの設定
        account_info_dic = {
            settings.ACCOUNT_CODE: self.__account_code,
            settings.AMOUNT: amount,
            settings.QUANTITY: quantity,
            settings.UPDATE_DATE: "{0:%Y/%m/%d}".format(datetime.datetime.now()),
        }
        return account_info_dic


class SBISecuritiesFX(IAccount):
    __account_code: str

    def __init__(self, account_code: str):
        self.__account_code = account_code

    def get_account_dic(self) -> dict:
        """口座情報を取得する

        Returns:
            dict: 口座情報
        """
        # 外貨預金はないため0で返す
        account_info_dic = {
            settings.ACCOUNT_CODE: self.__account_code,
            settings.AMOUNT: "0",
            settings.QUANTITY: "0",
            settings.UPDATE_DATE: "{0:%Y/%m/%d}".format(datetime.datetime.now()),
        }
        return account_info_dic
