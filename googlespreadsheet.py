# Googleスプレッドシート操作
import gspread
from oauth2client.service_account import ServiceAccountCredentials

import auth
import settings
from fund.fundinfo import FundInfo


class GoogleSpreadSheet:

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
    NAME = 0
    COMPANY = 1
    CATEGORY = 2
    BASE_PRICE = 3
    ALLOTMENT = 4
    COMMISION = 5
    COST = 6
    ASEETS = 7
    BEFORE_ASEETS = 8

    def __init__(self):
        # 認証情報の設定
        self.__credentials = ServiceAccountCredentials.from_json_keyfile_name(
            auth.JSON_KEY_FILE_PATH, self.__scope
        )

        # Googleスプレッドシートの取得
        gclient = gspread.authorize(self.__credentials)
        self.__workbook = gclient.open_by_key(auth.SPREADSHEET_KEY)

    def write_fundinfolist(self, sheetname: str, fund_info_list: list[FundInfo]):
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
            cell_list[self.ALLOTMENT].value = fund.allotment
            cell_list[self.COMMISION].value = fund.commision
            cell_list[self.COST].value = fund.cost
            # 純資産は前回純資産にコピーしてから
            cell_list[self.BEFORE_ASEETS].value = cell_list[self.ASEETS].value
            cell_list[self.ASEETS].value = fund.assets

            worksheet.update_cells(cell_list)
            currentRow += 1
