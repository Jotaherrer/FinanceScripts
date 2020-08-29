import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
from statsmodels.sandbox.regression.gmm import IV2SLS
from sklearn.linear_model import LogisticRegression


df = pd.read_excel('Clase 3/cig.xlsx')

"""
The data set consists of annual data for the 48 continental U.S. states.  Quantity consumed is measured by annual 
per capita cigarette sales in packs per fiscal year, as derived from state tax collection data.  The price is the average retail 
cigarette price per pack during the fiscal year, including taxes. The cigarette-specific tax is the tax applied to cigarettes only.  
All prices, income, and taxes are deflated by the Consumer Price Index and thus are in constant (real) dollars.  

Columns description:
- state: 48 continental U.S. states 
- year: 1985 and 1995
- cpi: Consumer Price Index (U.S.)   
- pop: State population
- packpc: Number of packs consumed per capita ==> IMPORTANT TO SHOW RELATIVE CONSUMPTION TO POPULATION SIZE (MORE POPULATED STATES 
SHOULD HAVE GREATER SALES, BUT WHEN ADJUSTED FOR POPULATION WE ADJUST THIS DIFFERENCE)
- income: State personal income (nominal)
- tax: Average stat, federal and average local taxes for FY.
- avgprs: Average price during FY, including sales tax.
- taxs: Average taxes fro FY, including sales tax.

How can we determine the optimal level of tax prices for cigarettes?
"""
### RE-EXPRESS VALUES FOR INFLATION INDICES
df['real_price'] = df['avgprs'] / df['cpi']     # ==> Relative price for cigarettes and consumer index products (real purchase power).
df['cigtax'] = df['tax'] / df['cpi']

### CREATE IMPORTANT NEW VARIABLES
df['sales_tax'] = (df['taxs'] - df['tax']) / df['cpi'] # ==> Discrimination of Sales Tax 
df['income_per_capita'] = df['income'] / df['pop'] * df['cpi']    # ==> Income per capita  

### COMPUTE CORRELATIONS
corr_tax = df['real_price'].corr(df['cigtax'])              # ==> 0.84 - HIGH correlation between price and taxes.
corr_sales_tax = df['real_price'].corr(df['sales_tax'])     # ==> 0.70 - Also HIGH correlation but with prices and sales tax.

### STORE DATA FOR 1995 ONLY TO AVOID WORKING WITH PANEL DATA 
df_1995 = df[df['year'] == 1995]

### CALCULATE LINEAR REGRESSION - 1 STAGE OLS
lm = smf.ols('np.log(packpc) ~ np.log(real_price)',data=df_1995)    # ==> Coefficientes are interpreted as demand elasticity for cigarettes.
                                                                    # ==> An increase in 1% of prices should cause a 1,21% decrease in demand.
fit_lm = lm.fit()
print(fit_lm.summary())

### CALCULATE LINEAR REGRESSION WITH INSTRUMENTAL VARIABLES AS ENDOGENOUS VARIABLES ARE INVOLVED IN THE CASE - 2 STAGE OLS
lm2_1 = smf.ols('np.log(real_price) ~ sales_tax', data=df_1995)
fit_lm2_1 = lm2_1.fit()
print(fit_lm2_1.summary())      # ==> As expected by the results of calculated correlations, R2 is relatively high.
                                # ==> In univariate regression models, R2 tends to be similar with correlation. 
### 2 STAGE
orig = np.log(df_1995['real_price']).values
fitted = fit_lm2_1.fittedvalues.values      
lm2_2 = smf.ols('np.log(packpc) ~ fitted', data=df_1995)
fit_lm2_2 = lm2_2.fit()
print(fit_lm2_2.summary())      # ==> Obtain corrected regression with revised elasticy for cigarettes. However, Standard Deviations are manually calculated.

fit_lm2_2_iv = IV2SLS(np.log(df_1995['packpc']),fitted, instrument=df_1995['sales_tax']).fit()
print(fit_lm2_2_iv.summary())