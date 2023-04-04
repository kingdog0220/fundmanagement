import datetime
import os

import file
import settings
from fund.rakuten_securities import RakutenSecurities
from googlespreadsheet import GoogleSpreadSheet
from seleniumlauncher import SeleniumLauncher as seleniumlauncher

# main
try:
    print("START : {0:%Y/%m/%d %H:%M:%S}".format(datetime.datetime.now()))
    rakuten = RakutenSecurities()
    rakuten.get_total_return_csv(True)
    fundinfolist = rakuten.get_fundinfolist()
    googlespreadsheet = GoogleSpreadSheet()
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
    if seleniumlauncher.driver is not None:
        if seleniumlauncher.driver:
            seleniumlauncher.driver.quit
