from montecarlo import montecarlo_difusion, montecarlo_binominal
from opciones import Analysis
import datetime as dt
import numpy as np
from math import log, exp, sqrt
import matplotlib.pyplot as plt

### PARAMETERS
s0 = 100
sigma = 0.3
r = 0.045 
maturity = 1/12
n = 30
simulations = 20000
delta = maturity/n
m = r - sigma**2 / 2

### FUNCTION TO CREATE 'M' SIMULATIONS OF PAYOFFS ON 'N' TRADING PERIODS
def create_sim(s0,r,sigma,n):
    st = s0    

    def generate_value():
        nonlocal st
        final_pfs = []

        for i in range(n):
            if i == 0:
                st = st * exp(m * delta + sigma * sqrt(delta) * np.random.randn())
                pf = log(st/s0) ** 2
                final_pfs.append(pf)
            else:
                sf = st * exp(m * delta + sigma * sqrt(delta) * np.random.randn()) 
                pf = log(sf/st) ** 2
                final_pfs.append(pf)
                st = sf

        final_pfs = 12 * sum(final_pfs)
        return final_pfs

    return generate_value()

sim_values = []

for i in range(simulations):
    vs = create_sim(s0,r,sigma,n)
    sim_values.append(vs)

final_vs = sqrt(np.mean(sim_values))

print(f"Valuacion Variance Swap: {round(final_vs,6)}")

### HISTOGRAM PLOT FOR NORMAL DISTRIBUTION VISUALIZATION   
fig = plt.figure(figsize=(12,9))
ax = fig.subplots()
plt.hist(sim_values, bins=100)
plt.axis([0,0.2,0,800])
plt.ylabel('M simulaciones')
plt.xlabel('Variance Swap payoffs')
plt.title('Distribucion de cash flows de un Variance Swap')
plt.show()