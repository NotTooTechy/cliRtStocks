import sys
import datetime

START_DATE=datetime.datetime(2018, 1, 16)
END_DATE=datetime.datetime(2019, 10, 10)

START_DATE=datetime.datetime(2017, 7, 16)
#END_DATE=datetime.datetime(2018, 1, 15)
def chk_arg(argument):
        if any(argument in s for s in sys.argv):
                        index = [i for i, s in enumerate(sys.argv) if argument in s][0]
                        ret = sys.argv[index].split('=')[1]
                        return ret
        return None


