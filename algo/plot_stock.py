import plotly.plotly as py
import plotly.graph_objs as go
import plotly.figure_factory as FF

import numpy as np
import pandas as pd

import sys

fname = sys.argv[1]
window_size= int(sys.argv[2])
df = pd.read_csv(fname)
df = df.iloc[::-1]

#sample_data_table = FF.create_table(df.head())
#py.plot(sample_data_table, filename='sample-data-table')

trace1 = go.Scatter(
                    x=df['timestamp'], y=df['close'], # Data
                    mode='lines', name='%s'%fname.strip(".csv") # Additional options
                   )
trace2 = go.Scatter(
                    x=df['timestamp'], y=df['close'].rolling(window_size).mean(), # Data
                    mode='lines', name='Mvg Avg(%s)'%window_size # Additional options
                   )
count = 0
buy_flag = True
under_avg_count = 0
annotations=[]
#font=dict(family='Courier New, monospace', size=16, color='#ffffff')
font_buy=dict(family='Courier New, monospace', size=14, color='black')
font_sell=dict(family='Courier New, monospace', size=18, color='red')
yaxis=dict(range=[0, 15])
for index, row in df.iterrows():
    font_sell=dict(family='Courier New, monospace', size=18, color='red')
    close_val = row['close']
    moving_avg=df['close'].rolling(window=window_size, min_periods=1, center=False).mean()
    moving_avg = moving_avg[index]
    if count >30 and isinstance(moving_avg, float):
        if close_val> moving_avg and buy_flag:
            buy_flag = False
            buy_price = row['close']
            x = dict( x=row['timestamp'], y=row['close'], xref='x', yref='y', text='BUY', showarrow=True, arrowhead=5, ax=-30, ay=70, font=font_buy)
            annotations.append(x)

        if close_val< moving_avg and not buy_flag:
            under_avg_count += 1
        if under_avg_count > 7:
            under_avg_count = 0
            buy_flag = True
            if close_val > buy_price:
                font_sell=dict(family='Courier New, monospace', size=18, color='green')
            x = dict( x=row['timestamp'], y=row['close'], xref='x', yref='y', text='SELL', showarrow=True, arrowhead=2, ax=-30, ay=70, font=font_sell)
            annotations.append(x)
    count += 1
#annotations = [dict( x=row['timestamp'], y=row['close'], xref='x', yref='y', text='SELL', showarrow=True, arrowhead=7, ax=10, ay=-40)]

#print annotations
#trace2 = go.Scatter(x=df['x'], y=df['sinx'], mode='lines', name='sinx' )
#trace3 = go.Scatter(x=df['x'], y=df['cosx'], mode='lines', name='cosx')

layout = go.Layout(title=fname,
                   plot_bgcolor='rgb(230, 230,230)',
                   showlegend=True,
                   annotations=annotations,
                   )#yaxis = yaxis)


#fig = go.Figure(data=[trace1, trace2, trace3], layout=layout)
fig = go.Figure(data=[trace1,trace2], layout=layout)

fname = fname.split("/")[1]
#fname = fname.split(".")[0]
print(fname)
# Plot data in the notebook
py.plot(fig, filename=fname)
#plt.plot(df['WFC'].rolling(9).mean(),label= 'MA 9 days')
