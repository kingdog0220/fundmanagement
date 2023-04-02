from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager


# シングルトンとして使い回す
class SeleniumLauncher:
    driver = None

    def __new__(cls):
        if cls.driver is None:
            options = Options()
            # 常に最新バージョンのChromeDriverをダウンロードして自動的に使用
            cls.driver = webdriver.Chrome(
                ChromeDriverManager().install(), chrome_options=options
            )
        return cls.driver
