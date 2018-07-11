import datetime as dt
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
from matplotlib import style
import pandas as pd
import pandas_datareader.data as web

style.use('ggplot')

start = dt.datetime(2018, 1, 1)
end = dt.datetime.now()

df = web.DataReader("MSFT", 'morningstar', start, end)

print(df.head())
print(df.tail())

