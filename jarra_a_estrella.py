# jarras_a_estrella.py
# --------------------------------------------------------
# Problema de las jarras (3 L, 7 L, 9 L) resuelto con búsqueda A*
# Costos de acciones:
#   - Llenar = 1
#   - Vaciar = 3
#   - Transferir = 2
#
# Representación del estado: (litros_jarra1, litros_jarra2, litros_jarra3)
#   jarra1: capacidad 3 L
#   jarra2: capacidad 7 L
#   jarra3: capacidad 9 L
#
# Operadores (nombres completos):
#   LLENAR_JARRA1, LLENAR_JARRA2, LLENAR_JARRA3
#   VACIAR_JARRA1,  VACIAR_JARRA2,  VACIAR_JARRA3
#   TRANSFERIR_DE_JARRA1_A_JARRA2, TRANSFERIR_DE_JARRA1_A_JARRA3,
#   TRANSFERIR_DE_JARRA2_A_JARRA1, TRANSFERIR_DE_JARRA2_A_JARRA3,
#   TRANSFERIR_DE_JARRA3_A_JARRA1, TRANSFERIR_DE_JARRA3_A_JARRA2
# --------------------------------------------------------

from heapq import heappush, heappop

# Capacidades de las jarras
CAPACIDAD_JARRA1 = 3
CAPACIDAD_JARRA2 = 7
CAPACIDAD_JARRA3 = 9

COSTO_ACCION_LLENAR = 1
COSTO_ACCION_VACIAR = 3
COSTO_ACCION_TRANSFERIR = 2

# Orden determinista de acciones
ORDEN_ACCIONES = [
     "LLENAR_JARRA1", "LLENAR_JARRA2", "LLENAR_JARRA3",
    "VACIAR_JARRA1",  "VACIAR_JARRA2",  "VACIAR_JARRA3",
    "TRANSFERIR_DE_JARRA1_A_JARRA2",
    "TRANSFERIR_DE_JARRA1_A_JARRA3",
    "TRANSFERIR_DE_JARRA2_A_JARRA1",
    "TRANSFERIR_DE_JARRA2_A_JARRA3",
    "TRANSFERIR_DE_JARRA3_A_JARRA1",
    "TRANSFERIR_DE_JARRA3_A_JARRA2",
]


# 1) Definir estado inicial y final

def obtener_estado_inicial():
    """
    Devuelve el estado inicial: las tres jarras están vacías.
    """
    return (0, 0, 0)



def es_estado_final(estado):
    """
    Retorna True si la jarra de 7 L (jarra2) contiene exactamente 6 L.
    """
    litros_jarra1, litros_jarra2, litros_jarra3 = estado
    return litros_jarra2 == 6

# 2) Heurística para A*
# Heurística admisible: h(n) = |litros_jarra2 - 6|
def funcion_heuristica(estado):
    _, litros_jarra2, _ = estado
    return abs(litros_jarra2 - 6)