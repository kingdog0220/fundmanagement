import unittest

from application.googlespreadsheet import GoogleSpreadSheet
from fund.website.common.fundinfo import FundInfo


class TestGoogleSpreadSheet(unittest.TestCase):
    def setUp(self) -> None:
        googlespreadsheet = GoogleSpreadSheet()
        googlespreadsheet.workbook.values_clear("'ファンドテスト'!A2:I5")
        worksheet = googlespreadsheet.workbook.worksheet("ファンドテスト")
        worksheet.update_cell(2, 9, 130.2)
        worksheet.update_cell(3, 9, 100)

        worksheet2 = googlespreadsheet.workbook.worksheet("投資信託リターンテスト")
        worksheet2.clear()

        googlespreadsheet.workbook.values_clear("'総資産テスト'!F3:I16")

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
            r"D:\src\fundmanagement\test\test_data\rakuten_securities\TotalReturn_test.csv",
            "shift-jis",
        )

    @unittest.skip("個別に実行。書き込まれた結果を実際に確認する")
    def test_write_account_info(self):
        account_info_dic = {
            "account_code": "RKS_ACC",
            "amount": "1,234,567.012",
            "quantity": "1.20105",
            "update_date": "2023/05/05",
        }
        googlespreadsheet = GoogleSpreadSheet()
        googlespreadsheet.write_account_info("総資産テスト", account_info_dic)

    def test_convert_to_float(self):
        googlespreadsheet = GoogleSpreadSheet()
        value = googlespreadsheet.convert_to_float("12,000.123")
        self.assertEquals(value, 12000.123)

    def test_convert_to_float_empty(self):
        googlespreadsheet = GoogleSpreadSheet()
        value = googlespreadsheet.convert_to_float("")
        self.assertEquals(value, 0)

    def test_convert_to_float_exception(self):
        googlespreadsheet = GoogleSpreadSheet()
        with self.assertRaises(ValueError):
            googlespreadsheet.convert_to_float("abc")
