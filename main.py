import datetime

import settings
from fund.rakuten_securities import RakutenSecurities
from googlespreadsheet import GoogleSpreadSheet

# main
try:
    print("START : {0:%Y/%m/%d %H:%M:%S}".format(datetime.datetime.now()))
    rakuten = RakutenSecurities()
    fundinfolist = rakuten.get_fundinfolist()
    googlespreadsheet = GoogleSpreadSheet()
    googlespreadsheet.write_fundinfolist(settings.FUNDINFO_SHEETNAME, fundinfolist)
    print("END-Success : {0:%Y/%m/%d %H:%M:%S}".format(datetime.datetime.now()))
except KeyboardInterrupt:
    print("KeyboardInterruptException")
except ValueError as ex:
    print("ValueError {}".format(ex))
except Exception:
    print("Exception")
