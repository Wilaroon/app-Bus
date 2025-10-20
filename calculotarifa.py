# services/calculo_tarifa.py
import math
import random

TARIFA_BASE = 1.50
PRECIO_POR_KM = 1.00  # tarifa base por km

def calcular_tarifa(lat1, lon1, lat2, lon2):
    """
    Calcula distancia y tarifa básica sin mostrarla en la terminal
    """
    R = 6371  # radio de la Tierra en km
    dlat = math.radians(lat2 - lat1)
    dlon = math.radians(lon2 - lon1)
    a = math.sin(dlat/2)**2 + math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) * math.sin(dlon/2)**2
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    distancia_km = R * c

    # Simulación opcional de tráfico y velocidad
    factor_trafico = random.uniform(0.8, 1.5)
    tarifa = TARIFA_BASE + (distancia_km * PRECIO_POR_KM * factor_trafico)

    return round(distancia_km, 2), round(tarifa, 2)
