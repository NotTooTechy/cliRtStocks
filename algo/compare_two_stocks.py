import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF

import numpy as np
import pandas as pd

import sys

fname = sys.argv[1]
fname2= sys.argv[2]
df = pd.read_csv(fname)

#sample_data_table = FF.create_table(df.head())
#py.plot(sample_data_table, filename='sample-data-table')

trace1 = go.Scatter(
                    x=df['Date'], y=df['Adj Close'], # Data
                    mode='lines', name='%s'%fname.strip(".csv") # Additional options
                   )
df = pd.read_csv(fname2)
trace2 = go.Scatter(
                    x=df['Date'], y=df['Adj Close'], #.rolling(6).mean(), # Data
                    mode='lines', name='Moving Avg' # Additional options
                   )

#print annotations
#trace2 = go.Scatter(x=df['x'], y=df['sinx'], mode='lines', name='sinx' )
#trace3 = go.Scatter(x=df['x'], y=df['cosx'], mode='lines', name='cosx')

layout = go.Layout(title=fname,
                   plot_bgcolor='rgb(230, 230,230)',
                   showlegend=True,
                   )#yaxis = yaxis)


#fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
fig = go.Figure(data=[trace1,trace2], layout=layout)

fname = fname.split("/")[1]
fname = fname.split(".")[0]
fname2 = fname2.split("/")[1]
fname2 = fname2.split(".")[0]
fname += "-" + fname2
# Plot data in the notebook
py.plot(fig, filename=fname)
#plt.plot(df['WFC'].rolling(9).mean(),label= 'MA 9 days')
