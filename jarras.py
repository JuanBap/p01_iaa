# jarras.py
# --------------------------------------------------------
# Problema de las jarras (5 L y 4 L) resuelto con búsqueda
# Best-First (Greedy) usando la heurística h(R5, R4) = |R5 - 2|.
#
# Representación del estado: (litros_jarra5, litros_jarra4)
#   litros_jarra5 = litros actuales en la jarra de 5 L
#   litros_jarra4 = litros actuales en la jarra de 4 L
#
# Operadores:
#   L5  = Llenar jarra de 5 L
#   L4  = Llenar jarra de 4 L
#   V5  = Vaciar jarra de 5 L
#   V4  = Vaciar jarra de 4 L
#   T54 = Transferir de 5 L a 4 L
#   T45 = Transferir de 4 L a 5 L
# --------------------------------------------------------

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

# 3) Acciones y precondiciones

def obtener_acciones_posibles(estado):
    """
    Retorna el conjunto de acciones posibles para aplicar en el 'estado'
    Se verifican las precondiciones básicas para cada posible acción
    """
    litros_jarra5, litros_jarra4 = estado
    conjunto_acciones = set()

    if litros_jarra5 < CAPACIDAD_JARRA5:
        conjunto_acciones.add("L5")
    if litros_jarra4 < CAPACIDAD_JARRA4:
        conjunto_acciones.add("L4")
    if litros_jarra5 > 0:
        conjunto_acciones.add("V5")
    if litros_jarra4 > 0:
        conjunto_acciones.add("V4")
    if litros_jarra5 > 0 and litros_jarra4 < CAPACIDAD_JARRA4:
        conjunto_acciones.add("T54")
    if litros_jarra4 > 0 and litros_jarra5 < CAPACIDAD_JARRA5:
        conjunto_acciones.add("T45")

    return conjunto_acciones

# 4) Modelo de transición

def aplicar_accion(estado, accion):
    """
    Aplica la acción al estado y retorna el nuevo estado (litros_jarra5, litros_jarra4)
    Hace uso de min/max para manejar los sobrantes de las jarras
    """

    litros_jarra5, litros_jarra4 = estado

    if accion == "L5":       # Llenar jarra de 5 litros
        return (CAPACIDAD_JARRA5, litros_jarra4)

    elif accion == "L4":     # Llenar jarra de 4 litros
        return (litros_jarra5, CAPACIDAD_JARRA4)

    elif accion == "V5":     # Vaciar jarra de 5 litros
        return (0, litros_jarra4)

    elif accion == "V4":     # Vaciar jarra de 4 litros
        return (litros_jarra5, 0)

    elif accion == "T54":    # Transferir de jarra 5 L a jarra 4 L
        espacio_disponible_en_jarra4 = CAPACIDAD_JARRA4 - litros_jarra4
        cantidad_transferida = min(litros_jarra5, espacio_disponible_en_jarra4)
        return (litros_jarra5 - cantidad_transferida, litros_jarra4 + cantidad_transferida)

    elif accion == "T45":    # Transferir de jarra 4 L a jarra 5 L
        espacio_disponible_en_jarra5 = CAPACIDAD_JARRA5 - litros_jarra5
        cantidad_transferida = min(litros_jarra4, espacio_disponible_en_jarra5)
        return (litros_jarra5 + cantidad_transferida, litros_jarra4 - cantidad_transferida)
    

# 5) Búsqueda best-first
def busqueda_best_first(estado_inicial = None):
    """
    Realiza la búsqueda Best-first:
    - La prioridad en la cola es sólo la heurística h(n)
    - Devuelve el (estado_objetivo, diccionario_padre, diccionario_accion) para reconstruir el camino.
    """
    if estado_inicial is None:
        estado_inicial = obtener_estado_inicial()
    
    # Cola de prioridad: (h, id_incremental, estado)
    frontera = []
    id_incremental = 0
    heappush(frontera, (funcion_heuristica(estado_inicial), id_incremental, estado_inicial))

    # Conjuntos y diccionarios de apoyo
    visitados = set()
    diccionario_padre = {estado_inicial: None}
    diccionario_accion = {estado_inicial: None}

    while frontera:
        valor_heuristico, identificador, estado_actual = heappop(frontera)

        if estado_actual in visitados:
            continue
        visitados.add(estado_actual)

        if es_estado_final(estado_actual):
            return estado_actual, diccionario_padre, diccionario_accion
        
        for accion in obtener_acciones_posibles(estado_actual):
            sucesor = aplicar_accion(estado_actual, accion)
            if sucesor not in diccionario_padre: # Si aún no ha sido descubieto
                diccionario_padre[sucesor] = estado_actual
                diccionario_accion[sucesor] = accion
                id_incremental += 1
                heappush(frontera, (funcion_heuristica(sucesor), id_incremental, sucesor))
        
    # En caso de que no se encuentre la solución
    return None, diccionario_padre, diccionario_accion

# 6) Reconstrucción de la solución
def reconstruir_camino(estado_final, diccionario_padre, diccionario_accion):
    """
    Reconstruye la secuencia de (estado, acción) desde el inicial
    hasta el final. La primera tupla tiene accion_entrada = None.
    """
    if estado_final is None:
        return[]
    
    camino = []
    estado = estado_final

    while estado is not None:
        accion_entrada = diccionario_accion[estado]
        camino.append((estado, accion_entrada))
        estado = diccionario_padre[estado]
    camino.reverse()
    return camino

# 7) Imprimir texto
def descripcion_de_accion(codigo_accion):
    """
    Traduce el código corto de acción a una descripción legible.
    """
    return {
        "L5": "Llenar jarra de 5 L",
        "L4": "Llenar jarra de 4 L",
        "V5": "Vaciar jarra de 5 L",
        "V4": "Vaciar jarra de 4 L",
        "T54": "Transferir de 5 L a 4 L",
        "T45": "Transferir de 4 L a 5 L",
        None:  "Estado inicial"
    }[codigo_accion]

# 8) Ejecución simple
if __name__ == "__main__":
    estado_objetivo, diccionario_padre, diccionario_accion = busqueda_best_first()
    camino_solucion = reconstruir_camino(estado_objetivo, diccionario_padre, diccionario_accion)

    print("Solución Solución Best-First con heurística |J5-2|:\n")
    for indice, (estado, accion) in enumerate(camino_solucion):
        print(f"Paso {indice:02d}: Estado {str(estado):>7}  <- {descripcion_de_accion(accion)}")
    print("\nEstado final alcanzado:", camino_solucion[-1][0] if camino_solucion else None)