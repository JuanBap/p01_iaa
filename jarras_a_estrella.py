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

# Orden determinista de acciones para consistencia en la búsqueda
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
    _, litros_jarra2, _ = estado
    return litros_jarra2 == 6

# 2) Heurística para A*: h(n) = |litros_jarra2 - 6|
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

# 5) Búsqueda A* con logs detallados - Ayudado de ChatGPT 5 Thinking, prompt documentado en prompt2.txt
def busqueda_a_estrella(estado_inicial=None):
    """
    Realiza la búsqueda A*:
    - La prioridad en la cola es f(n) = g(n) + h(n)
    - Devuelve (estado_objetivo, diccionario_padre, diccionario_accion, logs_por_estado)
      donde logs_por_estado detalla cada expansión.
    """
    if estado_inicial is None:
        estado_inicial = obtener_estado_inicial()

    frontera = []  # elementos: (f, id_incremental, estado)
    id_incremental = 0
    heappush(frontera, (funcion_heuristica(estado_inicial), id_incremental, estado_inicial))

    # Estructuras de apoyo
    diccionario_padre = {estado_inicial: None}
    diccionario_accion = {estado_inicial: None}
    diccionario_costo_acumulado = {estado_inicial: 0}  # g(n)

    # Contadores y logs
    total_descubiertos = 1  # incluye el inicial
    total_expandidos = 0
    indice_expansion = 0
    logs_por_estado = {}

    visitados = set()

    while frontera:
        valor_funcion_f, _identificador, estado_actual = heappop(frontera)

        if estado_actual in visitados:
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
        visitados.add(estado_actual)
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

            # Registrar sucesor (siempre)
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
                id_incremental += 1
                heappush(frontera, (valor_funcion_f_sucesor, id_incremental, estado_sucesor))
                lista_sucesores_anadidos.append((valor_funcion_f_sucesor, costo_acumulado_sucesor, heuristica_sucesor, estado_sucesor))
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
            "sucesores": lista_sucesores,             # (estado, accion, costo_accion, g, h, f)
            "sucesores_anadidos": lista_sucesores_anadidos,  # (f, g, h, estado)
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

# 7) Descripciones legibles de acciones
def descripcion_de_accion(nombre_accion):
    descripciones = {
        "LLENAR_JARRA1": "Llenar jarra 1 (3 L)",
        "LLENAR_JARRA2": "Llenar jarra 2 (7 L)",
        "LLENAR_JARRA3": "Llenar jarra 3 (9 L)",
        "VACIAR_JARRA1": "Vaciar jarra 1 (3 L)",
        "VACIAR_JARRA2": "Vaciar jarra 2 (7 L)",
        "VACIAR_JARRA3": "Vaciar jarra 3 (9 L)",
        "TRANSFERIR_DE_JARRA1_A_JARRA2": "Transferir de jarra 1 (3 L) a jarra 2 (7 L)",
        "TRANSFERIR_DE_JARRA1_A_JARRA3": "Transferir de jarra 1 (3 L) a jarra 3 (9 L)",
        "TRANSFERIR_DE_JARRA2_A_JARRA1": "Transferir de jarra 2 (7 L) a jarra 1 (3 L)",
        "TRANSFERIR_DE_JARRA2_A_JARRA3": "Transferir de jarra 2 (7 L) a jarra 3 (9 L)",
        "TRANSFERIR_DE_JARRA3_A_JARRA1": "Transferir de jarra 3 (9 L) a jarra 1 (3 L)",
        "TRANSFERIR_DE_JARRA3_A_JARRA2": "Transferir de jarra 3 (9 L) a jarra 2 (7 L)",
        None: "Estado inicial"
    }
    return descripciones.get(nombre_accion, nombre_accion)

# 8) Utilidades de impresión "visual"

def _formatear_tabla_cola(frontera_total):
    """
    Devuelve dos líneas tipo tabla:
    - Encabezado con los estados en orden de f
    - Fila con los índices de columna (0..n-1)
    """
    if not frontera_total:
        return ["(cola vacía)", ""]
    estados = [str(t[3]) for t in frontera_total]  # t = (f,g,h,estado)
    # calcular anchos por columna
    anchos = [max(len(e), 1) for e in estados]
    linea_titulos = "| " + " | ".join(f"{e:<{anchos[i]}}" for i, e in enumerate(estados)) + " |"
    linea_indices = "| " + " | ".join(f"{i:<{anchos[i]}}" for i, _ in enumerate(estados)) + " |"
    separador = "-" * len(linea_titulos)
    return [linea_titulos, separador, linea_indices]

