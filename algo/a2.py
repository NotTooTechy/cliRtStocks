import pandas_datareader as pdr
import pandas as pd
import datetime 
import sys

ticker = sys.argv[1]
instr = pdr.get_data_yahoo(ticker, 
                          start=datetime.datetime(2018, 1, 1), 
                          end=datetime.datetime(2018, 8, 1))

instr.to_csv('data/%s.csv'%ticker)
df = pd.read_csv('data/%s.csv'%ticker, header=0, index_col='Date', parse_dates=True)

print instr.tail()