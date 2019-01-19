import sys
import datetime

START_DATE=datetime.datetime(2018, 1, 16)
START_DATE=datetime.datetime(2016, 9, 16)
#START_DATE=datetime.datetime(2006, 9, 16)
END_DATE=datetime.datetime.now()
#END_DATE=datetime.datetime(2018, 11, 25)

api_key="ynfGhK3IYmAYvAyj9L2t"


#START_DATE=datetime.datetime(2015, 1, 19)
#START_DATE=datetime.datetime(2018, 7, 6)

RISK_SELL = 0.96
RISK_SELL = 0.9999
RISK_SELL = 0.96

def chk_arg(argument):
        if any(argument in s for s in sys.argv):
                        index = [i for i, s in enumerate(sys.argv) if argument in s][0]
                        ret = sys.argv[index].split('=')[1]
                        return ret
        return None


