import seaborn as sns
import pandas_datareader.data as pdr
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt

### IMPORT DATA US STOCKS / ARG CEDEARS 
cedears = ['AAPL.BA', 'ABEV.BA', 'ABT.BA', 'AMD.BA', 'AMZN.BA', 'ARCO.BA', 'AUY.BA', 'AXP.BA', 'AZN.BA', 'BA.BA','BABA.BA', 'BBD.BA', 
          'BCS.BA','C.BA','CSCO.BA','CVX.BA','DESP.BA', 'DISN.BA','EBAY.BA','ERJ.BA','FB.BA','GE.BA','GGB.BA','GILD.BA', 'GLNT.BA'
          'GOLD.BA','GOOGL.BA', 'GSK.BA','HMY.BA','IBM.BA','INTC.BA','ITUB.BA','JNJ.BA','JPM.BA','KO.BA','MCD.BA','MELI.BA','MMM.BA',
          'MSFT.BA','NFLX.BA','NKE.BA','NVDA.BA','PBR.BA','PFE.BA','PG.BA','QCOM.BA','SNAP.BA','T.BA','TEN.BA','TRIP.BA','TSLA.BA','TWTR.BA',
          'V.BA','VALE.BA','WFC.BA','WMT.BA','X.BA','XOM.BA']

stocks = ['AAPL', 'ABEV', 'ABT', 'AMD', 'AMZN', 'ARCO', 'AUY', 'AXP', 'AZN', 'BA','BABA', 'BBD', 
          'BCS','C','CSCO','CVX','DESP', 'DIS','EBAY','ERJ','FB','GE','GGB','GILD', 'GLOB'
          'GOLD','GOOGL', 'GSK','HMY','IBM','INTC','ITUB','JNJ','JPM','KO','MCD','MELI','MMM',
          'MSFT','NFLX','NKE','NVDA','PBR','PFE','PG','QCOM','SNAP','T','TS','TRIP','TSLA','TWTR',
          'V','VALE','WFC','WMT','X','XOM']

locales = []

start = dt.datetime(2018,1,1)
start = start.strftime('%Y-%m-%d')

def get_data(stock):
    info = pdr.get_data_yahoo(stock, start=str(start))
    return info

def work_data(stock):
    worked_data = stock.loc[:,'Adj Close'].pct_change().dropna()
    worked_data = pd.DataFrame(worked_data)
    worked_data.rename(columns={'Adj Close': 'rets'}, inplace=True)
    return worked_data

def process_data(stock):
    variable = get_data(str(stock))
    variable = work_data(variable)
    return variable

aapl = process_data('aapl')
abev = process_data('abev')
abt = process_data('abt')
amd = process_data('amd')
amzn = process_data('amzn')
arco = process_data('arco')     # 2012  en adelante
auy = process_data('auy')
axp = process_data('axp')
ba = process_data('ba')
baba = process_data('baba')     # 2014-09 en adelante
bbd = process_data('bbd')
bcs = process_data('bcs')
c = process_data('c')
csco = process_data('csco')
cvx = process_data('cvx')
desp = process_data('desp')     # 2017-09 en adelante
disn = process_data('dis')
ebay = process_data('ebay')
erj = process_data('erj')
fb = process_data('fb')         # 2012-05 en adelante
ge = process_data('ge')
ggb = process_data('ggb')
gild = process_data('gild')
glob = process_data('glob')     # 2014-07 en adelante
gold = process_data('gold')   
googl = process_data('googl')
gsk = process_data('gsk')
hmy = process_data('hmy')
ibm = process_data('ibm')
intc = process_data('intc')
itub = process_data('itub')
jnj = process_data('jnj')
jpm = process_data('jpm')
ko = process_data('ko')
mcd = process_data('mcd')
meli = process_data('meli')     # 2007-08 en adelante
mmm = process_data('mmm')
msft = process_data('msft')
nflx = process_data('nflx')     
nke = process_data('nke')
nvda = process_data('nvda')
pbr = process_data('pbr')
pfe = process_data('pfe')
pg = process_data('pg')
qcom = process_data('qcom')
snap = process_data('snap')     # 2017-03 en adelante
t = process_data('t')
ts = process_data('ts')
trip = process_data('trip')     # 2011-12 en adelante
tsla = process_data('tsla')     # 2010-06 en adelante
twtr = process_data('twtr')     # 2013-11 en adelante
v = process_data('v')           # 2008-03 en adelante
vale = process_data('vale')
wfc = process_data('wfc')
wmt = process_data('wmt')
x = process_data('x')
xom = process_data('xom')

