# BeautifulSoup4を使用したスクレイピング
import bs4
import requests


class ScrapeBeautifulSoup:
    @property
    def parsedhtml(self):
        if self.__parsedhtml is None:
            return None
        return self.__parsedhtml

    def __init__(self):
        self.__parsedhtml = None

    def get_html(self, url: str):
        res = requests.get(url)
        res.raise_for_status()
        self.__parsedhtml = bs4.BeautifulSoup(res.content, "html.parser")

    def select_one(self, cssselector: str) -> str:
        # name,category,commisionはこのメソッドで取得できる
        if self.__parsedhtml is None:
            raise ValueError("error-__parsedhtml is None.")

        element = self.__parsedhtml.select_one(cssselector)
        if element is None:
            raise ValueError("error-cssselector is None")

        return element.text

    def get_company(self, cssselector: str) -> str:
        if self.__parsedhtml is None:
            raise ValueError("error-__parsedhtml is None.")

        table = self.__parsedhtml.select(cssselector)
        if table is None:
            raise ValueError("error-cssselector is None")

        cols = table[1].find_all("td")
        return cols[0].text

    def get_baseprice(self, cssselector: str) -> str:
        if self.__parsedhtml is None:
            raise ValueError("error-__parsedhtml is None.")

        table = self.__parsedhtml.select(cssselector)
        if table is None:
            raise ValueError("error-cssselector is None")

        element = table[0].select_one(".doc-yen-01")
        if element is None:
            raise ValueError("error-.doc-yen-01 is None")

        return "{}{}".format(element.text, element.nextSibling)

    def get_assets(self, cssselector: str) -> str:
        if self.__parsedhtml is None:
            raise ValueError("error-__parsedhtml is None.")

        table = self.__parsedhtml.select(cssselector)
        if table is None:
            raise ValueError("error-cssselector is None")

        cols = table[1].find_all("td")
        return cols[1].text

    def get_allotment(self, cssselector: str) -> int:
        if self.__parsedhtml is None:
            raise ValueError("error-__parsedhtml is None.")

        table = self.__parsedhtml.select(cssselector)
        if table is None:
            raise ValueError("error-cssselector is None")

        cols = table[0].find_all("td")
        value = str(cols[2].text).replace("円", "")
        if value.isdecimal():
            return int(value)
        else:
            raise ValueError("error-allotment")

    def get_cost(self, cssselector: str) -> str:
        if self.__parsedhtml is None:
            raise ValueError("error-__parsedhtml is None.")

        costs = self.__parsedhtml.select_one(cssselector)
        if costs is None:
            raise ValueError("error-cssselector is None")

        element = costs.find("td")
        if element is None:
            raise ValueError("error-cost")

        return element.text
