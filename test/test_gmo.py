import json
import os
import unittest

from fund.gmo import GMO

TEST_DIR = r"D:\src\fundmanagement\test\test_case\gmo"


class TestGMO(unittest.TestCase):
    def test_get_gmo_account_assets(self):
        """実際にJSONファイルを出力できるか"""
        gmo = GMO()
        data = gmo.get_assets()
        dir = os.path.join(TEST_DIR, "gmo_test.json")
        with open(dir, mode="wt", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def test_get_gmo_account_assets_jpy(self):
        """実際にJSONファイルを出力できるか"""
        gmo = GMO()
        data = gmo.get_account_info("GMOJPY")
        dir = os.path.join(TEST_DIR, "gmo_test_jpy.json")
        with open(dir, mode="wt", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def test_get_gmo_account_assets_btc(self):
        """実際にJSONファイルを出力できるか"""
        gmo = GMO()
        data = gmo.get_account_info("GMOBTC")
        dir = os.path.join(TEST_DIR, "gmo_test_btc.json")
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