### CARTERA GLOBAL - 2006/ACTUAL
corrs_hist = np.corrcoef([aapl['rets'],abev['rets'],abt['rets'],amd['rets'],amzn['rets'],auy['rets'],axp['rets'],ba['rets'],baba['rets'],bbd['rets'],
                          bcs['rets'],c['rets'], csco['rets'],cvx['rets'],desp['rets'],disn['rets'],ebay['rets'],fb['rets'],erj['rets'],ge['rets'],ggb['rets'],
                          gild['rets'],glob['rets'],['rets'], googl['rets'],gsk['rets'],hmy['rets'],ibm['rets'],intc['rets'],itub['rets'],jnj['rets'], meli['rets'],
                          jpm['rets'],ko['rets'],mcd['rets'],mmm['rets'],msft['rets'],nflx['rets'],nke['rets'],nvda['rets'],pbr['rets'],
                          pfe['rets'],pg['rets'],snap['rets'],qcom['rets'],t['rets'],ts['rets'],tsla['rets'],twtr['rets'],v['rets'],vale['rets'],wfc['rets'],wmt['rets'],x['rets'],xom['rets']])

legend=['AAPL', 'ABEV', 'ABT', 'AMD', 'AMZN', 'AUY', 'AXP', 'BA', 'BABA','BBD','BCS','C','CSCO','CVX','DESP','DIS','EBAY','ERJ','FB','ERJ','GE','GGB','GILD', 'GLOB',
          'GOLD','GOOGL', 'GSK','HMY','IBM','INTC','ITUB','JNJ','MELI','JPM','KO','MCD','MELI','MMM','MSFT','NFLX','NKE','NVDA','PBR','PFE',
          'PG','SNAP','QCOM','T','TS','TSLA','TWTR','VISA','VALE','WFC','WMT','X','XOM']

fig = plt.figure(figsize=(35,35))
ax1 = fig.subplots()
sns.heatmap(corrs_hist,xticklabels=legend, yticklabels=legend, annot=True,cmap='Reds')
plt.savefig("corrs.png")
plt.close('all')

### CARTERA GLOBAL - 2006/ACTUAL
corr_actual = np.corrcoef([gold['rets'],msft['rets'],pbr['rets'],jpm['rets']])
legend_actual = ['GOLD','MSFT','PBR','JPMC']
fig2 = plt.figure(figsize=(10,10))
ax2 = fig2.subplots()
sns.heatmap(corr_actual,xticklabels=legend_actual, yticklabels=legend_actual, annot=True,cmap='Reds')
plt.savefig("corrs_actual.png")
plt.close('all')

### CARTERA GLOBAL - 2018/ACTUAL
corrs_2018 = np.corrcoef([aapl['rets'],abev['rets'],abt['rets'],amd['rets'],amzn['rets'],auy['rets'],axp['rets'],ba['rets'],bbd['rets'],
                          bcs['rets'],c['rets'], csco['rets'],cvx['rets'],disn['rets'],ebay['rets'],erj['rets'],ge['rets'],ggb['rets'],
                          gild['rets'],gold['rets'], googl['rets'],gsk['rets'],hmy['rets'],ibm['rets'],intc['rets'],itub['rets'],jnj['rets'],
                          jpm['rets'],ko['rets'],mcd['rets'],mmm['rets'],msft['rets'],nflx['rets'],nke['rets'],nvda['rets'],pbr['rets'],
                          pfe['rets'],pg['rets'],qcom['rets'],t['rets'],ts['rets'],vale['rets'],wfc['rets'],wmt['rets'],x['rets'],xom['rets']])

legend_2018=['AAPL', 'ABEV', 'ABT', 'AMD', 'AMZN', 'AUY', 'AXP', 'BA', 'BBD','BCS','C','CSCO','CVX','DIS','EBAY','ERJ','GE','GGB','GILD',
            'GOLD','GOOGL', 'GSK','HMY','IBM','INTC','ITUB','JNJ','JPM','KO','MCD','MELI','MMM','MSFT','NFLX','NKE','NVDA','PBR','PFE',
            'PG','QCOM','T','TS','VALE','WFC','WMT','X','XOM']
            
fig2018 = plt.figure(figsize=(35,35))
ax2018 = fig2018.subplots()
sns.heatmap(corrs_2018,xticklabels=legend_2018, yticklabels=legend_2018, annot=True,cmap='Reds')
plt.savefig("corrs_2018.png")
plt.close('all')
