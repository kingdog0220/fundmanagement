import json
import os
import unittest

from application.seleniumlauncher import SeleniumLauncher as seleniumlauncher
from fund.website.common.webcontainer import WebSiteDIContainer

TEST_DIR = r"D:\src\fundmanagement\test\test_data\login"


class TestLogin(unittest.TestCase):
    def test_mufj(self):
        container = WebSiteDIContainer()
        website = container.resolve("MUFJ")
        data = website.get_account("MUFJ_ACC")
        website.logout()
        dir = os.path.join(TEST_DIR, "test_mufj.json")
        with open(dir, mode="wt", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def tearDown(self):
        if seleniumlauncher.driver:
            seleniumlauncher.driver.quit
