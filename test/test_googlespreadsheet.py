import unittest

from fund.fundinfo import FundInfo
from googlespreadsheet import GoogleSpreadSheet


class TestGoogleSpreadSheet(unittest.TestCase):
    @unittest.skip("個別に実行。書き込まれた結果を実際に確認する")
    def test_write_fundinfolist(self):
        # 前回純資産額となる値は130.2
        fund = FundInfo(
            "日経平均投資信託",
            "大和アセットマネジメント",
            "国内株式",
            "14,500円 （2/27）",
            120.4,
            100,
            200,
            "0.23％",
        )
        googlespreadsheet = GoogleSpreadSheet()
        googlespreadsheet.write_fundinfolist("ファンドテスト", [fund])

    @unittest.skip("個別に実行。書き込まれた結果を実際に確認する")
    def test_write_fundinfolists(self):
        fund1 = FundInfo(
            "日経平均投資信託1",
            "大和アセットマネジメント",
            "国内株式",
            "14,500円 （2/27）",
            120.4,
            100,
            200,
            "0.23％",
        )
        fund2 = FundInfo(
            "S&P500投資信託2",
            "大和アセットマネジメント",
            "海外株式",
            "11,123円 （2/27）",
            80,
            0,
            0,
            "1.01％",
        )
        googlespreadsheet = GoogleSpreadSheet()
        googlespreadsheet.write_fundinfolist("ファンドテスト", [fund1, fund2])
