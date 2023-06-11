import datetime
import time

from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait

import settings
from application.seleniumlauncher import SeleniumLauncher
from fund.website.common.iaccount import IAccount
from fund.website.common.iwebsite import IWebSite


class SBIBank(IWebSite):
    """住信SBI銀行のサイト"""

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

        url = settings.SBI_BANK_URL
        driver = SeleniumLauncher()
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/header/div[3]/a",
                )
            )
        )
        button = driver.find_element(By.XPATH, "/html/body/header/div[3]/a")
        button.click()
        # ユーザー名とパスワードを入力
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/app/div[1]/ng-component/div/main/ng-component/form/section[1]/div/div/ul/li/nb-button-login/button",
                )
            )
        )
        login_id = driver.find_element(By.ID, "userNameNewLogin")
        password = driver.find_element(By.ID, "loginPwdSet")

        login_id.send_keys(settings.SBI_BANK_LOGIN_ID)
        password.send_keys(settings.SBI_BANK_LOGIN_PASSWORD)

        login_button = driver.find_element(
            By.XPATH,
            "/html/body/app/div[1]/ng-component/div/main/ng-component/form/section[1]/div/div/ul/li/nb-button-login/button",
        )
        login_button.click()
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
                "error-SBIBank account instance {0} is None".format(account_code)
            )
        account_info_dic = self.__account_instance.get_account_dic()
        return account_info_dic

    def logout(self):
        """ログアウトする"""
        if self.__is_login:
            driver = SeleniumLauncher()
            button = driver.find_element(
                By.XPATH,
                "/html/body/app/nb-head/header/div[2]/a",
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
            settings.SBI_BANK_ACCOUNT: SBIBankNormalAccount,
            settings.SBI_BANK_FX_ACCOUNT: SBIBankFXAccount,
        }
        account_class = account_class_dic.get(account_code)
        if account_class is None:
            # 不正な値の場合などのデフォルト処理
            raise NotImplementedError()
        self.__account_instance = account_class(account_code)


class SBIBankNormalAccount(IAccount):
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
        # ログイン直後の場合は残高一覧のページへ遷移する
        if len(driver.find_elements(By.CLASS_NAME, "m-zandaka-date")) <= 0:
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "top-hdr-linklist"))
            )
            element = driver.find_element(
                By.XPATH,
                "/html/body/app/div[1]/ng-component/div/main/ng-component/div[3]/nb-gethtml-dynamic[1]/ul/li[2]/a",
            )
            element.click()
        # 残高一覧のページ
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/app/div[1]/ng-component/div/main/ng-component/section[1]",
                )
            )
        )
        amount = driver.find_element(
            By.XPATH,
            "/html/body/app/div[1]/ng-component/div/main/ng-component/section[1]/div/ul/li[1]/h2/a/span[1]/span[1]",
        ).text
        account_info_dic = {
            settings.ACCOUNT_CODE: self.__account_code,
            settings.AMOUNT: amount,
            settings.UPDATE_DATE: "{0:%Y/%m/%d}".format(datetime.datetime.now()),
        }
        return account_info_dic


class SBIBankFXAccount(IAccount):
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
        # ログイン直後の場合は残高一覧のページへ遷移する
        if len(driver.find_elements(By.CLASS_NAME, "m-zandaka-date")) <= 0:
            wait.until(
                EC.presence_of_element_located((By.CLASS_NAME, "top-hdr-linklist"))
            )
            element = driver.find_element(
                By.XPATH,
                "/html/body/app/div[1]/ng-component/div/main/ng-component/div[3]/nb-gethtml-dynamic[1]/ul/li[2]/a",
            )
            element.click()
        # 残高一覧のページ
        wait.until(
            EC.presence_of_element_located(
                (
                    By.XPATH,
                    "/html/body/app/div[1]/ng-component/div/main/ng-component/section[1]",
                )
            )
        )
        amount = driver.find_element(
            By.XPATH,
            "/html/body/app/div[1]/ng-component/div/main/ng-component/section[1]/div/ul/li[3]/h2/a/span[1]/span[1]",
        ).text
        # 展開
        icon = driver.find_element(
            By.XPATH,
            "/html/body/app/div[1]/ng-component/div/main/ng-component/section[1]/div/ul/li[3]/h2/a/span[2]/i[1]",
        )
        icon.click()
        wait.until(EC.presence_of_element_located((By.CLASS_NAME, "m-acdArea_inr")))
        quantity = driver.find_element(
            By.XPATH,
            "/html/body/app/div[1]/ng-component/div/main/ng-component/section[1]/div/ul/li[3]/div/div/div/table/tbody/tr/td[1]/span[1]",
        ).text
        account_info_dic = {
            settings.ACCOUNT_CODE: self.__account_code,
            settings.AMOUNT: amount,
            settings.QUANTITY: quantity,
            settings.UPDATE_DATE: "{0:%Y/%m/%d}".format(datetime.datetime.now()),
        }
        return account_info_dic
