import unittest

from fund.fundinfo import FundInfo
from googlespreadsheet import GoogleSpreadSheet


class TestGoogleSpreadSheet(unittest.TestCase):
    def setUp(self) -> None:
        googlespreadsheet = GoogleSpreadSheet()
        googlespreadsheet.workbook.values_clear("'ファンドテスト'!A2:I5")
        worksheet = googlespreadsheet.workbook.worksheet("ファンドテスト")
        worksheet.update_cell(2, 9, 130.2)
        worksheet.update_cell(3, 9, 100)

        worksheet2 = googlespreadsheet.workbook.worksheet("投資信託リターンテスト")
        worksheet2.clear()

        googlespreadsheet.workbook.values_clear("'総資産テスト'!E3:G16")

    @unittest.skip("個別に実行。書き込まれた結果を実際に確認する")
    def test_write_fundinfolist(self):
        fund = FundInfo(
            "日経平均投資信託",
            "大和アセットマネジメント",
            "国内株式",
            "14,500円",
            "2023年04月14日",
            100,
            200,
            "0.23％",
            120.4,
        )
        googlespreadsheet = GoogleSpreadSheet()
        googlespreadsheet.write_fundinfolist("ファンドテスト", [fund])

    @unittest.skip("個別に実行。書き込まれた結果を実際に確認する")
    def test_write_fundinfolists(self):
        fund1 = FundInfo(
            "日経平均投資信託1",
            "大和アセットマネジメント",
            "国内株式",
            "14,500円",
            "2023年04月14日",
            100,
            200,
            "0.23％",
            120.4,
        )
        fund2 = FundInfo(
            "S&P500投資信託2",
            "大和アセットマネジメント",
            "海外株式",
            "11,123円",
            "2023年04月14日",
            0,
            0,
            "1.01％",
            115,
        )
        googlespreadsheet = GoogleSpreadSheet()
        googlespreadsheet.write_fundinfolist("ファンドテスト", [fund1, fund2])

    @unittest.skip("個別に実行。書き込まれた結果を実際に確認する")
    def test_import_totalreturn_csv(self):
        googlespreadsheet = GoogleSpreadSheet()
        googlespreadsheet.import_totalreturn_csv(
            "投資信託リターンテスト",
            r"D:\src\fundmanagement\test\test_case\rakuten\TotalReturn_test.csv",
            "shift-jis",
        )

    @unittest.skip("個別に実行。書き込まれた結果を実際に確認する")
    def test_write_account_info(self):
        account_info_dic = {
            "code": "RKS",
            "amount": "1,234,567",
            "update_date": "2023/05/05",
        }
        googlespreadsheet = GoogleSpreadSheet()
        googlespreadsheet.write_account_info("総資産テスト", account_info_dic)
