# Imports
"""
https://www.holisticseo.digital/python-seo/google-trends/
https://pypi.org/project/pytrends/
"""
import pytrends, pandas as pd
from pytrends.request import TrendReq
import matplotlib.pyplot as plt
import pandas_datareader as pdr
import numpy as np
from datetime import datetime, timedelta

# Arg prices
ypf_adr = pdr.get_data_yahoo('YPF', start='1/1/2020')
ypf_adr = ypf_adr.loc[:,'Adj Close'].reset_index()
ypf_adr.set_index('Date', inplace=True)
ypf_adr.rename(columns={'Adj Close': 'ADR'},inplace=True)
ypf_local = pdr.get_data_yahoo('YPFD.BA', start='1/1/2020')
ypf_local = ypf_local.loc[:,'Adj Close'].reset_index()
ypf_local.set_index('Date', inplace=True)
ypf_local.rename(columns={'Adj Close': 'Local'}, inplace=True)
ccl = pd.concat([ypf_adr, ypf_local], axis=1)
ccl['CCL'] = ccl['Local'] / ccl['ADR']
ccl = ccl.dropna()
ccl = ccl.reset_index()
ccl

# Create instance of the Trend Object
pytrend = TrendReq()
# Build keyword list
kw_list2 = ['dolar', 'blue', 'coronavirus']
pytrend.build_payload(kw_list=kw_list2, cat=0, timeframe='today 12-m', geo='AR', gprop='')
interest = pytrend.interest_over_time()
interest = interest.reset_index()

dates = interest.date.values
newdate = [pd.to_datetime(d) + timedelta(3) for d in dates]
interest['date'] = newdate
interest

# 3-month case
pytrend2 = TrendReq()
kw_list = ['dolar', 'blue', 'coronavirus']
pytrend2.build_payload(kw_list, cat=0, timeframe='today 3-m', geo='AR')
daily_interest = pytrend2.interest_over_time()
daily_interest = daily_interest.reset_index()
daily_interest

# 3-month inflation
pytrend3 = TrendReq()
kw_list3 = ['inflacion']
pytrend3.build_payload(kw_list3, cat=0, timeframe='today 3-m', geo='AR')
inflation = pytrend3.interest_over_time()
inflation = daily_interest.reset_index()
inflation


# Daily search trends
arg_trend = pytrend.trending_searches(pn='argentina')
arg_trend.head(40)
us_trend = pytrend.trending_searches(pn='united_states')
us_trend.head(40)


# Today's trend
df_today_arg = pytrend.today_searches(pn='AR')
df_today_arg
df_today_us = pytrend.today_searches(pn='US')
df_today_us


# Plot
fig, ax1 = plt.subplots(figsize=(15,10))

ax2 = ax1.twinx()
ax1.plot(interest['date'], interest['dolar'], label='Búsquedas Dolar', marker='*', color='g')
ax2.plot(ccl['Date'], ccl['CCL'], label='CCL', color='b')

ax1.set_ylabel('Cantidad de búsquedas', color='g', fontsize=12)
ax2.set_ylabel('Tipo de cambio CCL', color='b', fontsize=12)

plt.title('Google Trends 2020', size=17)
plt.legend()
plt.show()


# Top charts
df_charts = pytrend.top_charts(2020, hl='en-US', tz=300, geo='GLOBAL')
df_charts
df_charts_arg = pytrend.top_charts(2020, hl='en-US', tz=300, geo='AR')
df_charts_arg

