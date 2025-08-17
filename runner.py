from heapq import heappush, heappop

# Capacidades de las jarras
CAPACIDAD_JARRA5 = 5
CAPACIDAD_JARRA4 = 4

# 1) Estado inicial y final

def obtener_estado_inicial():
    """
    Devuelve el estado inicial (las dos jarras están vacías)
    """
    return (0,0)

def es_estado_final(estado):
    """
    Retorna true si el estado corresponde al estado final.
    El final es que la jarra de 5 litros contenga exactamente 2 litros.
    """
    litros_jarra5, litros_jarra4 = estado
    return litros_jarra5 == 2


# 2) Heurística

def funcion_heuristica(estado):
    """
    Función heurística: muestra qué tan lejos la jarra 5 se encuentra de tener su capacidad ideal (2 litros)
    """
    litros_jarra5, litros_jarra4 = estado
    return abs(litros_jarra5 - 2)


