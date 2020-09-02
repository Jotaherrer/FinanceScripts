from montecarlo import montecarlo_difusion, montecarlo_binominal
from opciones import Analysis
import datetime as dt
from math import log, exp, sqrt

s0 = 100
k_list_1 = list(range(40,170,10))
k_list_2 = list(range(70,131,5))
sigma = 0.3
r = 0.045 
maturity = 1/12
n = 30
simulations = 20000
today = dt.datetime.today()

### BLACK & SCHOLES CALCULATION WITH OOP SCRIPT
test_analysis = Analysis(s0,maturity,today,maturity,r,sigma)

### CALCULATE CALLS AND PUTS VALUES FOR LIST 1 OF STRIKE PRICES
c_1 = [test_analysis.black_scholes(s0,e,maturity,r,sigma)[2] for e in k_list_1]
p_1 = [test_analysis.black_scholes(s0,e,maturity,r,sigma)[3] for e in k_list_1]

### CALCULATE VIX PARAMETERS FOR LIST 1 OF STRIKES
s_star_1 = []
for k in k_list_1:
    a = abs(s0 * exp(r*maturity) - k)
    s_star_1.append((k, a))
    for e in s_star_1:
        if e[1] > a:
            s_star_1.remove(e)
        else:
            if (e[1] > 3):
                s_star_1.remove(e)
s_star_1_value = s_star_1[0][0]

puts_value_1 = []    
for i in range(1,6):
    first_p1 = ((k_list_1[i+1] - k_list_1[i-1]) / 2) / (k_list_1[i] ** 2) * p_1[i]
    puts_value_1.append(first_p1)
suma_puts_1 = sum(puts_value_1)

calls_value_1 = []
for i in range(6,12):
    first_c1 = (((k_list_1[i+1] - k_list_1[i-1]) / 2) / (k_list_1[i] ** 2)) * c_1[i]
    calls_value_1.append(first_c1)
suma_calls_1 = sum(calls_value_1)

power_vix_1 = ((suma_puts_1 + suma_calls_1) * 2 * exp(r*maturity) / maturity) - 1/maturity * ((s0 * exp(r*maturity)/s_star_1_value) - 1) ** 2 
vix_1 = sqrt(power_vix_1)

### CALCULATE CALLS AND PUTS VALUES FOR LIST 2 OF STRIKE PRICES
s_star_2 = []
c_2 = [test_analysis.black_scholes(s0,e,maturity,r,sigma)[2] for e in k_list_2]
p_2 = [test_analysis.black_scholes(s0,e,maturity,r,sigma)[3] for e in k_list_2]

### CALCULATE VIX PARAMETERS FOR LIST 2 STRIKES
for k in k_list_2:
    a = abs(s0 * exp(r*maturity) - k)
    s_star_2.append((k, a))
    for e in s_star_2:
        if e[1] > a:
            s_star_2.remove(e)
        else:
            if (e[1] > 3):
                s_star_2.remove(e)
s_star_2_value = s_star_2[0][0]


puts_value_2 = []    
for i in range(1,6):
    first_p2 = ((k_list_2[i+1] - k_list_2[i-1]) / 2) / (k_list_2[i] ** 2) * p_2[i]
    puts_value_2.append(first_p2)
suma_puts_2 = sum(puts_value_1)

calls_value_2 = []
for i in range(6,12):
    first_c2 = (((k_list_2[i+1] - k_list_2[i-1]) / 2) / (k_list_2[i] ** 2)) * c_2[i]
    calls_value_2.append(first_c2)
suma_calls_2 = sum(calls_value_2)

power_vix_2 = ((suma_puts_2 + suma_calls_2) * 2 * exp(r*maturity) / maturity) - 1/maturity * ((s0 * exp(r*maturity)/s_star_2_value) - 1) ** 2 
vix_2 = sqrt(power_vix_2)

print(f'Valuacion VIX - Case 1: {round(vix_1,4)}\nValuacion VIX - Case 2: {round(vix_2,4)}\nSigma: {sigma}')