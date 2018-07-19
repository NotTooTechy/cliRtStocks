import pandas as pd
import numpy as np

#df = pd.read_csv('data/msft.csv', index_col='UID', names=['UID', 'First Name', 'Last Name', 'Age', 'Pre-Test Score', 'Post-Test Score'])
df = pd.read_csv('data/msft.csv')

#print df
#print dir(df)
print type(df)
print df.head()
print df.shape
print df.columns
print df.dtypes

#print df['MSFT']
col = []
for c in df.columns:
	print df[c].dtypes
	print df[c].head()
