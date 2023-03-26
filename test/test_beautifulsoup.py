import threading
import unittest
from http.server import HTTPServer, SimpleHTTPRequestHandler

import settings
from scrape import Scrape as scrape

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
        scraped = scrape(settings.NISSAY_TOPIX_URL)
        if scraped.parsedhtml is None:
            print("Target URL is None.")
        print(scraped.parsedhtml)

    def test_get_name(self):
        scraped = scrape(self.url)
        name = scraped.get_name(".fundname")
        self.assertEquals(name, "eMAXIS Slim全世界株式（オール･カントリー）")

    def test_get_company(self):
        scraped = scrape(self.url)
        company = scraped.get_company(".comp")
        self.assertEquals(company, "投信会社名：三菱UFJ国際投信")

    def test_get_category(self):
        scraped = scrape(self.url)
        category = scraped.get_category(".fcate")
        self.assertEquals(category, "国際株式・グローバル・含む日本（F）")

    def test_get_baseprice(self):
        scraped = scrape(self.url)
        baseprice = scraped.get_baseprice(".fprice")
        self.assertEquals(baseprice, "16,522")

    def test_get_basedate(self):
        scraped = scrape(self.url)
        baseprice = scraped.get_baseprice(".ptdate")
        self.assertEquals(baseprice, "2023年03月17日")

    def test_get_allotment(self):
        scraped = scrape(self.url)
        allotments = scraped.get_allotments(".table5b")
        expects = [
            "2022年04月25日",
            "0円",
            "2021年04月26日",
            "0円",
            "2020年04月27日",
            "0円",
            "2019年04月25日",
            "0円",
        ]
        self.assertListEqual(expects, allotments)

    def test_get_commision(self):
        scraped = scrape(self.url)
        commision = scraped.get_commision(".table1b")
        self.assertEquals(commision, "0円")

    def test_get_cost(self):
        scraped = scrape(self.url)
        cost = scraped.get_cost("#graph21")
        self.assertEquals(cost, "0.11%")

    def test_get_assets(self):
        scraped = scrape(self.url)
        assets = scraped.get_assets(".price2")
        self.assertEquals(assets, "914,754百万円")

    def tearDown(self):
        # Use unittest tearDown method.
        self.server.shutdown()
        self.thread.join()
