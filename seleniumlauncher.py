import os

from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager

import settings


# シングルトンとして使い回す
class SeleniumLauncher:
    driver = None

    def __new__(cls):
        if cls.driver is None:
            options = Options()
            absolute_path = os.path.abspath(settings.CSV_DIR)
            prefs = {"download.default_directory": absolute_path}
            options.add_experimental_option("prefs", prefs)
            options.add_experimental_option("excludeSwitches", ["enable-logging"])
            # 常に最新バージョンのChromeDriverをダウンロードして自動的に使用
            cls.driver = webdriver.Chrome(
                ChromeDriverManager().install(), chrome_options=options
            )
        return cls.driver
