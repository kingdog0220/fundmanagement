import os
from os.path import dirname, join

from dotenv import load_dotenv

# 楽天証券投資信託情報
NISSAY_TOPIX_URL = "https://www.rakuten-sec.co.jp/web/fund/detail/?ID=JP90C000BRT6"
TAWARA_DEVELOPED_COUNTRY_URL = (
    "https://www.rakuten-sec.co.jp/web/fund/detail/?ID=JP90C000CMK4"
)
E_MAXIS_SLIM_EMERGING_URL = (
    "https://www.rakuten-sec.co.jp/web/fund/detail/?ID=JP90C000F7H5"
)
E_MAXIS_SLIM_SP500_URL = (
    "https://www.rakuten-sec.co.jp/web/fund/detail/?ID=JP90C000GKC6"
)
RAKUTEN_LOGIN_URL = "https://www.rakuten-sec.co.jp"

# Google関連
GOOGLE_SPREAD_API = "https://spreadsheets.google.com/feeds"
GOOGLE_DRIVE_API = "https://www.googleapis.com/auth/drive"
FUNDINFO_SHEETNAME = "ファンド"
IMPORT_RETURN_CSV_SHEETNAME = "投資信託リターン"

# ファイル操作
CSV_DIR = r".\fund\rakuten"
IMPORTED_FILE_DIR = r".\fund\rakuten\old"

# 認証情報の読み込み
dotenv_path = join(dirname(__file__), ".env")
load_dotenv(dotenv_path)

GAS_JSON_KEY_FILE_PATH = os.environ.get("GAS_JSON_KEY_FILE_PATH")
GOOGLE_SPREADSHEET_KEY = os.environ.get("GOOGLE_SPREADSHEET_KEY")
RAKUTEN_LOGIN_ID = os.environ.get("RAKUTEN_LOGIN_ID")
RAKUTEN_PASSWORD = os.environ.get("RAKUTEN_PASSWORD")
