import yfinance, pandas as pd

# Tickers
stocks = ['AAPL','ABEV','AMD','AMZN', 'BA','BABA', 'BBD', 'C','DESP','GOLD','HMY','INTC','JPM','KO','MELI','MSFT','NVDA','PBR', 'PFE','QCOM','TSLA','WFC']
adrs = ['BBAR','BMA', 'CEPU', 'CRESY', 'GGAL', 'PAM', 'SUPV', 'TGS', 'YPF']

# Filter fundamental data for US stocks
stock_data = {}
for stock in stocks:
    a = yfinance.Ticker(stock)
    inf = a.info
    desired_keys = ['fullTimeExmployees', 'industry', 'previousClose', 'payoutRatio', 'beta', 'trailingPE', 'marketCap', 'averageVolume',
                    'priceToSalesTrailing12Months', 'fiftyTwoWeekHigh', 'forwardPE', 'fiftyTwoWeekLow', 'enterpriseToRevenue', 'profitMargins',
                    'enterpriseToEbitda', 'forwardEps', 'bookValue', 'heldPercentInstitutions', 'trailingEps', 'priceToBook', 'heldPercentInsiders',
                    'shortRatio', 'earningsQuarterlyGrowth', 'pegRatio']
    stock_data[stock] = {key: value for key, value in inf.items() if key in desired_keys}
    print('Ok storing {}'.format(stock))

# Testing results
stock_data['AAPL']

# Storing last price
last_price_us = []
for stock in stock_data:
    for item, value in stock_data[stock].items():
        if item == 'previousClose':
            last_price_us.append((stock, value))
# Testing last price
last_price_us

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

# Testing results
stock_data_arg['GGAL']

# Storing last price
last_price_arg = []
for stock in stock_data_arg:
    for item, value in stock_data_arg[stock].items():
        if item == 'previousClose':
            last_price_arg.append((stock, value))
# Testing last price
last_price_arg

