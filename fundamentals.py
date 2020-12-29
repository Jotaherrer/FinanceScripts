import yfinance, pandas as pd
import requests, datetime as dt
import bs4 as bs
import pickle

# Tickers
stocks = ['AAPL','ABEV','AMD','AMZN', 'BA','BABA', 'BBD', 'C','DESP','GOLD','HMY','INTC','JPM','KO','MELI','MSFT','NVDA','PBR', 'PFE','QCOM','TSLA','WFC']
adrs = ['BBAR','BMA', 'CEPU', 'CRESY', 'GGAL', 'PAM', 'SUPV', 'TGS', 'YPF']

# Obtaining SP500 Stocks
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

# Filter fundamental data for US stocks
stock_data = {}
for stock in tickers:
    if stock not in stock_data:
        a = yfinance.Ticker(stock)
        inf = a.info
        desired_keys = ['fullTimeExmployees', 'industry', 'previousClose', 'payoutRatio', 'beta', 'trailingPE', 'marketCap', 'averageVolume',
                        'priceToSalesTrailing12Months', 'fiftyTwoWeekHigh', 'forwardPE', 'fiftyTwoWeekLow', 'enterpriseToRevenue', 'profitMargins',
                        'enterpriseToEbitda', 'forwardEps', 'bookValue', 'heldPercentInstitutions', 'trailingEps', 'priceToBook', 'heldPercentInsiders',
                        'shortRatio', 'earningsQuarterlyGrowth', 'pegRatio']
        stock_data[stock] = {key: value for key, value in inf.items() if key in desired_keys}
        print('Ok storing {}'.format(stock))
    else:
        print('{} is already stored in the dictionary'.format(stock))

# Filter fundamental data for ARG stocks
stock_data_arg = {}
for stock in adrs:
    a = yfinance.Ticker(stock)
    inf = a.info
    desired_keys = ['fullTimeExmployees', 'industry', 'previousClose', 'payoutRatio', 'beta', 'trailingPE', 'marketCap', 'averageVolume',
                    'priceToSalesTrailing12Months', 'fiftyTwoWeekHigh', 'forwardPE', 'fiftyTwoWeekLow', 'enterpriseToRevenue', 'profitMargins',
                    'enterpriseToEbitda', 'forwardEps', 'bookValue', 'heldPercentInstitutions', 'trailingEps', 'priceToBook', 'heldPercentInsiders',
                    'shortRatio', 'earningsQuarterlyGrowth', 'pegRatio']
    stock_data_arg[stock] = {key: value for key, value in inf.items() if key in desired_keys}
    print('Ok storing {}'.format(stock))

with open('financial_data.p', 'wb') as f:
    pickle.dump(stock_data, f)

with open('financial_data.p', 'rb') as f:
    loaded_data = pickle.load(f)

# Testing results
loaded_data['WFC']
stock_data = loaded_data
stock_data['WFC']
stock_data_arg['GGAL']

### STORING SELECTED VARIABLES
# LAST PRICE US
last_price_us = []
for stock in stock_data:
    for item, value in stock_data[stock].items():
        if item == 'previousClose':
            last_price_us.append((stock, value))
# Testing last price
last_price_us

# LAST PRICE ARG
last_price_arg = []
for stock in stock_data_arg:
    for item, value in stock_data_arg[stock].items():
        if item == 'previousClose':
            last_price_arg.append((stock, value))
# Testing last price
last_price_arg

# MARKET CAP US
market_caps_us = []
for stock in stock_data:
    for item, value in stock_data[stock].items():
        if item =='marketCap':
            market_caps_us.append((stock, value))
#Testing market cap
market_caps_us
caps = pd.DataFrame(market_caps_us, columns=['Stock', 'Market Cap'])
caps.sort_values('Market Cap', ascending=False, inplace=True)
caps.reset_index(drop=True, inplace=True)
caps = caps[caps.Stock != 'GOOG'].reset_index(drop=True)
caps[:11]

# Creating dataframes for data
df_arg = pd.DataFrame(stock_data_arg)
df_spy = pd.DataFrame(stock_data)

# Sectors
test = pd.DataFrame(df_spy.iloc[0].values)
sectors = pd.DataFrame(test[0].unique())
test[0].unique()
len(test[0].unique())
