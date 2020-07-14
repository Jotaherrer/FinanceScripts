#%% IMPORT PACKAGES
import pandas_datareader as pdr
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib.inline

#%% BANCOS EN PESOS, MERVAL EN PESOS
mkt_banks_arg = pdr.get_data_yahoo(['BMA.BA', 'GGAL.BA', 'SUPV.BA'], start='1/1/2010')
ggal = pdr.get_data_yahoo('GGAL.BA', start='1/1/2019')
imv = pdr.get_data_yahoo('^MERV', start='1/1/2010')

#%% GALICIA Y BANCOS ADRS
ggal_adr = pdr.get_data_yahoo('GGAL', start='1/1/2010')
ggal_adr_chg = ggal_adr['Adj Close'].pct_change()
mkt_banks_adr = pdr.get_data_yahoo(['BMA', 'GGAL', 'SUPV'], start='1/1/2017')

# %% ACCIONES TECH USA
mkt_usa = pdr.get_data_yahoo(['AAPL', 'TSLA', 'AMZN', 'FB', 'MSFT'], start='1/1/2018')
mkt_spx = pdr.get_data_yahoo('SP500', start='1/1/1980')

# %% BANCOS ARGENTINOS EN PESOS - 2010 EN ADELANTE
plt.plot(mkt_banks_arg.index, mkt_banks_arg['Adj Close'], label=['BMA', 'GGAL','SUPV'])
plt.legend()
plt.show()

#%% GALICIA EN PESOS - COLUMNAS DE APERTURA Y CIERRE
plt.plot(ggal.index, ggal[['Adj Close', 'Open']])
plt.show()

#%% GALICIA ADR - PORCENTAJE DE VARIACION DIARIA
plt.plot(ggal_adr_chg['2018':'2019'])
plt.show()

#%%
plt.plot(mkt_banks_adr.index, mkt_banks_adr['Adj Close'])
plt.show()

#%% clase UTDT
mkt = pdr.get_data_yahoo(['AAPL', 'AMZN','TSLA'], start='2018-01-01')
mkt_apple = mkt.loc[:, ('Adj Close','AAPL')]
aapl = pdr.get_data_yahoo('AAPL', start='2018-01-01')

retornos_appl_2018 = aapl.loc['2018','Adj Close'].pct_change().dropna().cumsum().plot()
retornos_appl_2019 = aapl.loc['2019','Adj Close'].pct_change().dropna().cumsum().plot()
retornos_appl_2020 = aapl.loc['2020','Adj Close'].pct_change().dropna().cumsum().plot()

#%% clase UTDT
## Medias moviles
## Media de 10 dias comenzando en 5 periodos

aapl = pdr.get_data_yahoo('AAPL', start='2018-01-01')

aapl['Adj Close'].rolling(10, min_periods=5).mean().plot()
aapl.loc[:,'Adj Close'].plot()

aapl['Adj Close'].rolling(30, min_periods=10).mean().plot()
aapl.loc[:,'Adj Close'].plot()

aapl['Adj Close'].rolling(50, min_periods=10).mean().plot()
aapl.loc[:,'Adj Close'].plot()

aapl['Adj Close'].rolling(55, min_periods=5).mean().plot()
aapl.loc[:,'Adj Close'].plot()

aapl['Adj Close'].rolling(75, min_periods=10).mean().plot()
aapl.loc[:,'Adj Close'].plot()

aapl['Adj Close'].rolling(100, min_periods=25).mean().plot()
aapl.loc[:,'Adj Close'].plot()

aapl['Adj Close'].rolling(120, min_periods=30).mean().plot()
aapl.loc[:,'Adj Close'].plot()

aapl['Adj Close'].rolling(150, min_periods=30).mean().plot()
aapl.loc[:,'Adj Close'].plot()

aapl['Adj Close'].rolling(200, min_periods=30).mean().plot()
aapl.loc[:,'Adj Close'].plot()

# %%
aapl1 = aapl.loc['2018-02-13':, 'Adj Close']
ma55 = aapl['Adj Close'].rolling(55, min_periods=5).mean().dropna()
ma55 = ma55.loc['2018-02-13':]
ma200 = aapl['Adj Close'].rolling(200, min_periods=30).mean().dropna()

ma200.plot()
aapl1.plot()

ma55.plot()
aapl1.plot()

# %% CORRELATIONS
import pandas_datareader as pdr
import pandas as pd

mkt = pdr.get_data_yahoo(['AAPL', 'AMZN','TSLA'], start='2018-01-01')

cagr_apple = mkt.loc[:, ('Adj Close', 'AAPL')].pct_change().dropna().cumsum()
cagr_tsla = mkt.loc[:, ('Adj Close', 'TSLA')].pct_change().dropna().cumsum()

## CORR EN T0
corr = cagr_apple.corr(cagr_tsla)
## PLOT HISTORICO
cagr_apple.rolling(50, min_periods=10).corr(cagr_tsla).plot()

# %%
spy = pdr.get_data_yahoo('SPY', start='2018-01-01')
cagr_spy = spy['Adj Close'].pct_change().cumsum().dropna()
cagr_apple.rolling(50, min_periods=10).corr(cagr_spy).corr(cagr_tsla).plot()