cmd = "python g5.py aapl short=%d"
cmd = "python g5.py msft short=%d"
cmd = "python g5.py hou.to short=%d"
import commands

for i in range(1, 30):
	out = commands.getoutput(cmd%i)
	print i, out.strip()


