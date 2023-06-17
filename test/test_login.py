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

    def test_rks(self):
        container = WebSiteDIContainer()
        website = container.resolve("RKS")
        data = website.get_account("RKS_ACC")
        website.logout()
        dir = os.path.join(TEST_DIR, "test_rks.json")
        with open(dir, mode="wt", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def test_rkb(self):
        container = WebSiteDIContainer()
        website = container.resolve("RKB")
        data = website.get_account("RKB_ACC")
        website.logout()
        dir = os.path.join(TEST_DIR, "test_rkb.json")
        with open(dir, mode="wt", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)

    def test_sbis(self):
        container = WebSiteDIContainer()
        website = container.resolve("SBIS")
        data = website.get_account("SBISMMF_ACC")
        dir = os.path.join(TEST_DIR, "test_sbis_mmf.json")
        with open(dir, mode="wt", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        data2 = website.get_account("SBISFX_ACC")
        dir = os.path.join(TEST_DIR, "test_sbis_fx.json")
        with open(dir, mode="wt", encoding="utf-8") as f:
            json.dump(data2, f, ensure_ascii=False, indent=2)
        website.logout()

    def test_sbib(self):
        container = WebSiteDIContainer()
        website = container.resolve("SBIB")
        data = website.get_account("SBIB_ACC")
        dir = os.path.join(TEST_DIR, "test_sbib.json")
        with open(dir, mode="wt", encoding="utf-8") as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        data2 = website.get_account("SBIBFX_ACC")
        dir = os.path.join(TEST_DIR, "test_sbib_fx.json")
        with open(dir, mode="wt", encoding="utf-8") as f:
            json.dump(data2, f, ensure_ascii=False, indent=2)
        website.logout()

    def tearDown(self):
        if seleniumlauncher.driver:
            seleniumlauncher.driver.quit
