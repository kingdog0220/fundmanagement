# BeautifulSoup4を使用したスクレイピング
import bs4
import requests


class ScrapeBeautifulSoup:
    """BeautifulSoupによるスクレイピングをカスタマイズ"""

    @property
    def parsedhtml(self):
        if self.__parsedhtml is None:
            return None
        return self.__parsedhtml

    def __init__(self, url: str, html=None):
        """BeautifulSoupでhtmlをパースする初期設定

        Args:
            url (str): 解析するサイトのURL
            html (_type_, optional): 解析するサイトのhtml. Defaults to None.
        """
        if html is None:
            res = requests.get(url)
            res.raise_for_status()
            self.__parsedhtml = bs4.BeautifulSoup(res.content, "html.parser")
        else:
            self.__parsedhtml = bs4.BeautifulSoup(html, "html.parser")

    def select_one(self, cssselector: str):
        """要素の取得

        Args:
            cssselector (str): CSSセレクタやタグ名

        Raises:
            ValueError: html解析エラー
            ValueError: CSSセレクタやタグが取得できない

        Returns:
            _type_: 要素
        """
        if self.__parsedhtml is None:
            raise ValueError("error-__parsedhtml is None.")

        element = self.__parsedhtml.select_one(cssselector)
        if element is None:
            raise ValueError("error-cssselector is None")

        return element
