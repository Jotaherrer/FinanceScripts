"""
Problem Set 1 - Revisado
"""
from random import gauss, seed
from math import sqrt, exp

def create_GBM(s0, mu, sigma):
    """
    Crea un generador de valores de un Geometric Brownian Motion.
    s0 = Initial price of stock.
    mu = retorno anual promedio proyectado de la acción. Debería reflejar
    lo que pasará de ahora en más con el precio de la acción.
    sigma = annual standard deviation
    """
    st = s0
    # st será la variable que mantendrá la simulación definida por la
    # función a continuación.

    def generate_value():
        """
        Generador de valores de un Geometric Brownian Motion.
        """
        # Esta función estará tomando la variable "st" de la función create_GBM
        # por lo tanto debo clasificarla como "non local" para poder declarar-
        # la y que funcione en esta función.
        # Sirve para "traer la variable que está en un nivel superior"

        nonlocal st

        st *= exp((mu - 0.5 * sigma ** 2) * (1. / 365.) + sigma * sqrt(1./365.)
        * gauss(mu=0, sigma=1))

        # *= es equivalente a multiplicar lo que está a la izquierda del = por
        # el valor que está a la derecha y luego se pisa el valor anterior.
        # En definitiva sería: st = st * 2

        return st

    # Al hacerlo a través de una función, la función hará su cálculo y post.
    # recalculará el valor de st, pisando el anterior.

    return generate_value

    # DIFERENCIA ENTRE NONLOCAL Y GLOBAL:
    # GLOBAL se utiliza si la variable está almacenada en el máximo nivel
    # del código (NIVEL MÓDULO)
    # NONLOCAL se utiliza cuando la variable está almacenada dentro de una función

if __name__ == "__main__":
    # Al principio de la ejecución debe fijarse el "seed"
    seed(1234)
    gbm = create_GBM(100, 0.1, 0.05)

    # Creamos el loop para iterar 1000 veces la ecuación del precio.
    # En la creación del loop utilizamos el "_" en lugar de "i" para
    # omitir aclaraciones sobre el contenido de lo que se itera.
    for _ in range(1000):
        st = gbm()
        if st >= 130.:
            print("Target alcanzado. Toma de ganancia.")
            break
    else:
        print("Target no alcanzado.")

    print(st)

