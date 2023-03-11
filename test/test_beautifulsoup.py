import threading
import unittest
from http.server import HTTPServer, SimpleHTTPRequestHandler

import settings
from scrapebeautifulsoup import ScrapeBeautifulSoup as scrapebeautifulsoup

HOST = "localhost"
PORT = 8888


class StoppableHTTPServer(HTTPServer):
    """
    ThreadでSimpleHTTPServerを動かすためのwrapper class.
    Ctrl + Cで終了されるとThreadだけが死んで残る.
    KeyboardInterruptはpassする.
    """

    def run(self):
        try:
            self.serve_forever()
        except KeyboardInterrupt:
            pass
        finally:
            self.server_close()


class TestWebScraping(unittest.TestCase):

    scrapebs = scrapebeautifulsoup()

    def setUp(self):
        # Use unittest setUp method.
        self.server = StoppableHTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
        self.url = "http://{}:{}/test/test_case/test.html".format(HOST, PORT)
        self.thread = threading.Thread(None, self.server.run)
        self.thread.start()

    @unittest.skip("本番サイトの構成が変わったかもしれないときに実行")
    def test_get_html(self):
        self.scrapebs.get_html(settings.NISSAY_TOPIX_URL)
        if self.scrapebs.parsedhtml is None:
            print("Target URL is None.")

        print(self.scrapebs.parsedhtml)

    def test_select_one(self):
        self.scrapebs.get_html(self.url)
        name = self.scrapebs.select_one(".fund-name")
        self.assertEquals(name, "＜購入・換金手数料なし＞ニッセイＴＯＰＩＸインデックスファンド")

    def test_select_one_company(self):
        self.scrapebs.get_html(self.url)
        company = self.scrapebs.get_company(".tbl-data-01")
        self.assertEquals(company, "ニッセイアセットマネジメント")

    def test_get_baseprice(self):
        self.scrapebs.get_html(self.url)
        baseprice = self.scrapebs.get_baseprice(".tbl-data-01")
        self.assertEquals(baseprice, "14,664円 （3/10）")

    def test_get_assets(self):
        self.scrapebs.get_html(self.url)
        assets = self.scrapebs.get_assets(".tbl-data-01")
        self.assertEquals(assets, "551.25億円")

    def test_get_allotment(self):
        self.scrapebs.get_html(self.url)
        allotment = self.scrapebs.get_allotment(".tbl-data-01")
        self.assertEquals(allotment, 0)

    def test_get_cost(self):
        self.scrapebs.get_html(self.url)
        cost = self.scrapebs.get_cost(".trust-fee")
        self.assertEquals(cost, "0.154％")

    def tearDown(self):
        # Use unittest tearDown method.
        self.server.shutdown()
        self.thread.join()
