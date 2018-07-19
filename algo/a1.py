import pandas_datareader as pdr
import datetime 
msft = pdr.get_data_yahoo('MSFT', 
                          start=datetime.datetime(2018, 1, 1), 
                          end=datetime.datetime(2018, 8, 1))

print msft
