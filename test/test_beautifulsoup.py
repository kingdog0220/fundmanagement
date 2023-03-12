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
    def setUp(self):
        # Use unittest setUp method.
        self.server = StoppableHTTPServer((HOST, PORT), SimpleHTTPRequestHandler)
        self.url = "http://{}:{}/test/test_case/test.html".format(HOST, PORT)
        self.thread = threading.Thread(None, self.server.run)
        self.thread.start()

    @unittest.skip("本番サイトの構成が変わったかもしれないときに実行")
    def test_get_html(self):
        scrapebs = scrapebeautifulsoup(settings.NISSAY_TOPIX_URL)
        if scrapebs.parsedhtml is None:
            print("Target URL is None.")
        print(scrapebs.parsedhtml)

    def test_get_name(self):
        scrapebs = scrapebeautifulsoup(self.url)
        name = scrapebs.get_name(".fund-name")
        self.assertEquals(name, "＜購入・換金手数料なし＞ニッセイＴＯＰＩＸインデックスファンド")

    def test_get_company(self):
        scrapebs = scrapebeautifulsoup(self.url)
        company = scrapebs.get_company(".tbl-data-01")
        self.assertEquals(company, "ニッセイアセットマネジメント")

    def test_get_category(self):
        scrapebs = scrapebeautifulsoup(self.url)
        category = scrapebs.get_category(".fund-type")
        self.assertEquals(category, "国内株式")

    def test_get_baseprice(self):
        scrapebs = scrapebeautifulsoup(self.url)
        baseprice = scrapebs.get_baseprice(".tbl-data-01")
        self.assertEquals(baseprice, "14,664円 （3/10）")

    def test_get_assets(self):
        scrapebs = scrapebeautifulsoup(self.url)
        assets = scrapebs.get_assets(".tbl-fund-summary")
        self.assertEquals(assets, 551.25)

    def test_get_allotment(self):
        scrapebs = scrapebeautifulsoup(self.url)
        allotment = scrapebs.get_allotment(".tbl-data-01")
        self.assertEquals(allotment, 0)

    def test_get_commision(self):
        scrapebs = scrapebeautifulsoup(self.url)
        commision = scrapebs.get_commision(".no-fee")
        self.assertEquals(commision, 0)

    def test_get_cost(self):
        scrapebs = scrapebeautifulsoup(self.url)
        cost = scrapebs.get_cost(".trust-fee")
        self.assertEquals(cost, "0.154％")

    def tearDown(self):
        # Use unittest tearDown method.
        self.server.shutdown()
        self.thread.join()
