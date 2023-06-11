import datetime
import os

import file
import settings
from application.googlespreadsheet import GoogleSpreadSheet
from application.seleniumlauncher import SeleniumLauncher as seleniumlauncher
from fund.website.common.webcontainer import WebSiteDIContainer
from fund.website.wealthadvisor import WealthAdvisor

# main
try:
    print("START : {0:%Y/%m/%d %H:%M:%S}".format(datetime.datetime.now()))
    # 口座情報の取得
    container = WebSiteDIContainer()
    website_dic = {
        settings.MUFJ_BANK: [settings.MUFJ_BANK_ACCOUNT],
        settings.RAKUTEN_SECURITIES: [settings.RAKUTEN_SECURITIES_ACCOUNT],
        settings.GMO: [settings.GMO_JPY, settings.GMO_BTC, settings.GMO_XTZ],
        settings.SBI_SECURITIES: [
            settings.SBI_SECURITIES_MMF_ACCOUNT,
            settings.SBI_SECURITIES_FX_ACCOUNT,
        ],
        settings.RAKUTEN_BANK: [settings.RAKUTEN_BANK_ACCOUNT],
        settings.SBI_BANK: [settings.SBI_BANK_ACCOUNT, settings.SBI_BANK_FX_ACCOUNT],
        settings.DC: [settings.DC_ACCOUNT],
    }
    account_info_list = []
    for site_code, account_codes in website_dic.items():
        print("Website:{0}".format(site_code))
        website = container.resolve(site_code)
        website.login()
        for account_code in account_codes:
            print("Account:{0}".format(account_code))
            account_info_dic = website.get_account(account_code)
            account_info_list.append(account_info_dic)
        website.logout()

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
    if len(files) == 0:
        print(
            "No total return file : {0:%Y/%m/%d %H:%M:%S}".format(
                datetime.datetime.now()
            )
        )
    elif len(files) > 1:
        print(
            "Many total return files : {0:%Y/%m/%d %H:%M:%S}".format(
                datetime.datetime.now()
            )
        )
    else:
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
