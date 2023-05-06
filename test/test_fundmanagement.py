import json
import os
import shutil
import unittest

import file
from fund.gmo import GMO
from fund.wealthadvisor import WealthAdvisor

TEST_DIR = r"D:\src\fundmanagement\test\test_case\rakuten"
TEST_DIR_OLD = r"D:\src\fundmanagement\test\test_case\rakuten\old"
FILE_NAME = "TotalReturn_test.csv"

TEST_DIR_GMO = r"D:\src\fundmanagement\test\test_case\gmo"


class TestFundManagement(unittest.TestCase):
    def setUp(self):
        if os.path.exists(os.path.join(TEST_DIR_OLD, FILE_NAME)):
            shutil.move(
                os.path.join(TEST_DIR_OLD, FILE_NAME), os.path.join(TEST_DIR, FILE_NAME)
            )

    def test_get_files(self):
        files = file.get_files(TEST_DIR)
        expects = [FILE_NAME]
        self.assertListEqual(expects, files)

    def test_move_file(self):
        file.move_file(
            os.path.join(TEST_DIR, FILE_NAME),
            TEST_DIR_OLD,
        )
        files = file.get_files(TEST_DIR)
        self.assertCountEqual(files, [])

    def test_convert_to_billion_exception(self):
        wealthadvisor = WealthAdvisor()
        with self.assertRaises(ValueError):
            wealthadvisor.convert_to_billion("abc")

    def test_convert_to_billion(self):
        wealthadvisor = WealthAdvisor()
        value = wealthadvisor.convert_to_billion("914,754百万円")
        self.assertEquals(value, 9147.54)

    def test_get_gmo_account_assets(self):
        """実際にJSONファイルを出力できるか"""
        gmo = GMO()
        data = gmo.get_assets()
        dir = os.path.join(TEST_DIR_GMO, "gmo_test.json")
        with open(dir, mode="wt", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def test_get_gmo_account_assets_jpy(self):
        """実際にJSONファイルを出力できるか"""
        gmo = GMO()
        data = gmo.get_account_info("GMOJPY")
        dir = os.path.join(TEST_DIR_GMO, "gmo_test_jpy.json")
        with open(dir, mode="wt", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def test_get_gmo_account_assets_btc(self):
        """実際にJSONファイルを出力できるか"""
        gmo = GMO()
        data = gmo.get_account_info("GMOBTC")
        dir = os.path.join(TEST_DIR_GMO, "gmo_test_btc.json")
        with open(dir, mode="wt", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def test_calc_amount(self):
        gmo = GMO()
        amount = gmo.calc_amount("120.2345", "10.12")
        self.assertEquals(amount, 1217)

    def test_calc_amount_conversionrate_exception(self):
        gmo = GMO()
        with self.assertRaises(ValueError):
            gmo.calc_amount("120.2345", "ABC")

    def test_calc_amount_amount_exception(self):
        gmo = GMO()
        with self.assertRaises(ValueError):
            gmo.calc_amount("XYZ", "10.12")

    def test_calc_amount_empty_exception(self):
        gmo = GMO()
        with self.assertRaises(ValueError):
            gmo.calc_amount("", "")
