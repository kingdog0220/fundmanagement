# BeautifulSoup4を使用したスクレイピング
import bs4
import requests


class ScrapeBeautifulSoup:
    @property
    def parsedhtml(self):
        if self.__parsedhtml is None:
            return None
        return self.__parsedhtml

    def __init__(self, url: str):
        res = requests.get(url)
        res.raise_for_status()
        self.__parsedhtml = bs4.BeautifulSoup(res.content, "html.parser")

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
        # 直近4回の分配金履歴を返却。分配日と分配金額で1セット
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
        value = my_div[3].text.strip()
        return value

    def get_assets(self, cssselector: str) -> str:
        return self.select_one(cssselector).text
