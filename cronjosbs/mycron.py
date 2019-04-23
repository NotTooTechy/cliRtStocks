from commands import getoutput as gout

cmd = '''cd /root/cliRtStocks;date;./stckscreener.py usmarkets'''
output = gout(cmd)
out = output.split("\n")
for loop in out:
        print loop.strip(),"\t",
print

