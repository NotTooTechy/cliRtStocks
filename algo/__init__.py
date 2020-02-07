import sys
import datetime

#START_DATE=datetime.datetime(2016, 1, 16)
#START_DATE=datetime.datetime(2016, 9, 16)
START_DATE=datetime.datetime(2018, 02, 17)
#START_DATE=datetime.datetime(2009, 1, 1)
#START_DATE=datetime.datetime(2017, 1, 1)
#START_DATE=datetime.datetime(2007, 9, 16)
END_DATE=datetime.datetime.now()
#END_DATE=datetime.datetime(2019, 02, 04) #2018-05-16

#alpha: https://www.alphavantage.co/support/#api-key
api_key="EAE489DPENMJ722N"


#START_DATE=datetime.datetime(2015, 1, 19)
#START_DATE=datetime.datetime(2018, 7, 6)

RISK_SELL = 0.96
RISK_SELL = 0.9999
RISK_SELL = 1

def chk_arg(argument):
        if any(argument in s for s in sys.argv):
                        index = [i for i, s in enumerate(sys.argv) if argument in s][0]
                        try:
                            ret = sys.argv[index].split('=')[1]
                        except:
                            return None
                        return ret
        return None
