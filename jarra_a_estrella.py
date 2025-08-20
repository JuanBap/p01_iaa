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

# 3) Acciones y precondiciones

def obtener_acciones_posibles(estado):
    """
    Retorna el conjunto de acciones posibles (nombres completos) aplicables en 'estado'.
    """
    litros_jarra1, litros_jarra2, litros_jarra3 = estado
    conjunto_acciones = set()

    # Llenar (si no está llena)
    if litros_jarra1 < CAPACIDAD_JARRA1:
        conjunto_acciones.add("LLENAR_JARRA1")
    if litros_jarra2 < CAPACIDAD_JARRA2:
        conjunto_acciones.add("LLENAR_JARRA2")
    if litros_jarra3 < CAPACIDAD_JARRA3:
        conjunto_acciones.add("LLENAR_JARRA3")

    # Vaciar (si tiene algo)
    if litros_jarra1 > 0:
        conjunto_acciones.add("VACIAR_JARRA1")
    if litros_jarra2 > 0:
        conjunto_acciones.add("VACIAR_JARRA2")
    if litros_jarra3 > 0:
        conjunto_acciones.add("VACIAR_JARRA3")

    # Transferir (si origen tiene > 0 y destino no está lleno)
    if litros_jarra1 > 0 and litros_jarra2 < CAPACIDAD_JARRA2:
        conjunto_acciones.add("TRANSFERIR_DE_JARRA1_A_JARRA2")
    if litros_jarra1 > 0 and litros_jarra3 < CAPACIDAD_JARRA3:
        conjunto_acciones.add("TRANSFERIR_DE_JARRA1_A_JARRA3")

    if litros_jarra2 > 0 and litros_jarra1 < CAPACIDAD_JARRA1:
        conjunto_acciones.add("TRANSFERIR_DE_JARRA2_A_JARRA1")
    if litros_jarra2 > 0 and litros_jarra3 < CAPACIDAD_JARRA3:
        conjunto_acciones.add("TRANSFERIR_DE_JARRA2_A_JARRA3")

    if litros_jarra3 > 0 and litros_jarra1 < CAPACIDAD_JARRA1:
        conjunto_acciones.add("TRANSFERIR_DE_JARRA3_A_JARRA1")
    if litros_jarra3 > 0 and litros_jarra2 < CAPACIDAD_JARRA2:
        conjunto_acciones.add("TRANSFERIR_DE_JARRA3_A_JARRA2")

    return conjunto_acciones

# 4) Modelo de transición y costo de acción

def obtener_costo_de_accion(nombre_accion):
    """
    Devuelve el costo asociado a la acción por su tipo (llenar, vaciar, transferir).
    """
    if nombre_accion.startswith("LLENAR_"):
        return COSTO_ACCION_LLENAR
    if nombre_accion.startswith("VACIAR_"):
        return COSTO_ACCION_VACIAR
    if nombre_accion.startswith("TRANSFERIR_"):
        return COSTO_ACCION_TRANSFERIR
    raise ValueError(f"Acción desconocida: {nombre_accion}")

# Super tedioso jajaa

def aplicar_accion(estado, nombre_accion):
    """
    Aplica la acción (nombre completo) y retorna el nuevo estado (litros_jarra1, litros_jarra2, litros_jarra3).
    """
    litros_jarra1, litros_jarra2, litros_jarra3 = estado

    # Llenar
    if nombre_accion == "LLENAR_JARRA1":
        return (CAPACIDAD_JARRA1, litros_jarra2, litros_jarra3)
    if nombre_accion == "LLENAR_JARRA2":
        return (litros_jarra1, CAPACIDAD_JARRA2, litros_jarra3)
    if nombre_accion == "LLENAR_JARRA3":
        return (litros_jarra1, litros_jarra2, CAPACIDAD_JARRA3)

    # Vaciar
    if nombre_accion == "VACIAR_JARRA1":
        return (0, litros_jarra2, litros_jarra3)
    if nombre_accion == "VACIAR_JARRA2":
        return (litros_jarra1, 0, litros_jarra3)
    if nombre_accion == "VACIAR_JARRA3":
        return (litros_jarra1, litros_jarra2, 0)

    # Transferencias (cálculo genérico auxiliar)
    def transferir(cantidad_origen, capacidad_destino, cantidad_destino):
        espacio_en_destino = capacidad_destino - cantidad_destino
        cantidad_transferida = min(cantidad_origen, espacio_en_destino)
        return cantidad_transferida

    # 1 -> 2
    if nombre_accion == "TRANSFERIR_DE_JARRA1_A_JARRA2":
        t = transferir(litros_jarra1, CAPACIDAD_JARRA2, litros_jarra2)
        return (litros_jarra1 - t, litros_jarra2 + t, litros_jarra3)
    # 1 -> 3
    if nombre_accion == "TRANSFERIR_DE_JARRA1_A_JARRA3":
        t = transferir(litros_jarra1, CAPACIDAD_JARRA3, litros_jarra3)
        return (litros_jarra1 - t, litros_jarra2, litros_jarra3 + t)
    # 2 -> 1
    if nombre_accion == "TRANSFERIR_DE_JARRA2_A_JARRA1":
        t = transferir(litros_jarra2, CAPACIDAD_JARRA1, litros_jarra1)
        return (litros_jarra1 + t, litros_jarra2 - t, litros_jarra3)
    # 2 -> 3
    if nombre_accion == "TRANSFERIR_DE_JARRA2_A_JARRA3":
        t = transferir(litros_jarra2, CAPACIDAD_JARRA3, litros_jarra3)
        return (litros_jarra1, litros_jarra2 - t, litros_jarra3 + t)
    # 3 -> 1
    if nombre_accion == "TRANSFERIR_DE_JARRA3_A_JARRA1":
        t = transferir(litros_jarra3, CAPACIDAD_JARRA1, litros_jarra1)
        return (litros_jarra1 + t, litros_jarra2, litros_jarra3 - t)
    # 3 -> 2
    if nombre_accion == "TRANSFERIR_DE_JARRA3_A_JARRA2":
        t = transferir(litros_jarra3, CAPACIDAD_JARRA2, litros_jarra2)
        return (litros_jarra1, litros_jarra2 + t, litros_jarra3 - t)

    raise ValueError(f"Acción desconocida: {nombre_accion}")

