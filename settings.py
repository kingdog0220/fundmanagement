import os
from os.path import dirname, join

from dotenv import load_dotenv

# 投資信託情報
NISSAY_TOPIX_URL = "https://www.wealthadvisor.co.jp/FundData/SnapShot.do?fnc=2015042708"
TAWARA_DEVELOPED_COUNTRY_URL = (
    "https://www.wealthadvisor.co.jp/FundData/SnapShot.do?fnc=2015121809"
)
E_MAXIS_SLIM_EMERGING_URL = (
    "https://www.wealthadvisor.co.jp/FundData/SnapShot.do?fnc=2017073108"
)
E_MAXIS_SLIM_SP500_URL = (
    "https://www.wealthadvisor.co.jp/FundData/SnapShot.do?fnc=2018070301"
)

# 各銀行・証券会社コード値
MUFJ_BANK = "MUFJ"
MUFJ_BANK_ACCOUNT = "MUFJ_ACC"
RAKUTEN_SECURITIES = "RKS"
RAKUTEN_SECURITIES_ACCOUNT = "RKS_ACC"

ACCOUNT_CODE = "account_code"
AMOUNT = "amount"
QUANTITY = "quantity"
UPDATE_DATE = "update_date"

# Google関連
GOOGLE_SPREAD_API = "https://spreadsheets.google.com/feeds"
GOOGLE_DRIVE_API = "https://www.googleapis.com/auth/drive"
FUNDINFO_SHEETNAME = "ファンド"
IMPORT_RETURN_CSV_SHEETNAME = "投資信託リターン"
TOTAL_ASSET_SHEETNAME = "総資産"

# ファイル操作
CSV_DIR = r".\fund\rakuten"
IMPORTED_FILE_DIR = r".\fund\rakuten\old"

# URL
MUFJ_LOGIN_URL = (
    "https://entry11.bk.mufg.jp/ibg/dfw/APLIN/loginib/login?_TRANID=AG004_001"
)
RAKUTEN_LOGIN_URL = "https://www.rakuten-sec.co.jp"

# 認証情報の読み込み
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

GAS_JSON_KEY_FILE_PATH = os.environ.get("GAS_JSON_KEY_FILE_PATH")
GOOGLE_SPREADSHEET_KEY = os.environ.get("GOOGLE_SPREADSHEET_KEY")
RAKUTEN_LOGIN_ID = os.environ.get("RAKUTEN_LOGIN_ID")
RAKUTEN_PASSWORD = os.environ.get("RAKUTEN_PASSWORD")
MUFJ_CONTRACT_NUMBER = os.environ.get("MUFJ_CONTRACT_NUMBER")
MUFJ_PASSWORD = os.environ.get("MUFJ_PASSWORD")
GMO_API_KEY = os.environ.get("GMO_API_KEY")
GMO_API_SECRET = os.environ.get("GMO_API_SECRET")
