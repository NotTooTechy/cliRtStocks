import json
import time
from copy import deepcopy as cp
from __init__ import chk_arg


fname=None
if chk_arg("json") is not None:
        fname= chk_arg("json")

with open(fname, 'r') as f:
	data = json.load(f)

top = {}
loops =0
for symbol, profit_avg_list in sorted(data.iteritems()):
    avg = int(profit_avg_list[0])
    profit = float(profit_avg_list[1])
    if profit < 1:
        continue
    if len(top) < 30:
        top[symbol] = profit_avg_list
        continue
    for tmp_symbol, tmp_profit_avg_list in sorted(top.iteritems()):
        tmp_avg = int(tmp_profit_avg_list[0])
        tmp_profit = float(tmp_profit_avg_list[1])
        if profit > tmp_profit:
            del top[tmp_symbol]
            top[symbol] = profit_avg_list
            break

print json.dumps(top, indent=4, sort_keys=True)        
with open('filtered_%s'%fname, 'w') as f:
	json.dump(top, f, indent=4) 

