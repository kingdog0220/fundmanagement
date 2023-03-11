from fund.rakuten_securities import RakutenSecurities

# main
try:
    rakuten = RakutenSecurities()
    fundinfolist = rakuten.get_fundinfolist()
except KeyboardInterrupt:
    print("KeyboardInterruptException")
except ValueError as ex:
    print("ValueError {}".format(ex))
except Exception:
    print("Exception")
