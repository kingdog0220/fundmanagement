import os
import shutil
import unittest

import file

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
