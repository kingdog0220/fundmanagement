# BeautifulSoup4を使用したスクレイピング
import bs4
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager


class ScrapeBeautifulSoup:
    @property
    def parsedhtml(self):
        if self.__parsedhtml is None:
            return None
        return self.__parsedhtml

    def __init__(self, url: str):
        # ヘッドレスモードで起動
        options = Options()
        options.add_argument("--headless")
        # 常に最新バージョンのChromeDriverをダウンロードして自動的に使用
        driver = webdriver.Chrome(
            ChromeDriverManager().install(), chrome_options=options
        )
        driver.get(url)
        wait = WebDriverWait(driver, 10)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#graph21 div")))
        rendered_html = driver.page_source
        driver.quit()

        self.__parsedhtml = bs4.BeautifulSoup(rendered_html, "html.parser")

    def select_one(self, cssselector: str):
        if self.__parsedhtml is None:
            raise ValueError("error-__parsedhtml is None.")

        element = self.__parsedhtml.select_one(cssselector)
        if element is None:
            raise ValueError("error-cssselector is None")

        return element

    def get_name(self, cssselector: str) -> str:
        return self.select_one(cssselector).text

    def get_company(self, cssselector: str) -> str:
        return self.select_one(cssselector).text

    def get_category(self, cssselector: str) -> str:
        return self.select_one(cssselector).text

    def get_baseprice(self, cssselector: str) -> str:
        return self.select_one(cssselector).text

    def get_allotments(self, cssselector: str) -> list:
        element = self.select_one(cssselector)
        my_td = element.find_all("td")
        # 分配金履歴を返却。分配日と分配金額で1セット
        values = []
        for value in my_td:
            values.append(value.text)
        return values

    def get_commision(self, cssselector: str) -> str:
        element = self.select_one(cssselector)
        my_td = element.find_all("td")
        # 5行目が買付手数料
        return my_td[4].text

    def get_cost(self, cssselector: str) -> str:
        element = self.select_one(cssselector)
        my_div = element.find_all("div")
        # 2つ目の要素が信託報酬率
        value = my_div[3].text.strip()
        return value

    def get_assets(self, cssselector: str) -> str:
        return self.select_one(cssselector).text
