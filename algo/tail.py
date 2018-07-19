import sys
import json
from commands import getoutput as gout

kupljeno = {
        "HOU.TO":10.75,
        "CVE.TO":13.82,
        "JTR.V":1.00
}

def check_entry(cmd_arg):
	if any(cmd_arg in s for s in sys.argv):
			index = [i for i, s in enumerate(sys.argv) if cmd_arg in s][0]
			lines = sys.argv[index].split('=')[1]
			return lines
	return None


lines = 15
l = check_entry("lines")
if l is not None:
	lines = int(l)

with open("best_avg.json", 'r') as f:
	data = json.load(f)

cmd = "python d5.py %s short=%s debug | tail -n %d"
for ticker, short in data.iteritems():
	print "-"*80
	print gout(cmd%(ticker, short, lines))



