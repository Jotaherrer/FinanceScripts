from math import exp, sqrt, log, pi
import os, time, xlwings as xw

from scipy.stats import norm
import pandas as pd
import numpy as np
from matplotlib.pyplot import plot 
import requests
import datetime as dt

from api_config import *
from api_iol import api, api_opciones, token_key, info_acciones
from api_iol_recursiva import parse_dates

class Options():
    def plot_payoff(self, lower_bound, upper_bound):
        """
        Metodo que grafica el payoff simulado de la opcion.
        """
        graph = range(lower_bound * 2, upper_bound * 2 + 1)
        plot([e/2 for e in graph], [self.payoff(e/2) for e in graph])


class VanillaOption(Options):
    def __init__(self, type, cost, strike):
        self.type = type
        self.strike = strike
        self.cost = cost

    def __repr__(self):
        return f'{self.type} @ Strike:{self.strike} @ Cost:{self.cost}'


class Call(VanillaOption):
    def __init__(self, cost, strike):
        super().__init__("Call", cost, strike)

    def payoff(self, price):
        if self.cost > 0:
            return -self.cost if price < self.strike else price - self.strike -self.cost
        else:
            return -self.cost if price < self.strike else (-price + self.strike)-self.cost 

    def be_price(self):
        """
        Calcula el precio break even de la posicion
        """
        if self.cost < 0:
            return self.strike - self.cost
        else:
            return self.strike + self.cost


class Put(VanillaOption):
    def __init__(self, cost, strike):
        super().__init__("Put", cost, strike)

    def payoff(self, price):
        if self.cost > 0:
            return self.strike-price-self.cost if price < self.strike else -self.cost
        else:
            return -self.cost if price > self.strike else -self.cost + (price - self.strike)

    def be_price(self):
        """
        Calcula el precio break even de la posicion
        """
        if self.cost < 0:
            return self.strike - self.cost
        else:
            return self.strike + self.cost

class Strategy(Options):
    def __init__(self, name):
        self.name = name
        self.positions = []

    def add_position(self, quantity, option):
        self.positions.append((quantity, option))

    def payoff(self,price):
        return sum([q * option.payoff(price) for q, option in self.positions])

    def __repr__(self):
        return self.name


def clean_data(data_opciones, call=True):
    """
    Function created to clean data stored in the API's format. Parameters:
    - data_opciones: Data input of option's information in the original format output provided by the external API.
    - call: Boolean object that has Calls as the default parameter, False is used for Puts info.
    """
    df = pd.DataFrame(data_opciones)
    calls = df[df.tipoOpcion == 'Call']
    puts = df[df.tipoOpcion == 'Put']

    if call:
        cotizaciones = calls.loc[:,['simbolo','cotizacion']]
        ticker = []
        for e in cotizaciones.simbolo:
            ticker.append(e)
        price = []
        for e in cotizaciones['cotizacion']:
            price.append(e)
        price = pd.DataFrame(price)
        last_price = []
        for e in price['ultimoPrecio']:
            last_price.append(e)
        vencimiento = []
        for e in cotizaciones.simbolo:
            vencimiento.append(e[-2:])
        vencimiento_df = pd.DataFrame(vencimiento)
        vencimiento_lista = list(vencimiento_df[0].unique())

        strikes_calls = []

        for e in ticker:
            if (e[3] == 'C') & (e[-2:] == vencimiento_lista[0]):
                word = e
                where = word.find('C')
                strike = word[where+1:where+4]
                if strike.find('.') == 2:
                    strike = strike[:2]
                    strikes_calls.append(int(strike))
                else:
                    strikes_calls.append(int(strike))
            elif (e[3] == 'C') & (e[-2:] == vencimiento_lista[1]):
                word = e
                where = word.find('C')
                strike = word[where+1:where+4]
                if strike.find('.') == 2:
                    strike = strike[:2]
                    strikes_calls.append(int(strike))
                else:
                    strikes_calls.append(int(strike))

            elif (e[3] == 'C') & (e[-2:] == vencimiento_lista[2]) | (e[-2:] == vencimiento_lista[3]):
                word = e
                where = word.find('C')
                strike = word[where+1:where+4]
                if strike.find('.') == 2:
                    strike = strike[:2]
                    strikes_calls.append(int(strike))
                else:
                    strikes_calls.append(int(strike))

        if len(last_price)==len(strikes_calls):
            comb = list(zip(last_price, strikes_calls, vencimiento))
            return comb
        else:
            return f'Error en importación de información para los Calls.'
    else:
        cotizaciones = puts.loc[:,['simbolo','cotizacion']]
        ticker = []
        for e in cotizaciones.simbolo:
            ticker.append(e)
        price = []
        for e in cotizaciones['cotizacion']:
            price.append(e)
        price = pd.DataFrame(price)
        last_price = []
        for e in price['ultimoPrecio']:
            last_price.append(e)
        vencimiento = []
        for e in cotizaciones.simbolo:
            vencimiento.append(e[-2:])
        vencimiento_df = pd.DataFrame(vencimiento)
        vencimiento_lista = list(vencimiento_df[0].unique())

        strikes_puts = []

        for e in ticker:
            if (e[3] == 'V') & (e[-2:] == vencimiento_lista[0]):
                word = e
                where = word.find('V')
                strike = word[where+1:where+4]
                if strike.find('.') == 2:
                    strike = strike[:2]
                    strikes_puts.append(int(strike))
                else:
                    strikes_puts.append(int(strike))
            elif (e[3] == 'V') & (e[-2:] == vencimiento_lista[1]):
                word = e
                where = word.find('V')
                strike = word[where+1:where+4]
                if strike.find('.') == 2:
                    strike = strike[:2]
                    strikes_puts.append(int(strike))
                else:
                    strikes_puts.append(int(strike))

            elif (e[3] == 'V') & (e[-2:] == vencimiento_lista[2]):
                word = e
                where = word.find('V')
                strike = word[where+1:where+4]
                if strike.find('.') == 2:
                    strike = strike[:2]
                    strikes_puts.append(int(strike))
                else:
                    strikes_puts.append(int(strike))

        if len(last_price)==len(strikes_puts):
            comb = list(zip(last_price, strikes_puts,vencimiento))
            return comb
        else:
            return f'Error en importacion de informacion para los Puts.'
    return comb


