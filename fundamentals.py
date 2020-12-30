import yfinance, pandas as pd
import requests, datetime as dt
import bs4 as bs
import pickle
import xlwings as xw


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
market_caps_us, payout_ratio, betas, trail_pe, avg_vol, price_to_sales, fifty_w_high, forw_pe, fifty_w_low, profit_margin, e_to_ebitda, e_to_rev, forw_eps, book_value, inst, trail_eps, p_to_book, short, peg = [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []
for stock in stock_data:
    for item, value in stock_data[stock].items():
        if item =='marketCap':
            market_caps_us.append((stock, value))
        elif item == 'payoutRatio':
            payout_ratio.append((stock, value))
        elif item == "beta":
            betas.append((stock, value))
        elif item == "trailingPE":
            trail_pe.append((stock, value))
        elif item == "averageVolume":
            avg_vol.append((stock, value))
        elif item == "priceToSalesTrailing12Months":
            price_to_sales.append((stock, value))
        elif item == "fiftyTwoWeekHigh":
            fifty_w_high.append((stock, value))
        elif item == "forwardPE":
            forw_pe.append((stock, value))
        elif item == "fiftyTwoWeekLow":
            fifty_w_low.append((stock, value))
        elif item == "profitMargins":
            profit_margin.append((stock, value))
        elif item == "enterpriseToEbitda":
            e_to_ebitda.append((stock, value))
        elif item == "enterpriseToRevenue":
            e_to_rev.append((stock, value))
        elif item == "forwardEps":
            forw_eps.append((stock, value))
        elif item == "bookValue":
            book_value.append((stock, value))
        elif item == "heldPercentInstitutions":
            inst.append((stock, value))
        elif item == "trailingEps":
            trail_eps.append((stock, value))
        elif item == "priceToBook":
            p_to_book.append((stock, value))
        elif item == "shortRatio":
            short.append((stock, value))
        elif item == "pegRatio":
            peg.append((stock, value))
#Testing market cap
caps = pd.DataFrame(market_caps_us, columns=['Stock', 'Market Cap'])
payout = pd.DataFrame(payout_ratio, columns=['Stock', 'Payout Ratio'])
beta = pd.DataFrame(betas, columns=['Stock', 'Beta'])
trailing_pe = pd.DataFrame(trail_pe, columns=['Stock', 'Trailing PE'])
average_vol = pd.DataFrame(avg_vol, columns=['Stock', 'Average Volume'])
price_sales = pd.DataFrame(price_to_sales, columns=['Stock', 'Price/Sales'])
fifty_high = pd.DataFrame(fifty_w_high, columns=['Stock', '55w High'])
forward_pe = pd.DataFrame(forw_pe, columns=['Stock', 'Forward PE'])
fifty_low = pd.DataFrame(fifty_w_low, columns=['Stock', '55w Low'])
profit_margin = pd.DataFrame(profit_margin, columns=['Stock', 'Profit Margin'])
enter_ebitda = pd.DataFrame(e_to_ebitda, columns=['Stock', 'EV/EBITDA'])
enter_rev = pd.DataFrame(e_to_rev, columns=['Stock', 'EV/Revenue'])
forward_eps = pd.DataFrame(forw_eps, columns=['Stock', 'Forward EPS'])
book_value = pd.DataFrame(book_value, columns=['Stock', 'Book Value'])
institutionals = pd.DataFrame(inst, columns=['Stock', '% Institutionals'])
trailing_eps = pd.DataFrame(trail_eps, columns=['Stock', 'Trailing EPS'])
price_to_book = pd.DataFrame(p_to_book, columns=['Stock', 'Price/Book Value'])
short_ratio = pd.DataFrame(short, columns=['Stock', 'Short ratio'])
peg_ratio = pd.DataFrame(peg, columns=['Stock', 'PEG ratio'])

# Combining dataframes
merged = caps.merge(payout, on='Stock').merge(beta, on='Stock').merge(trailing_pe, on='Stock').merge(average_vol, on='Stock').merge(price_sales, on='Stock').merge(fifty_high, on='Stock').merge(fifty_low, on='Stock').merge(forward_pe, on='Stock').merge(profit_margin, on='Stock').merge(enter_ebitda, on='Stock').merge(enter_rev, on='Stock').merge(forward_eps, on='Stock').merge(book_value, on='Stock').merge(institutionals, on='Stock').merge(trailing_eps, on='Stock').merge(price_to_book, on='Stock').merge(short_ratio, on='Stock').merge(peg_ratio, on='Stock')
merged_mkt_cap = merged.sort_values('Market Cap', ascending=False).reset_index(drop=True)
merged_mkt_cap = merged_mkt_cap[merged_mkt_cap.Stock != 'GOOG'].reset_index(drop=True)
merged_mkt_cap[:11]

# Creating dataframes for data
df_arg = pd.DataFrame(stock_data_arg)
df_spy = pd.DataFrame(stock_data)

# Sectors
test = pd.DataFrame(df_spy.iloc[0].values)
sectors = pd.DataFrame(test[0].unique())
test[0].unique()
len(test[0].unique())

# Envio a excel
def excel(market_data):
    """
    """
    if os.path.exists('fundamental_data.xlsx'):
        wb = xw.Book('fundamental_data.xlsx')
        ws = wb.sheets('Fundamentals')
        ws.range('A1').expand().value = market_data
        print('Carga exitosa de datos!')

excel(merged_mkt_cap)