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

# 5) Búsqueda A* con logs detallados
def busqueda_a_estrella(estado_inicial=None):
    """
    Realiza la búsqueda A*:
    - La prioridad en la cola es f(n) = g(n) + h(n)
    - Devuelve (estado_objetivo, diccionario_padre, diccionario_accion, logs_por_estado)
      donde logs_por_estado detalla cada expansión.
    """
    if estado_inicial is None:
        estado_inicial = obtener_estado_inicial()

    costo_estimado_desde_estado = funcion_heuristica(estado_inicial)  # h(inicial)
    frontera = []  # elementos: (f, id_incremental, estado)
    identificador_incremental = 0
    heappush(frontera, (costo_estimado_desde_estado, identificador_incremental, estado_inicial))

    # Estructuras de apoyo
    diccionario_padre = {estado_inicial: None}
    diccionario_accion = {estado_inicial: None}
    diccionario_costo_acumulado = {estado_inicial: 0}  # g(n)

    # Contadores y logs
    total_descubiertos = 1  # incluye el inicial
    total_expandidos = 0
    indice_expansion = 0
    logs_por_estado = {}

    conjunto_visitados = set()

    while frontera:
        valor_funcion_f, _identificador, estado_actual = heappop(frontera)

        # Si ya se visitó con mejor costo, se omite
        if estado_actual in conjunto_visitados:
            continue

        costo_acumulado_actual = diccionario_costo_acumulado[estado_actual]
        heuristica_actual = funcion_heuristica(estado_actual)

        # ¿Objetivo?
        if es_estado_final(estado_actual):
            frontera_total_ordenada = sorted(
                [
                    (
                        f,
                        diccionario_costo_acumulado.get(s, float("inf")),
                        f - diccionario_costo_acumulado.get(s, 0),
                        s,
                    )
                    for (f, _id, s) in frontera
                ],
                key=lambda t: (t[0], str(t[3]))
            )
            logs_por_estado[estado_actual] = {
                "indice_de_expansion": indice_expansion,
                "estado": estado_actual,
                "costo_acumulado_g": costo_acumulado_actual,
                "heuristica_h": heuristica_actual,
                "valor_funcion_f": costo_acumulado_actual + heuristica_actual,
                "accion_entrada": diccionario_accion.get(estado_actual),
                "sucesores": [],
                "sucesores_anadidos": [],
                "frontera_total": frontera_total_ordenada,
                "nuevos_descubiertos": 0,
                "expandidos_este_paso": 0,
                "totales": {"descubiertos": total_descubiertos, "expandidos": total_expandidos},
                "es_objetivo": True,
            }
            return estado_actual, diccionario_padre, diccionario_accion, logs_por_estado

        # Expandir
        conjunto_visitados.add(estado_actual)
        total_expandidos += 1

        acciones_posibles_en_orden = [a for a in ORDEN_ACCIONES if a in obtener_acciones_posibles(estado_actual)]

        # Para el log
        lista_sucesores = []
        lista_sucesores_anadidos = []
        descubiertos_este_paso = 0

        for nombre_accion in acciones_posibles_en_orden:
            estado_sucesor = aplicar_accion(estado_actual, nombre_accion)
            costo_de_accion = obtener_costo_de_accion(nombre_accion)
            costo_acumulado_sucesor = costo_acumulado_actual + costo_de_accion
            heuristica_sucesor = funcion_heuristica(estado_sucesor)
            valor_funcion_f_sucesor = costo_acumulado_sucesor + heuristica_sucesor

            # Registrar sucesor en el log (independiente de si entra o mejora)
            lista_sucesores.append((
                estado_sucesor,
                nombre_accion,
                costo_de_accion,
                costo_acumulado_sucesor,
                heuristica_sucesor,
                valor_funcion_f_sucesor
            ))

            # Si nunca visto o mejora costo g, actualizar y empujar a frontera
            if (estado_sucesor not in diccionario_costo_acumulado) or (costo_acumulado_sucesor < diccionario_costo_acumulado[estado_sucesor]):
                diccionario_costo_acumulado[estado_sucesor] = costo_acumulado_sucesor
                diccionario_padre[estado_sucesor] = estado_actual
                diccionario_accion[estado_sucesor] = nombre_accion
                identificador_incremental += 1
                heappush(frontera, (valor_funcion_f_sucesor, identificador_incremental, estado_sucesor))
                lista_sucesores_anadidos.append((valor_funcion_f_sucesor, estado_sucesor))
                descubiertos_este_paso += 1

        total_descubiertos += descubiertos_este_paso

        # Frontera para el log (ordenada por f, y estado como texto)
        frontera_total_ordenada = sorted(
            [
                (
                    f,
                    diccionario_costo_acumulado.get(s, float("inf")),
                    f - diccionario_costo_acumulado.get(s, 0),
                    s,
                )
                for (f, _id, s) in frontera
            ],
            key=lambda t: (t[0], str(t[3]))
        )

        logs_por_estado[estado_actual] = {
            "indice_de_expansion": indice_expansion,
            "estado": estado_actual,
            "costo_acumulado_g": costo_acumulado_actual,
            "heuristica_h": heuristica_actual,
            "valor_funcion_f": costo_acumulado_actual + heuristica_actual,
            "accion_entrada": diccionario_accion.get(estado_actual),
            "sucesores": lista_sucesores,  # (estado, accion, costo_accion, g, h, f)
            "sucesores_anadidos": lista_sucesores_anadidos,  # (f, estado)
            "frontera_total": frontera_total_ordenada,       # (f, g, h, estado)
            "nuevos_descubiertos": descubiertos_este_paso,
            "expandidos_este_paso": 1,
            "totales": {"descubiertos": total_descubiertos, "expandidos": total_expandidos},
            "es_objetivo": False,
        }

        indice_expansion += 1

    # Sin solución
    return None, diccionario_padre, diccionario_accion, logs_por_estado

# 6) Reconstrucción de la solución
def reconstruir_camino(estado_final, diccionario_padre, diccionario_accion):
    """
    Reconstruye la secuencia de (estado, acción_de_entrada) desde el inicial hasta el final.
    La primera tupla tiene accion_entrada = None.
    """
    if estado_final is None:
        return []

    camino = []
    estado = estado_final
    while estado is not None:
        accion_entrada = diccionario_accion.get(estado)
        camino.append((estado, accion_entrada))
        estado = diccionario_padre.get(estado)
    camino.reverse()
    return camino