def imprimir_traza_detallada(camino_solucion, logs_por_estado):
    """
    Imprime la traza detallada paso a paso al estilo solicitado.
    """
    print("Solución con A* (h(n)=|jarra2-6|; costos: Llenar=1, Vaciar=3, Transferir=2):\n")

    # Línea por cada estado del camino
    for indice, (estado, accion) in enumerate(camino_solucion):
        descripcion = descripcion_de_accion(accion)
        prefijo_paso = f"- Paso {indice:02d} | Estado {estado} <- {descripcion}"
        print(prefijo_paso)

        log = logs_por_estado.get(estado)
        if not log:
            print("  [Sin log disponible para este estado]\n")
            continue

        if log["es_objetivo"]:
            print("  [Objetivo detectado: no se expandió]")
            print(f"  Nuevos   | Descubiertos únicos: {log['nuevos_descubiertos']}  |  Expandidos: {log['expandidos_este_paso']}\n")
            continue

        print(f"  Expansión #{log['indice_de_expansion']:02d} (orden real) | g={log['costo_acumulado_g']}  h={log['heuristica_h']}  f={log['valor_funcion_f']}")
        print("  Sucesores descubiertos (estado, acción, c, g, h, f):")
        for (suc, acc, cacc, g_suc, h_suc, f_suc) in log["sucesores"]:
            print(f"    - {suc}  <- {descripcion_de_accion(acc)}  [c={cacc}, g={g_suc}, h={h_suc}, f={f_suc}]")

        # Sucesores realmente añadidos (nuevos o mejor g)
        if log["sucesores_anadidos"]:
            etiqueta = "  Sucesores añadidos: ["
            contenido = ", ".join([f"f={f:.0f}|g={g}|h={h}:{s}" for (f, g, h, s) in log["sucesores_anadidos"]])
            print(etiqueta + contenido + "]")
        else:
            print("  Sucesores añadidos: []")

        # Frontera total ordenada
        if log["frontera_total"]:
            lista = ", ".join([f"f={f:.0f}|g={g}|h={h}:{s}" for (f, g, h, s) in log["frontera_total"]])
            print(f"  Frontera total: [{lista}]")
        else:
            print("  Frontera total: []")

        # Tabla de la cola
        print("  Cola (formato tabla):")
        l1, l2, l3 = _formatear_tabla_cola(log["frontera_total"])
        print(l1)
        if l2:
            print(l2)
        if l3:
            print(l3)

        # Contadores
        print(f"  Nuevos   | Descubiertos únicos: {log['nuevos_descubiertos']}  |  Expandidos: {log['expandidos_este_paso']}")
        print(f"  Totales  | Descubiertos: {log['totales']['descubiertos']}  |  Expandidos: {log['totales']['expandidos']}")

        # Notas en el primer paso como en tu ejemplo
        if indice == 0:
            print("  Nota: 'Descubiertos' totales incluyen el estado inicial.")
            print("  Nota: El contador de descubiertos incluye solo sucesores realmente nuevos (únicos) agregados a la frontera; los ya vistos no incrementan el total.")
        print()

# 9) Main
if __name__ == "__main__":
    estado_objetivo, diccionario_padre, diccionario_accion, logs_por_estado = busqueda_a_estrella()
    camino_solucion = reconstruir_camino(estado_objetivo, diccionario_padre, diccionario_accion)

    imprimir_traza_detallada(camino_solucion, logs_por_estado)

    # Resumen final
    acciones_ejecutadas = max(0, len(camino_solucion) - 1)
    estados_descubiertos_totales = 0
    # tomar "descubiertos" del último log disponible
    if camino_solucion:
        ultimo_estado = camino_solucion[-1][0]
        ultimo_log = logs_por_estado.get(ultimo_estado)
        if ultimo_log:
            estados_descubiertos_totales = ultimo_log["totales"]["descubiertos"]

    print(f"Estado final alcanzado: {camino_solucion[-1][0] if camino_solucion else None}")
    print(f"Camino solución reconstruido con {len(camino_solucion)} pasos")
    print(f"\nResumen:\n- Acciones ejecutadas: {acciones_ejecutadas}\n- Estados descubiertos (nodos generados): {estados_descubiertos_totales}")