def excel(df, sheet_name):
    if os.path.exists('Options.xlsx'):
        wb = xw.Book('Options.xlsx')
        ws = wb.sheets(sheet_name)
        ws.range('A1').expand().value = df
        tiempo = time.asctime()
        print('Carga exitosa de datos. Ultima ejecucion: ',tiempo)


class Analysis():
    def __init__(self, spot, maturity, today, timedelta, risk_free, sigma):
        self.spot = spot
        self.maturity = maturity
        self.today = today
        self.timedelta = timedelta
        self.risk_free = risk_free
        self.sigma = sigma

    def black_scholes(self, spot, strike, maturity, risk_free, sigma):
        d1 = (log(spot/strike) + (risk_free + .5 * sigma ** 2) * maturity) / (sigma * sqrt(maturity))
        d2 = d1 - sigma * sqrt(maturity)
        bs_call = spot * norm.cdf(d1) - strike * exp(-risk_free * maturity) * norm.cdf(d2)
        bs_put = strike * exp(-risk_free * maturity) - spot + bs_call
        return (d1,d2,bs_call,bs_put)

    def greek_calls(self,spot,strike,maturity, risk_free, sigma):
        d1 = (log(spot/strike) + (risk_free + .5 * sigma ** 2) * maturity) / (sigma * sqrt(maturity))
        d2 = d1 - sigma * sqrt(maturity)
        delta = norm.cdf(d1)
        gamma = norm.pdf(d1) / (spot*sigma*sqrt(maturity))
        vega = spot * norm.pdf(d1) * sqrt(maturity)
        theta = -(spot * norm.pdf(d1) * sigma) / (2*sqrt(maturity)) - risk_free * strike * exp(-risk_free * maturity) * norm.cdf(d2)
        return [('delta',delta), ('gamma', gamma), ('vega', vega), ('theta', theta)]

    def greek_puts(self,spot,strike,maturity,risk_free, sigma):
        d1 = (log(spot/strike) + (risk_free + .5 * sigma ** 2) * maturity) / (sigma * sqrt(maturity))
        d2 = d1 - sigma * sqrt(maturity)
        delta = norm.cdf(-d1)
        gamma = norm.pdf(d1) / (spot * sigma * sqrt(maturity))
        vega = spot * norm.pdf(d1) * sqrt(maturity)
        theta = -(spot * norm.pdf(d1) * sigma) / (2*sqrt(maturity)) + risk_free * strike * exp(-risk_free * maturity) * norm.cdf(-d2)
        return [('delta',delta), ('gamma', gamma), ('vega', vega), ('theta', theta)]

    def implied_vol(self, option_price, spot, strike, maturity, risk_free, call=True):
        maximasIteraciones = 300
        pr_techo = option_price
        pr_piso = option_price
        vi_piso = maximasIteraciones
        vi = maximasIteraciones

        if call:
            for number in range(1,maximasIteraciones):
                sigma = (number)/100
                bs = self.black_scholes(spot, strike, maturity, risk_free, sigma)[2]
                if bs > option_price:
                    vi_piso = number - 1
                    pr_techo = bs
                    break
                else:
                    pr_piso = bs

            rango = (option_price - pr_piso) / (pr_techo - pr_piso)
            vi = (vi_piso + rango) / 100

        else:
            for number in range(1,maximasIteraciones):
                sigma = (number)/100
                bs = self.black_scholes(spot, strike, maturity, risk_free, sigma)[3]
                if bs > option_price:
                    vi_piso = number - 1
                    pr_techo = bs
                    break
                else:
                    pr_piso = bs

            rango = (option_price - pr_piso) / (pr_techo - pr_piso)
            vi = (vi_piso + rango) / 100 

        return vi

    def process_calls(self, data):
        """
        Insert as input the result of the function 'clean_data(mercado_opciones)' to process the market
        data in a Pandas DataFrame. Example: a1.process_calls(clean_data(mercado_opciones))
        """
        self.raw_calls = pd.DataFrame(data)
        self.raw_calls.rename(columns={0:'Prima', 1:'Strike', 2:'T'}, inplace=True)
        self.raw_calls = self.raw_calls[self.raw_calls.Prima != 0]
        self.raw_calls['Var. S/Spot'] = self.raw_calls.apply(lambda row: round((row['Strike']/self.spot - 1),2),axis=1)
        self.raw_calls['Condicion'] = self.raw_calls.apply(lambda row: ('OTM' if row['Strike'] > self.spot else 'ITM'),axis=1)
        self.raw_calls['Valor_Tiempo'] = self.raw_calls.apply(lambda row: (row['Prima'] / self.spot if row['Condicion'] == 'OTM' 
                                                                            else (row['Prima'] - (self.spot - row['Strike'])) / self.spot ), axis=1)
        self.raw_calls['TNA'] = self.raw_calls['Valor_Tiempo'] / self.timedelta 
        
        self.raw_calls['IV'] = self.raw_calls.apply(lambda row: (self.implied_vol(row['Prima'], self.spot, row['Strike'], self.timedelta, self.risk_free)), axis=1)
        self.raw_calls['B&S'] = self.raw_calls.apply(lambda row: (self.black_scholes(self.spot, row['Strike'], self.timedelta, self.risk_free, self.sigma)[2]), axis=1)

        self.raw_calls['Delta'] = self.raw_calls.apply(lambda row: (self.greek_calls(self.spot, row['Strike'], self.timedelta, self.risk_free, self.sigma)[0][1]), axis=1)
        self.raw_calls['Gamma'] = self.raw_calls.apply(lambda row: (self.greek_calls(self.spot, row['Strike'], self.timedelta, self.risk_free, self.sigma)[1][1]), axis=1)
        self.raw_calls['Vega'] = self.raw_calls.apply(lambda row: (self.greek_calls(self.spot, row['Strike'], self.timedelta, self.risk_free, self.sigma)[2][1]), axis=1)
        self.raw_calls['Theta'] = self.raw_calls.apply(lambda row: (self.greek_calls(self.spot, row['Strike'], self.timedelta, self.risk_free, self.sigma)[3][1]), axis=1)

        return self.raw_calls

    def process_puts(self, data):
        """
        Insert as input the result of the function 'clean_data(mercado_opciones)' to process the market
        data in a Pandas DataFrame. Example: a1.process_puts(clean_data(mercado_opciones, False))
        """
        self.raw_puts = pd.DataFrame(data)
        self.raw_puts.rename(columns={0:'Prima', 1:'Strike', 2:'T'}, inplace=True)
        self.raw_puts = self.raw_puts[self.raw_puts.Prima != 0]
        self.raw_puts['Var. S/Spot'] = self.raw_puts.apply(lambda row: round((row['Strike']/self.spot - 1),2),axis=1)
        self.raw_puts['Condicion'] = self.raw_puts.apply(lambda row: ('ITM' if row['Strike'] > self.spot else 'OTM'),axis=1)
        self.raw_puts['Valor_Tiempo'] = self.raw_puts.apply(lambda row: (row['Prima'] / self.spot if row['Condicion'] == 'OTM' 
                                                                            else (row['Prima'] - (self.spot - row['Strike'])) / self.spot ), axis=1)
        
        self.raw_puts['IV'] = self.raw_puts.apply(lambda row: (self.implied_vol(row['Prima'], self.spot, row['Strike'], self.timedelta, self.risk_free, False)), axis=1)
        self.raw_puts['B&S'] = self.raw_puts.apply(lambda row: (self.black_scholes(self.spot, row['Strike'], self.timedelta, self.risk_free, self.sigma)[3]), axis=1)

        self.raw_puts['Delta'] = self.raw_puts.apply(lambda row: (self.greek_puts(self.spot, row['Strike'], self.timedelta, self.risk_free, self.sigma)[0][1]), axis=1)
        self.raw_puts['Gamma'] = self.raw_puts.apply(lambda row: (self.greek_puts(self.spot, row['Strike'], self.timedelta, self.risk_free, self.sigma)[1][1]), axis=1)
        self.raw_puts['Vega'] = self.raw_puts.apply(lambda row: (self.greek_puts(self.spot, row['Strike'], self.timedelta, self.risk_free, self.sigma)[2][1]), axis=1)
        self.raw_puts['Theta'] = self.raw_puts.apply(lambda row: (self.greek_puts(self.spot, row['Strike'], self.timedelta, self.risk_free, self.sigma)[3][1]), axis=1)

        return self.raw_puts

    def merge_opts(self):
        calls = self.process_calls(clean_data(mercado_opciones))
        calls = calls.loc[:,['Strike','Prima','T']]
        calls.rename(columns={'Prima':"Prima Calls"}, inplace=True)
        puts = self.process_puts(clean_data(mercado_opciones, False))
        puts = puts.loc[:,['Strike', 'Prima','T']]
        puts.rename(columns={'Prima':"Prima Puts"}, inplace=True)
        combined = pd.merge(calls, puts, how='left')

        combined['Paridad - Calls'] = combined.apply(lambda row: (self.spot + row['Prima Puts'] - row['Strike'] * exp(-self.timedelta*self.risk_free)), axis=1) 
        combined['Paridad - Puts'] = combined.apply(lambda row: (row['Prima Calls'] + row['Strike'] * exp(-self.timedelta * self.risk_free) - self.spot),axis=1)
        combined['Call Arbitrage'] = round((combined['Prima Calls'] - combined['Paridad - Calls']) / -combined['Prima Calls'],2)
        combined['Put Arbitrage'] = round((combined['Prima Puts'] - combined['Paridad - Puts']) / -combined['Prima Puts'],2)

        return combined


