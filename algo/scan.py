#sma_return(ticker=_ticker, short_window=sshort, capital=INITIAL_CAPITAL, step_buy_th=STEP_BUY_THERESHOLD, step_sell_th=STEP_SELL_THRESHOLD)
from d5 import sma_return

sma_list = {
	"BBD-B.TO" : 17,
	"PD.TO" : 25,
	"CPG.TO" : 10,
	"MEG.TO" : 24,
	"ACB.TO" : 6,
	"PLC.TO" : 6,
	"BB.TO" : 17 ,
	"PLC.TO" : 17 
    }

sma_list = {
	"ET.TO" : 17 ,
	"BB.TO" : 4 ,
	"JTR.V" : 17 ,
	"PYR.V" : 17 ,
	"HWO.TO" : 17 ,
	"SEV.TO" : 17 ,
	"OBE.TO" : 4
    }
CAPITAL = 3000
total_return = 0
total_capital = 0

for a, b in sma_list.iteritems():
    ret = sma_return(a, b, CAPITAL)
    print a, b, ret
    total_capital += CAPITAL
    total_return += ret
print
print 'Total Inestment\t', total_capital
print 'Total Return\t', total_return
