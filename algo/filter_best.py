import json
import time
from copy import deepcopy as cp

with open('tsx_scan.json', 'r') as f:
	data = json.load(f)

top = {}
loops =0
for a, b in data.iteritems():
  loops+=1
  tmp_top = {}
  ticker = a
  avg = b[0]
  profit = b[1]
  lentop = len(top.keys())
  if lentop < 20:
     top[ticker] = round(profit)
  else:
    tmp_top = cp(top)
    for c, d in top.iteritems():
      if d < profit:
        del tmp_top[c]
        tmp_top[a] = round(profit)
        break
    top = cp(tmp_top)
    
#print top

for a, b in top.iteritems():
  print a, data[a]
        
        
with open('tsx_best.json', 'w') as f:
	json.dump(top, f) 
