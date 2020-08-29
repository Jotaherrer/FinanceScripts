#%%
import api_min_hac as mh
import matplotlib.pyplot as plt

#%%
## ARGENTINE-PESO REAL EXCHANGE RATE
tcrm = mh.get_data(['116.3_TCRMA_0_M_36'], star_date='2002-01-01', limit=1000)
plt.plot(tcrm)
plt.title('REAL EXCHANGE RATE')
plt.show()

#%%
## NOMINAL EXCHANGE RATE TIME SERIES - NATIONAL BANK OFFICIAL RATE
tc_bna = mh.get_data(['168.1_T_CAMBIOR_D_0_0_26'], start_date='2008-01-01', limit= 1000)
tc_bna.plot()

#%%
## NOMINAL EXCHANGE RATE TIME SERIES - CENTRAL BANK OFFICIAL RATE (A3500)
tc3500 = mh.get_data(['175.1_DR_REFE500_0_0_25'], start_date='2010-01',
                   limit = 1000)
tc3500.plot()

#%%
## IPC BUENOS AIRES - 2016 EN ADELANTE
ipc_ba = mh.get_data(['103.1_I2N_2016_M_19'], limit = 1000)
ipc_ba.plot()

#%%
## EMAE - ESTIMADOR ACTIVIDAD ECONOMICA
emae_20 = mh.get_data(['143.3_NO_PR_2004_A_21'], limit = 1000, start_date='2020-01-01')
emae_20.plot()

emae_19 = mh.get_data(['143.3_NO_PR_2004_A_21'], limit = 1000, start_date='2019-01-01', end_date='2019-12-31')
emae_19.plot()

emae_18 = mh.get_data(['143.3_NO_PR_2004_A_21'], limit = 1000, start_date='2018-01-01', end_date='2018-12-31')
emae_18.plot()

emae_17 = mh.get_data(['143.3_NO_PR_2004_A_21'], limit = 1000, start_date='2017-01-01', end_date='2017-12-31')
emae_17.plot()

emae_15 = mh.get_data(['143.3_NO_PR_2004_A_21'], limit = 1000, start_date='2015-01-01', end_date='2015-12-31')
emae_15.plot()

emae = mh.get_data(['143.3_NO_PR_2004_A_21'], limit = 1000)
emae.plot()

#%%
# INTERNATIONAL RESERVES - Registro de reservas internacionales:
res = mh.get_data(['92.1_RID_0_0_32'], limit=1000)
res.plot()

#%% SOJA
soja = mh.get_data(['121.2_AS_0_0_11'], limit=1000)
plt.plot(soja.index, soja)
plt.title('Precio internacional Soja en USD')
plt.show()

# %%
# PETROLEO
oil = mh.get_data(['Precio_petroleo_RgR2vi'], limit = 1000)
oil.plot()

#%%
# POROTO DE SOJA
poroto = mh.get_data(['369.3_POROTO_SOJOJA__11'], limit = 1000)
poroto.plot()
poroto2 = mh.get_data(['369.3_POROTO_SOJOJA__11'], limit = 1000, start_date='2019-01-01', end_date = '2019-12-31')
poroto2.plot()



# %%
