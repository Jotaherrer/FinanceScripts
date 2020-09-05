import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests, json, os, time
import pandas_datareader as pdr
import datetime as dt
import xlwings as xw
from pandas.tseries.offsets import Day, MonthEnd
import yfinance as yf

from api_config import usuario, password
from api_iol_recursiva import clean_assets

plt.style.use('fivethirtyeight')

def token_key(text):
    """
    Function that works out the received content to extract refreshed access token
    """
    content2 = str(text.split())
    beginning = content2.find('access_token":"') + int(15)
    end = content2.find('token_type') - int(3)
    access_token = content2[beginning:end]
    return access_token


def cedears_prices():
    """
    Gets prices from foreigne stocks trading locally.
    """
    url1 = "https://api.invertironline.com/token"

    data = {
            "username": usuario,
            "password": password,
            "grant_type": "password"        
    }
    response = requests.post(url1, data=data)
    if response.status_code == 200:
        content = response.text
        access_key = token_key(content)

        url2 = f'https://api.invertironline.com/api/v2/Cotizaciones/Acciones/CEDEARs/argentina'
        datos = requests.get(url2, headers={
                                        'Authorization': 'Bearer '+access_key
        })
        datos = json.loads(datos.text)
        datos = datos['titulos']
        datos = clean_assets(datos)
    return datos


def local_stocks_prices():
    """
    Gets prices from local stocks trading abroad.
    """
    url1 = "https://api.invertironline.com/token"

    data = {
            "username": usuario,
            "password": password,
            "grant_type": "password"        
    }
    response = requests.post(url1, data=data)
    if response.status_code == 200:
        content = response.text
        access_key = token_key(content)

        url2 = f'https://api.invertironline.com/api/v2/Cotizaciones/Acciones/Merval/argentina'
        datos = requests.get(url2, headers={
                                        'Authorization': 'Bearer '+access_key
        })
        datos = json.loads(datos.text)
        datos = datos['titulos']
        datos = clean_assets(datos)
    return datos


def local_bonds_prices():
    """
    Gets prices from local bonds trading locally.
    """
    url1 = "https://api.invertironline.com/token"

    data = {
            "username": usuario,
            "password": password,
            "grant_type": "password"        
    }
    response = requests.post(url1, data=data)
    if response.status_code == 200:
        content = response.text
        access_key = token_key(content)

        url2 = f'https://api.invertironline.com/api/v2/Cotizaciones/Bonos/Merval/argentina'
        datos = requests.get(url2, headers={
                                        'Authorization': 'Bearer '+access_key
        })
        datos = json.loads(datos.text)
        datos = datos['titulos']
        datos = clean_assets(datos)
    return datos


def prices(tickers):
    """
    Gets prices of US stocks from yahoo finance. Input a list of stocks or an individual asset as argument.
    """
    try:
        start = dt.datetime.today()
        start = start.strftime('%Y-%m-%d') 
        data = pdr.get_data_yahoo(tickers, start=start)
        price = data['Adj Close']
        vol = data['Volume']
        data_dic = {}
        for stock in tickers:
            data_dic[str(stock)] = price[str(stock)][0], vol[str(stock)][0]
        
        df_data = pd.DataFrame(data_dic.values(), columns=['precio_usa', 'volumen_usa'])
        df_data['Ticker'] = tickers
        df_data = df_data.loc[:,['Ticker', 'precio_usa', 'volumen_usa']]

    except:
        start = dt.datetime.today()
        start = start - Day(3)
        start = start.strftime('%Y-%m-%d') 
        data = pdr.get_data_yahoo(tickers, start=start)
        price = data['Adj Close']
        vol = data['Volume']
        data_dic = {}
        for stock in tickers:
            data_dic[str(stock)] = price[str(stock)][0], vol[str(stock)][0]
        
        df_data = pd.DataFrame(data_dic.values(), columns=['precio_usa', 'volumen_usa'])
        df_data['Ticker'] = tickers
        df_data = df_data.loc[:,['Ticker', 'precio_usa', 'volumen_usa']]

    return df_data


