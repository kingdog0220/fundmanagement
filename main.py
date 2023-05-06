import datetime
import os

import file
import settings
from fund.wealthadvisor import WealthAdvisor
from fund.website import WebSiteDIContainer
from googlespreadsheet import GoogleSpreadSheet
from seleniumlauncher import SeleniumLauncher as seleniumlauncher

# main
try:
    print("START : {0:%Y/%m/%d %H:%M:%S}".format(datetime.datetime.now()))
    # 口座情報の取得
    container = WebSiteDIContainer()
    website_list = [settings.MUFJ_BANK, settings.RAKUTEN_SECURITIES]
    account_info_list = []
    for website_code in website_list:
        website = container.resolve(website_code)
        account_info_dic = website.get_account_info()
        account_info_list.append(account_info_dic)

    # 投資信託の基本情報取得
    wealthadvisor = WealthAdvisor()
    fundinfolist = wealthadvisor.get_fundinfolist()
    # GoogleSpreadSheetへ書き込む
    googlespreadsheet = GoogleSpreadSheet()
    for account_info_dic in account_info_list:
        googlespreadsheet.write_account_info(
            settings.TOTAL_ASSET_SHEETNAME, account_info_dic
        )

    googlespreadsheet.write_fundinfolist(settings.FUNDINFO_SHEETNAME, fundinfolist)
    files = file.get_files(settings.CSV_DIR)
    # 1件しか取得しない想定
    filepath = os.path.join(settings.CSV_DIR, files[0])
    googlespreadsheet.import_totalreturn_csv(
        settings.IMPORT_RETURN_CSV_SHEETNAME, filepath
    )
    file.move_file(filepath, settings.IMPORTED_FILE_DIR)
    print("END-Success : {0:%Y/%m/%d %H:%M:%S}".format(datetime.datetime.now()))
except KeyboardInterrupt:
    print("KeyboardInterruptException")
except ValueError as ex:
    print("ValueError {}".format(ex))
except Exception as ex:
    print("Exception {}".format(ex))
finally:
    if seleniumlauncher.driver:
        seleniumlauncher.driver.quit
