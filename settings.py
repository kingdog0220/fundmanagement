import os
from os.path import dirname, join

from dotenv import load_dotenv

# 各銀行・証券会社コード値
MUFJ_BANK = "MUFJ"
MUFJ_BANK_ACCOUNT = "MUFJ_ACC"
RAKUTEN_SECURITIES = "RKS"
RAKUTEN_SECURITIES_ACCOUNT = "RKS_ACC"
GMO = "GMO"
GMO_JPY = "GMOJPY"
GMO_BTC = "GMOBTC"
GMO_XTZ = "GMOXTZ"
SBI_SECURITIES = "SBIS"
SBI_SECURITIES_MMF_ACCOUNT = "SBISMMF_ACC"
SBI_SECURITIES_FX_ACCOUNT = "SBISFX_ACC"
RAKUTEN_BANK = "RKB"
RAKUTEN_BANK_ACCOUNT = "RKB_ACC"
SBI_BANK = "SBIB"
SBI_BANK_ACCOUNT = "SBIB_ACC"
SBI_BANK_FX_ACCOUNT = "SBIBFX_ACC"
DC = "DC"
DC_ACCOUNT = "DC_ACC"

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
CSV_DIR = r".\fund\website\rakuten_securities"
IMPORTED_FILE_DIR = r".\fund\website\rakuten_securities\old"

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
SBI_LOGIN_ID = os.environ.get("SBI_LOGIN_ID")
SBI_PASSWORD = os.environ.get("SBI_PASSWORD")
RAKUTEN_BANK_LOGIN_ID = os.environ.get("RAKUTEN_BANK_LOGIN_ID")
RAKUTEN_BANK_PASSWORD = os.environ.get("RAKUTEN_BANK_PASSWORD")
SBI_BANK_LOGIN_ID = os.environ.get("SBI_BANK_LOGIN_ID")
SBI_BANK_LOGIN_PASSWORD = os.environ.get("SBI_BANK_LOGIN_PASSWORD")
DC_LOGIN_ID = os.environ.get("DC_LOGIN_ID")
DC_LOGIN_PASSWORD = os.environ.get("DC_LOGIN_PASSWORD")

# URL
NISSAY_TOPIX_URL = os.environ.get("NISSAY_TOPIX_URL")
TAWARA_DEVELOPED_COUNTRY_URL = os.environ.get("TAWARA_DEVELOPED_COUNTRY_URL")
E_MAXIS_SLIM_EMERGING_URL = os.environ.get("E_MAXIS_SLIM_EMERGING_URL")
E_MAXIS_SLIM_SP500_URL = os.environ.get("E_MAXIS_SLIM_SP500_URL")
MUFJ_LOGIN_URL = os.environ.get("MUFJ_LOGIN_URL")
RAKUTEN_LOGIN_URL = os.environ.get("RAKUTEN_LOGIN_URL")
SBI_LOGIN_URL = os.environ.get("SBI_LOGIN_URL")
RAKUTEN_BANK_LOGIN_URL = os.environ.get("RAKUTEN_BANK_LOGIN_URL")
SBI_BANK_URL = os.environ.get("SBI_BANK_URL")
DC_LOGIN_URL = os.environ.get("DC_LOGIN_URL")
