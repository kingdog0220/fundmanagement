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
        name = scrapebs.get_name(".fundname")
        self.assertEquals(name, "eMAXIS Slim全世界株式（オール･カントリー）")

    def test_get_company(self):
        scrapebs = scrapebeautifulsoup(self.url)
        company = scrapebs.get_company(".comp")
        self.assertEquals(company, "投信会社名：三菱UFJ国際投信")

    def test_get_category(self):
        scrapebs = scrapebeautifulsoup(self.url)
        category = scrapebs.get_category(".fcate")
        self.assertEquals(category, "国際株式・グローバル・含む日本（F）")

    def test_get_baseprice(self):
        scrapebs = scrapebeautifulsoup(self.url)
        baseprice = scrapebs.get_baseprice(".fprice")
        self.assertEquals(baseprice, "16,522")

    def test_get_allotment(self):
        scrapebs = scrapebeautifulsoup(self.url)
        allotment = scrapebs.get_allotment(".table5b")
        self.assertEquals(allotment, "2022年04月25日,0円")

    def test_get_commision(self):
        scrapebs = scrapebeautifulsoup(self.url)
        commision = scrapebs.get_commision(".table1b")
        self.assertEquals(commision, "0円")

    def test_get_cost(self):
        scrapebs = scrapebeautifulsoup(self.url)
        cost = scrapebs.get_cost("#graph21")
        self.assertEquals(cost, "0.11%")

    def test_get_assets(self):
        scrapebs = scrapebeautifulsoup(self.url)
        assets = scrapebs.get_assets(".price2")
        self.assertEquals(assets, "914,754百万円")

    def tearDown(self):
        # Use unittest tearDown method.
        self.server.shutdown()
        self.thread.join()
