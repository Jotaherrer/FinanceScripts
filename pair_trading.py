import pandas as pd
import yfinance, datetime as dt
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

# Set params
start = dt.datetime(2020,1,1)
start = start.strftime('%Y-%m-%d')
end = dt.datetime(2020,11,6)
end = end.strftime('%Y-%m-%d')

# Stocks selection
stocks = ['AAPL','ABEV','AMD','AMZN', 'BA','BABA', 'BBD', 'C','DESP','GOLD','HMY','INTC','JPM','KO','MELI','MSFT','NVDA','PBR', 'PFE','QCOM','TSLA','WFC']
arg_stocks = ['BBAR','BMA', 'CEPU', 'CRESY', 'GGAL', 'PAM', 'SUPV', 'TGS', 'YPF']

# Data feed
data = yfinance.download(stocks, start=start, end=end, progress=False)
last_price = data.loc[:,'Adj Close']
returns = np.log(last_price).diff(1).dropna()
norm_rets = last_price.pct_change().dropna()
returns.cumsum().iloc[-1].sort_values(ascending=False)

# Arg data feed
data_arg = yfinance.download(arg_stocks, start=start, end=end, interval='60m' ,progress=False)
price_arg = data_arg.loc[:,'Adj Close']
rets_arg = np.log(price_arg).diff(1).dropna()

# Test correlation
rets_to_corr = []
legends = returns.columns.values
for asset in returns.columns.values:
    rets_to_corr.append(returns[asset].values)
    print('Ok, {} stored correctly'.format(asset))
correlations = np.corrcoef(rets_to_corr)

# Arg correlation
arg_rets_to_corr = []
legends_arg = rets_arg.columns.values
for asset in rets_arg.columns.values:
    arg_rets_to_corr.append(rets_arg[asset].values)
    print('Ok, {} stored correctly'.format(asset))
arg_correlations = np.corrcoef(arg_rets_to_corr)

# Plot correlations
fig = plt.figure(figsize=(16,14))
fig.subplots()
sns.heatmap(correlations, xticklabels=legends, yticklabels=legends, annot=True,cmap='Blues')
plt.show()

fig = plt.figure(figsize=(16,14))
fig.subplots()
sns.heatmap(arg_correlations, xticklabels=legends_arg, yticklabels=legends_arg, annot=True,cmap='Reds')
plt.show()

# Testing JPM/WFC case
bank_rets = pd.concat([returns['JPM'], returns['WFC']], axis=1)
bank_rets['relation'] = bank_rets['JPM'] / bank_rets['WFC']

plt.figure(figsize=(14,12))
plt.plot(bank_rets.loc[:, 'relation'])
plt.show()

# Testing GGAL/BMA
arg_banks_rets = pd.concat([rets_arg['GGAL'], rets_arg['BMA']], axis=1)
arg_banks_rets['relation'] = arg_banks_rets['GGAL'] / arg_banks_rets['BMA']

plt.figure(figsize=(14,12))
plt.plot(arg_banks_rets.loc['2020-01-02', 'relation'])
plt.show()