def excel(df_ccl, df_arg_stocks, df_bonds, df_arg_stocks_ccl):
    """
    Loads API prices data for an excel file for a better UI.
    """
    if os.path.exists('CCL.xlsx'):
        wb = xw.Book('CCL.xlsx')
        # SHEET CEDEARS
        ws = wb.sheets('CCL CEDEARs')
        ws.range('A1').expand().value = df_ccl
        # SHEET MERVAL
        ws_merval = wb.sheets('Merval')
        ws_merval.range('A1').expand().value = df_arg_stocks
        # SHEET BONOS
        ws_bonds = wb.sheets('Bonos')
        ws_bonds.range('A1').expand().value = df_bonds
        # SHEET CCL MERVAL
        ws_ccl = wb.sheets('CCL ADRs')
        ws_ccl.range('A1').expand().value = df_arg_stocks_ccl

        tiempo = time.asctime()
        print('Carga exitosa de datos. Ultima ejecución: ',tiempo)


hour = 11
while (hour >= 11) & (hour <= 20):
    ### TIME SET-UP
    now = time.localtime()
    hour = now[3]
    
    ### US STOCKS DATA
    stocks = ['AAPL','ABEV','AMD','AMZN', 'BA','BABA', 'BBD', 'C','DESP','GOLD','HMY','INTC','JPM','KO','MELI','MSFT','NVDA','PBR', 'PFE','QCOM','TSLA','WFC']
    spx_data = prices(stocks)
    adrs = ['BBAR','BMA', 'CEPU', 'CRESY', 'GGAL', 'PAM', 'SUPV', 'TGS', 'YPF']
    adrs_data = prices(adrs)

    arg_stocks_list = []
    for e, info in adrs_data.iterrows():
        ticker,precio,vol = info
        arg_stocks_list.append([ticker,precio,vol])
    for row in arg_stocks_list:
        if row[0] == 'CRESY':
            row[0] = 'CRES'
        elif row[0] == 'PAM':
            row[0] = 'PAMP'
        elif row[0] == 'YPF':
            row[0] = 'YPFD'
        elif row[0] == 'TGS':
            row[0] = 'TGSU2'
        else:
            continue 
    arg_stocks_df = pd.DataFrame(arg_stocks_list, columns=['Ticker', 'precio_adr', 'vol_adr'])
    factor_adrs = [('BBAR', 3), ('BMA', 10), ('CEPU', 10), ('CRES', 10), ('GGAL', 10), ('PAMP',25),('SUPV', 5), ('TGSU2', 5), ('YPFD', 1)]
    df_factor_adrs = pd.DataFrame(factor_adrs, columns=['Ticker', 'Factor'])

    ### ARG STOCKS DATA
    # BONDS
    bonds = local_bonds_prices()
    bonds = bonds[bonds['Cant. Ops.'] > 10]
    bonds.rename(columns={'Price': 'Local', 'Cant. Ops.':'Operaciones', 'Spread': 'Puntas'}, inplace=True)
    bonds = bonds.loc[:,['Ticker', 'Local','Q. Compra', 'Px. Compra', 'Px. Venta', 'Q. Venta','Operaciones', 'Puntas', 'Horario']]

    # STOCKS
    arg_stocks = local_stocks_prices()
    arg_stocks2 = local_stocks_prices()
    arg_stocks2.rename(columns={'Price': 'Precio_Local', 'Cant. Ops.':'Operaciones', 'Spread': 'Puntas'}, inplace=True)
    arg_stocks2 = arg_stocks2.loc[:,['Ticker', 'Precio_Local','Q. Compra', 'Px. Compra', 'Px. Venta', 'Q. Venta','Operaciones', 'Puntas', 'Horario']]
    ### MERGING STOCKS DATA
    adr_merge = arg_stocks_df.merge(arg_stocks, how='left').merge(df_factor_adrs,how='left')
    adr_merge_def = adr_merge.loc[:,['Ticker', 'precio_adr', 'Price', 'Q. Compra', 'Px. Compra', 'Px. Venta', 'Q. Venta', 'Cant. Ops.','Factor']]
    adr_merge_def.rename(columns={'precio_adr':'ADR', 'Price':'Local', 'Cant. Ops.': "Operaciones"}, inplace=True)
    adr_merge_def['CCL'] = adr_merge_def.apply(lambda row: round(row['Local']/row['ADR'] * row['Factor'],2), axis=1)
    adr_merge_def['Desvio'] = adr_merge_def.apply(lambda row: round(((row['CCL'] / np.mean(adr_merge_def['CCL']) - 1)),3), axis=1)

    adr_merge_def['CCL Venta'] = adr_merge_def['Px. Compra'] / adr_merge_def['ADR'] * adr_merge_def['Factor']
    adr_merge_def['Desvio V.'] = adr_merge_def.apply(lambda row: round(((row['CCL Venta'] / np.mean(adr_merge_def['CCL Venta']) - 1)),3), axis=1)

    adr_merge_def['CCL Compra'] = adr_merge_def['Px. Venta'] / adr_merge_def['ADR'] * adr_merge_def['Factor']
    adr_merge_def['Desvio C.'] = adr_merge_def.apply(lambda row: round(((row['CCL Compra'] / np.mean(adr_merge_def['CCL Compra']) - 1)),3), axis=1)

    # CEDEARS
    cedears = cedears_prices()
    cedears.rename(columns={'Price':'P','Px. Compra':'C', 'Px. Venta': 'V','Horario':'H'}, inplace=True)
    cedears = cedears.loc[:,['Ticker', 'P','Q. Compra','C', 'V', 'Q. Venta','H']]
    factores = [('AAPL',10),('ABEV', (1/3)),('AMD',0.5),('AMZN',72),('BA',3),('BABA',9),('BBD',1),('C', 3),('DESP',1),('GOLD',1),('HMY',1),('INTC',5),('JPM',5),('KO',5),('MELI',2),('MSFT',5),('NVDA',12),('PBR',1),('PFE',2),('QCOM',11),('TSLA',15),('WFC', 5)]
    df_fact = pd.DataFrame(factores, columns=['Ticker', 'factor'])
    ### MERGING CCL DATAFRAMES
    comb = spx_data.merge(cedears,how='left').merge(df_fact, how='left')
    combinado = comb.loc[:,['Ticker', 'precio_usa','P','Q. Compra','C', 'V', 'Q. Venta','H','factor']]
    combinado['CCL'] = combinado['P'] / combinado['precio_usa'] * combinado['factor']
    combinado['Desvio'] = combinado.apply(lambda row: round(((row['CCL'] / np.mean(combinado['CCL']) - 1)),3), axis=1)

    combinado['CCL Venta'] = combinado['C'] / combinado['precio_usa'] * combinado['factor']
    combinado['Desvio V.'] = combinado.apply(lambda row: round(((row['CCL Venta'] / np.mean(combinado['CCL Venta']) - 1)),3), axis=1)

    combinado['CCL Compra'] = combinado['V'] / combinado['precio_usa'] * combinado['factor']
    combinado['Desvio C.'] = combinado.apply(lambda row: round(((row['CCL Compra'] / np.mean(combinado['CCL Compra']) - 1)),3), axis=1)

    combinado.rename(columns={'precio_usa':'Px. USA', "P": 'Px. ARG.', 'C':'Px. Compra','V':'Px. Venta', 'H':'Horario', "factor": 'Factor'},inplace=True)

    ### EXCEL EXPORT FOR PREVIEW
    excel(combinado, arg_stocks2, bonds, adr_merge_def)
