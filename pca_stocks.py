import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import bs4 as bs
import requests
import yfinance as yf

"""
https://towardsdatascience.com/stock-market-analytics-with-pca-d1c2318e3f0e
https://github.com/gylx/Financial-Machine-Learning-Articles/blob/master/Stock%20Market%20Analytics%20with%20PCA.ipynb
"""
plt.style.use('fivethirtyeight')

def spx():
    url = 'http://en.wikipedia.org/wiki/List_of_S%26P_500_companies'
    response = requests.get(url)
    if response.status_code == 200:
        soup = bs.BeautifulSoup(response.text, 'html')
        table = soup.find('table', {'class': 'wikitable sortable'})
        tickers = []
        for row in table.findAll('tr')[1:]:
            ticker = row.findAll('td')[0].text
            if not '.' in ticker:
                tickers.append(ticker.replace('\n',''))
    return tickers

tickers = spx()

prices = yf.download(tickers, start='2020-01-01')['Adj Close']
prices_done = prices.dropna(how='all')
rets = np.log(prices).diff(1).dropna(how='all')

### PLOT DAILY RETURNS

fig = plt.figure(figsize=(10,8))
ax = fig.subplots()
plt.plot(rets)
plt.title('Daily Returns SPY Stocks in 2020')
plt.tight_layout()
plt.show()
plt.close('all')

### PLOT CUMMULATIVE RETURNS

rets_cum = np.exp(rets.cumsum())
fig2 = plt.figure(figsize=(10,8))
ax2 = fig2.subplots()
plt.plot(rets_cum)
plt.tight_layout()
plt.show()
plt.close('all')

### PCA APPLICATION
from sklearn.decomposition import PCA

pca = PCA(1).fit(rets.fillna(0))
pc1 = pd.Series(index=rets.columns, data=pca.components_[0])
pc1.plot(figsize=(10,8))
plt.title("First Principal Component of SPY")
plt.show()
plt.close('all')

weights = abs(pc1) / sum(abs(pc1))
myrets = (weights * rets).sum(1)
np.exp(myrets.cumsum()).plot(figsize=(10,8))
plt.title('')