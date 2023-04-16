import threading
import unittest
from http.server import HTTPServer, SimpleHTTPRequestHandler

import settings
from fund.wealthadvisor import WealthAdvisor
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
        wealthadvisor = WealthAdvisor()
        scrapebs = scrapebeautifulsoup(self.url)
        name = wealthadvisor.get_name(scrapebs)
        self.assertEquals(name, "eMAXIS Slim全世界株式(オール･カントリー)")

    def test_get_company(self):
        wealthadvisor = WealthAdvisor()
        scrapebs = scrapebeautifulsoup(self.url)
        company = wealthadvisor.get_company(scrapebs)
        self.assertEquals(company, "投信会社名：三菱UFJ国際投信")

    def test_get_category(self):
        wealthadvisor = WealthAdvisor()
        scrapebs = scrapebeautifulsoup(self.url)
        category = wealthadvisor.get_category(scrapebs)
        self.assertEquals(category, "国際株式・グローバル・含む日本（F）")

    def test_get_baseprice(self):
        wealthadvisor = WealthAdvisor()
        scrapebs = scrapebeautifulsoup(self.url)
        baseprice = wealthadvisor.get_baseprice(scrapebs)
        self.assertEquals(baseprice, "17,375")

    def test_get_allotment(self):
        wealthadvisor = WealthAdvisor()
        scrapebs = scrapebeautifulsoup(self.url)
        allotments = wealthadvisor.get_allotments(scrapebs)
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
        wealthadvisor = WealthAdvisor()
        scrapebs = scrapebeautifulsoup(self.url)
        commision = wealthadvisor.get_commision(scrapebs)
        self.assertEquals(commision, "0円")

    def test_get_cost(self):
        wealthadvisor = WealthAdvisor()
        scrapebs = scrapebeautifulsoup(self.url)
        cost = wealthadvisor.get_cost(scrapebs)
        self.assertEquals(cost, "0.11%")

    def test_get_assets(self):
        wealthadvisor = WealthAdvisor()
        scrapebs = scrapebeautifulsoup(self.url)
        assets = wealthadvisor.get_assets(scrapebs)
        self.assertEquals(assets, "1,001,749百万円")

    def tearDown(self):
        # Use unittest tearDown method.
        self.server.shutdown()
        self.thread.join()
