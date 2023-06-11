# BeautifulSoup4を使用したスクレイピング
import bs4


class ScrapeBeautifulSoup:
    """BeautifulSoupによるスクレイピングをカスタマイズ"""

    @property
    def parsedhtml(self):
        if self.__parsedhtml is None:
            return None
        return self.__parsedhtml

    def __init__(self, html):
        """BeautifulSoupインスタンスの生成

        Args:
            html (_type_): パースするHTML

        Raises:
            bs4.FeatureNotFound: パースできなかった場合
        """
        try:
            self.__parsedhtml = bs4.BeautifulSoup(html, "html.parser")
        except bs4.FeatureNotFound:
            raise

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
            raise ValueError(
                "error-select_one cssselector:{0} is None".format(cssselector)
            )

        return element
