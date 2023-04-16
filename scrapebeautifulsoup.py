# BeautifulSoup4を使用したスクレイピング
import bs4
import requests


class ScrapeBeautifulSoup:
    @property
    def parsedhtml(self):
        if self.__parsedhtml is None:
            return None
        return self.__parsedhtml

    def __init__(self, url: str, html=None):
        if html is None:
            res = requests.get(url)
            res.raise_for_status()
            self.__parsedhtml = bs4.BeautifulSoup(res.content, "html.parser")
        else:
            self.__parsedhtml = bs4.BeautifulSoup(html, "html.parser")

    def select_one(self, cssselector: str):
        if self.__parsedhtml is None:
            raise ValueError("error-__parsedhtml is None.")

        element = self.__parsedhtml.select_one(cssselector)
        if element is None:
            raise ValueError("error-cssselector is None")

        return element
