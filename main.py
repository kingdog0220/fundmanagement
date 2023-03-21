import datetime

import settings
from fund.morningstar import MorningStar
from googlespreadsheet import GoogleSpreadSheet

# main
try:
    print("START : {0:%Y/%m/%d %H:%M:%S}".format(datetime.datetime.now()))
    morningstar = MorningStar()
    fundinfolist = morningstar.get_fundinfolist()
    googlespreadsheet = GoogleSpreadSheet()
    googlespreadsheet.write_fundinfolist(settings.FUNDINFO_SHEETNAME, fundinfolist)
    print("END-Success : {0:%Y/%m/%d %H:%M:%S}".format(datetime.datetime.now()))
except KeyboardInterrupt:
    print("KeyboardInterruptException")
except ValueError as ex:
    print("ValueError {}".format(ex))
except Exception:
    print("Exception")
