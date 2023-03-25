import os
import shutil
import unittest

import file
from fund.morningstar import MorningStar

TEST_DIR = r"D:\src\fundmanagement\test\test_case\rakuten"
TEST_DIR_OLD = r"D:\src\fundmanagement\test\test_case\rakuten\old"
FILE_NAME = "TotalReturn_test.csv"


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
        morningstar = MorningStar()
        with self.assertRaises(ValueError):
            morningstar.convert_to_billion("abc")

    def test_convert_to_billion(self):
        morningstar = MorningStar()
        value = morningstar.convert_to_billion("914,754百万円")
        self.assertEquals(value, 9147.54)
