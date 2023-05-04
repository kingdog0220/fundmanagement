# Googleスプレッドシート操作
import csv

import gspread
from oauth2client.service_account import ServiceAccountCredentials

import settings
from fund.fundinfo import FundInfo


class GoogleSpreadSheet:
    """GoogleSpreadSheetの操作を管理する"""

    __workbook: gspread.Spreadsheet

    @property
    def workbook(self):
        return self.__workbook

    __scopes = [
        settings.GOOGLE_SPREAD_API,
        settings.GOOGLE_DRIVE_API,
    ]
    __scope = " ".join(__scopes)

    # 列位置
    CODE = 0
    AMOUNT = 4
    QUANTITY = 5
    UPDATE_DATE = 6

    NAME = 0
    COMPANY = 1
    CATEGORY = 2
    BASE_PRICE = 3
    BASE_DATE = 4
    ALLOTMENT = 5
    COMMISION = 6
    COST = 7
    ASEETS = 8
    BEFORE_ASEETS = 9

    def __init__(self):
        # 認証情報の設定
        self.__credentials = ServiceAccountCredentials.from_json_keyfile_name(
            settings.GAS_JSON_KEY_FILE_PATH, self.__scope
        )

        # Googleスプレッドシートの取得
        gclient = gspread.authorize(self.__credentials)
        self.__workbook = gclient.open_by_key(settings.GOOGLE_SPREADSHEET_KEY)

    def write_account_info(self, sheetname: str, account_info_dic: dict):
        """口座情報をシートに書き込む

        Args:
            sheetname (str): シート名
            account_info_dic (dict): 口座情報
        """
        worksheet = self.__workbook.worksheet(sheetname)
        if worksheet is None:
            raise ValueError("error-sheetname is None.")

        cell = worksheet.find(account_info_dic[settings.CODE])
        if cell is None:
            return
        cell_list = worksheet.range(cell.row, self.CODE + 1, cell.row, self.UPDATE_DATE + 1)  # type: ignore
        if settings.AMOUNT in account_info_dic:
            num_value = round(
                float(account_info_dic[settings.AMOUNT].replace(",", "")), 0
            )
            cell_list[self.AMOUNT].value = num_value
        if settings.QUANTITY in account_info_dic:
            cell_list[self.QUANTITY].value = account_info_dic[settings.QUANTITY]
        if settings.UPDATE_DATE in account_info_dic:
            cell_list[self.UPDATE_DATE].value = account_info_dic[settings.UPDATE_DATE]
        worksheet.update_cells(cell_list)

    def write_fundinfolist(self, sheetname: str, fund_info_list: list[FundInfo]):
        """投資信託の情報をシートに書き込む

        Args:
            sheetname (str): シート名
            fund_info_list (list[FundInfo]): 投資信託の情報一覧
        """
        worksheet = self.__workbook.worksheet(sheetname)
        if worksheet is None:
            raise ValueError("error-sheetname is None.")

        currentRow = 2
        for fund in fund_info_list:
            # linterがアホなので
            cell_list = worksheet.range(currentRow, self.NAME + 1, currentRow, self.BEFORE_ASEETS + 1)  # type: ignore

            cell_list[self.NAME].value = fund.name
            cell_list[self.COMPANY].value = fund.company
            cell_list[self.CATEGORY].value = fund.category
            cell_list[self.BASE_PRICE].value = fund.baseprice
            cell_list[self.BASE_DATE].value = fund.basedate
            cell_list[self.ALLOTMENT].value = fund.allotment
            cell_list[self.COMMISION].value = fund.commision
            cell_list[self.COST].value = fund.cost
            # 純資産は前回純資産にコピーしてから
            cell_list[self.BEFORE_ASEETS].value = cell_list[self.ASEETS].value
            cell_list[self.ASEETS].value = fund.assets

            worksheet.update_cells(cell_list)
            currentRow += 1

    def import_totalreturn_csv(
        self, sheetname: str, filepath: str, encode: str = "shift-jis"
    ):
        """リターンデータ(CSV)をインポートする

        Args:
            sheetname (str): シート名
            filepath (str): リターンデータ(CSV)のファイルパス
            encode (str, optional): 文字コード Defaults to "shift-jis".
        """
        self.__workbook.values_update(
            sheetname,
            params={"valueInputOption": "USER_ENTERED"},
            body={"values": list(csv.reader(open(filepath, encoding=encode)))},
        )