if __name__ == '__main__':
    hour = 11
    while (hour >= 11) & (hour <= 20):
        now = time.localtime()
        hour = now[3]

        url = "https://api.invertironline.com/token"
        data = {
            "username": usuario,        # IMPORTO DE API_CONFIG.PY
            "password": password,       # IMPORTO DE API_CONFIG.PY
            "grant_type": "password"        
        }
        response = requests.post(url, data=data)

        if response.status_code == 200:
            content = response.text
            access_key = token_key(content)

            mercado_acciones = api('Acciones', 'Merval', 'argentina', access_key)
            mercado_opciones = api_opciones('bCBA', 'ggal', access_key)
            ggal = info_acciones(mercado_acciones,'GGAL')[0]
            ggal_maturity = dt.datetime.strptime(mercado_opciones[10]['descripcion'][-10:], '%d/%m/%Y')
            today = dt.datetime.today()
            maturity = (ggal_maturity-today).days / 365.

        a1 = Analysis(ggal, ggal_maturity, today, maturity, 0.25, 0.69)
        calls = a1.process_calls(clean_data(mercado_opciones))
        puts = a1.process_puts(clean_data(mercado_opciones, False))
        merged_data = a1.merge_opts()

        c1 = Call(clean_data(mercado_opciones)[0][0], clean_data(mercado_opciones)[0][1])
        c2 = Call(clean_data(mercado_opciones)[1][0], clean_data(mercado_opciones)[1][1])
        c3 = Call(clean_data(mercado_opciones)[2][0], clean_data(mercado_opciones)[2][1])
        c4 = Call(clean_data(mercado_opciones)[3][0], clean_data(mercado_opciones)[3][1])
        c5 = Call(clean_data(mercado_opciones)[4][0], clean_data(mercado_opciones)[4][1])
        c6 = Call(clean_data(mercado_opciones)[5][0], clean_data(mercado_opciones)[5][1])
        c7 = Call(clean_data(mercado_opciones)[6][0], clean_data(mercado_opciones)[6][1])

        PARAMS = {'spot': ggal, 'strike': c1.strike, 'plazo': 180, 'risk_free': 0.01,'sigma': 0.1, 'div': 0}

        s1 = Strategy('Bullspread de calls')
        s1.add_position(10, c1)
        s1.add_position(-10, c2)
        #s1.plot_payoff(60,160)
            
        
        excel(calls, 'C-VAL')
        excel(puts, 'P-VAL')
        excel(merged_data,'Parity')
        