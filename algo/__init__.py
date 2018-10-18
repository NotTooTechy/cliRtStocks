import sys
import datetime

START_DATE=datetime.datetime(2018, 1, 16)
START_DATE=datetime.datetime(2017, 9, 16)
END_DATE=datetime.datetime.now()


#START_DATE=datetime.datetime(2015, 1, 19)
#START_DATE=datetime.datetime(2018, 7, 6)

RISK_SELL = 0.88
RISK_SELL = 0.96
RISK_SELL = 0.88
RISK_SELL = 0.9999
RISK_SELL = 0.94

def chk_arg(argument):
        if any(argument in s for s in sys.argv):
                        index = [i for i, s in enumerate(sys.argv) if argument in s][0]
                        ret = sys.argv[index].split('=')[1]
                        return ret
        return None


