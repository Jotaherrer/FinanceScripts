import requests
from api_iol_recursiva import *
from opciones import *

mercado_acciones
info_bonos(mercado_bonos, 'AC17')
dolar_mep(mercado_bonos, 'AY24D', 'AY24')
ccl()
clean_assets(mercado_acciones)
clean_assets(mercado_cedears)
clean_assets(mercado_bonos)
store('ggal')
daily_ggal