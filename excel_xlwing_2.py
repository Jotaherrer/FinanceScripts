import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
import pandas_datareader as pdr
import datetime as dt
import json
import os
import time
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

def get_access():
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

def prices(tickers):
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

def excel(df):
    if os.path.exists('CCL.xlsx'):
        wb = xw.Book('CCL.xlsx')
        ws = wb.sheets('Cotizaciones')
        ws.range('A1').expand().value = df
        tiempo = time.asctime()
        print('Carga exitosa de datos. Ultima ejecucion: ',tiempo)

hour = 11

while (hour >= 11) & (hour <= 20):
    now = time.localtime()
    hour = now[3]
    
    stocks = ['AAPL','AMD','AMZN', 'BA','BABA', 'BBD', 'C','DESP','GOLD','HMY','JPM','KO','MELI','MSFT','NVDA','PBR', 'PFE','QCOM','TSLA','WFC']
    spx_data = prices(stocks)

    cedears = get_access()
    cedears.rename(columns={'Price':'P','Px. Compra':'C', 'Px. Venta': 'V','Horario':'H'}, inplace=True)
    cedears = cedears.loc[:,['Ticker', 'P','C', 'V','H']]
    factores = [('AAPL',10),('AMD',0.5),('AMZN',72),('BA',3),('BABA',9),('BBD',1),('C', 3),('DESP',1),('GOLD',1),('HMY',1),('JPM',5),('KO',5),('MELI',2),('MSFT',5),('NVDA',12),('PBR',1),('PFE',2),('QCOM',11),('TSLA',15),('WFC', 5)]
    df_fact = pd.DataFrame(factores, columns=['Ticker', 'factor'])

    comb = spx_data.merge(cedears,how='left').merge(df_fact, how='left')
    combinado = comb.loc[:,['Ticker', 'precio_usa','P','C','V','H','factor']]
    combinado['CCL'] = combinado['P'] / combinado['precio_usa'] * combinado['factor']
    combinado['Desvio'] = combinado.apply(lambda row: round(((row['CCL'] / np.mean(combinado['CCL']) - 1)),3), axis=1)

    combinado['CCL Venta'] = combinado['C'] / combinado['precio_usa'] * combinado['factor']
    combinado['Desvio V.'] = combinado.apply(lambda row: round(((row['CCL Venta'] / np.mean(combinado['CCL Venta']) - 1)),3), axis=1)

    combinado['CCL Compra'] = combinado['V'] / combinado['precio_usa'] * combinado['factor']
    combinado['Desvio C.'] = combinado.apply(lambda row: round(((row['CCL Compra'] / np.mean(combinado['CCL Compra']) - 1)),3), axis=1)

    combinado.rename(columns={'precio_usa':'Px. USA', "P": 'Px. ARG.', 'C':'Px. Compra','V':'Px. Venta', "factor": 'Factor'},inplace=True)

    if (np.min(combinado['Desvio C.'] < -.01)) | (np.min(combinado['Desvio'] < -.015)):
        print('Potencial Arbitraje')

    excel(combinado)
