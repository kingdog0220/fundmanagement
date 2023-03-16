import settings
from fund.rakuten_securities import RakutenSecurities
from googlespreadsheet import GoogleSpreadSheet

# main
try:
    rakuten = RakutenSecurities()
    fundinfolist = rakuten.get_fundinfolist()
    googlespreadsheet = GoogleSpreadSheet()
    googlespreadsheet.write_fundinfolist(settings.FUNDINFO_SHEETNAME, fundinfolist)
except KeyboardInterrupt:
    print("KeyboardInterruptException")
except ValueError as ex:
    print("ValueError {}".format(ex))
except Exception:
    print("Exception")
