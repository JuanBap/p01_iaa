# runner2.py
# ------------------------------------------------------
# Runner de consola para el problema de las jarras (A*).
# - Importa el módulo 'jarras_a_estrella' y ejecuta la búsqueda A*
#   mostrando el historial completo de expansiones en orden real
#   de extracción de la frontera (no solo el camino solución).
# - Incluye un modo "paso a paso" interactivo opcional.
# ------------------------------------------------------
import argparse
import time
import jarras_a_estrella as problema_jarras

# Ayudado con gpt porque son demasiados prints

def _tabla_ascii_frontera_estrella(frontera_total):
    """
    Recibe una lista de tuplas (f, g, h, estado) y devuelve una cadena con
    una tabla ASCII vertical con columnas: Idx, Estado, g, h, f.
    """
    if not frontera_total:
        return ""

    # Preparar filas como strings
    filas = []
    for idx, (f, g, h, s) in enumerate(frontera_total):
        filas.append([str(idx), str(s), str(g), str(h), f"{f:.0f}"])

    headers = ["Idx", "Estado", "g", "h", "f"]
    num_cols = len(headers)
    anchos = [len(headers[i]) for i in range(num_cols)]
    for fila in filas:
        for i, celda in enumerate(fila):
            if len(celda) > anchos[i]:
                anchos[i] = len(celda)

    def linea_sep():
        return "+" + "+".join("-" * (anchos[i] + 2) for i in range(num_cols)) + "+"

    def formatear_fila(valores):
        return "| " + " | ".join(f"{valores[i]:<{anchos[i]}}" for i in range(num_cols)) + " |"

    lineas = [linea_sep(), formatear_fila(headers), linea_sep()]
    for fila in filas:
        lineas.append(formatear_fila(fila))
    lineas.append(linea_sep())

    return "\n".join(lineas)


def _tabla_ascii_vertical(headers, filas):
    """
    Construye una tabla ASCII vertical genérica a partir de headers y filas (listas de strings).
    """
    if not filas:
        return ""
    headers_str = [str(h) for h in headers]
    filas_str = [[str(c) for c in fila] for fila in filas]
    num_cols = len(headers_str)
    anchos = [len(headers_str[i]) for i in range(num_cols)]
    for fila in filas_str:
        for i, celda in enumerate(fila):
            if len(celda) > anchos[i]:
                anchos[i] = len(celda)

    def linea_sep():
        return "+" + "+".join("-" * (anchos[i] + 2) for i in range(num_cols)) + "+"

    def formatear_fila(valores):
        return "| " + " | ".join(f"{valores[i]:<{anchos[i]}}" for i in range(num_cols)) + " |"

    lineas = [linea_sep(), formatear_fila(headers_str), linea_sep()]
    for fila in filas_str:
        lineas.append(formatear_fila(fila))
    lineas.append(linea_sep())
    return "\n".join(lineas)


def imprimir_logs_formateados_estrella(camino_solucion, logs_por_estado, pausa_segundos=0.0, modo_interactivo=False):
    """
    Imprime los logs de expansión A* de acuerdo al formato de runner.py,
    mostrando TODAS las expansiones en orden real (no solo el camino).
    """
    if not logs_por_estado:
        return

    print("Solución A* con heurística |jarra2-6| y costos L=1, V=3, T=2:\n")

    # Mostrar TODAS las expansiones en orden real (orden de extracción de la frontera)
    logs_expandidos = [v for v in logs_por_estado.values() if not v.get("es_objetivo") and ("indice_de_expansion" in v)]
    logs_expandidos.sort(key=lambda x: x["indice_de_expansion"])

    for idx, log in enumerate(logs_expandidos):
        estado = log["estado"]
        accion_entrada = log.get("accion_entrada")
        descripcion = problema_jarras.descripcion_de_accion(accion_entrada)

        print(f"- Paso {idx:02d} | Estado {estado} <- {descripcion}")
        print(
            f"  Expansión #{log['indice_de_expansion']:02d} (orden real) | g={log['costo_acumulado_g']}  h={log['heuristica_h']}  f={log['valor_funcion_f']}"
        )
        # Sucesores como tabla vertical
        filas_sucesores = []
        for i, (suc, acc, cacc, g_suc, h_suc, f_suc) in enumerate(log["sucesores"]):
            filas_sucesores.append([
                str(i),
                str(suc),
                problema_jarras.descripcion_de_accion(acc),
                str(cacc),
                str(g_suc),
                str(h_suc),
                f"{f_suc:.0f}",
            ])
        if not filas_sucesores:
            filas_sucesores = [["-", "(sin sucesores)", "-", "-", "-", "-", "-"]]
        print("  Sucesores (tabla):")
        print(
            _tabla_ascii_vertical(
                ["Idx", "Estado", "Acción", "c", "g", "h", "f"], filas_sucesores
            )
        )
        print("")

        # Sucesores añadidos como tabla vertical
        filas_anadidos = []
        for i, (f, g, h, s) in enumerate(log["sucesores_anadidos"]):
            filas_anadidos.append([str(i), str(s), str(g), str(h), f"{f:.0f}"])
        if not filas_anadidos:
            filas_anadidos = [["-", "(ninguno)", "-", "-", "-"]]
        print("  Sucesores añadidos (tabla):")
        print(_tabla_ascii_vertical(["Idx", "Estado", "g", "h", "f"], filas_anadidos))
        print("")

        # Frontera total como tabla vertical
        filas_frontera = []
        for i, (f, g, h, s) in enumerate(log["frontera_total"]):
            filas_frontera.append([str(i), str(s), str(g), str(h), f"{f:.0f}"])
        if not filas_frontera:
            filas_frontera = [["-", "(vacía)", "-", "-", "-"]]
        print("  Frontera total (tabla):")
        print(_tabla_ascii_vertical(["Idx", "Estado", "g", "h", "f"], filas_frontera))
        print("")

        # También mostrar la cola como tabla ASCII (estados/posición)
        if log["frontera_total"]:
            print("  Cola (formato tabla):")
            print(_tabla_ascii_frontera_estrella(log["frontera_total"]))

        print(
            f"  Nuevos   | Descubiertos únicos: {log['nuevos_descubiertos']}  |  Expandidos: {log['expandidos_este_paso']}"
        )
        print(
            f"  Totales  | Descubiertos: {log['totales']['descubiertos']}  |  Expandidos: {log['totales']['expandidos']}"
        )
        if idx == 0:
            print("  Nota: 'Descubiertos' totales incluyen el estado inicial.")
            print(
                "  Nota: El contador de descubiertos incluye solo sucesores realmente nuevos (únicos) agregados a la frontera; los ya vistos no incrementan el total."
            )
        print("")

        # Interacción / pausa entre pasos
        if modo_interactivo and idx < len(logs_expandidos) - 1:
            input("Presiona ENTER para continuar...")
        elif pausa_segundos > 0:
            time.sleep(pausa_segundos)

    # Imprimir el objetivo si está en logs y no fue expandido
    objetivos = [v for v in logs_por_estado.values() if v.get("es_objetivo")]
    if objetivos:
        obj = objetivos[0]
        estado = obj["estado"]
        print(
            f"- Paso {len(logs_expandidos):02d} | Estado {estado} <- {problema_jarras.descripcion_de_accion(obj.get('accion_entrada'))}"
        )
        print("  [Objetivo detectado: no se expandió]")
        print(
            f"  Nuevos   | Descubiertos únicos: {obj['nuevos_descubiertos']}  |  Expandidos: {obj['expandidos_este_paso']}"
        )
        print("")
        print(f"Estado final alcanzado: {estado}")


def ejecutar_busqueda_y_mostrar(pausa_segundos=0.0, modo_interactivo=False):
    """
    Ejecuta la búsqueda A* del módulo 'jarras_a_estrella' y muestra el resultado.
    Además imprime estadísticas simples del recorrido.
    """
    # 1) Ejecutar búsqueda
    estado_objetivo, diccionario_padre, diccionario_accion, logs_por_estado = problema_jarras.busqueda_a_estrella(
        problema_jarras.obtener_estado_inicial()
    )

    # 2) Reconstruir el camino solución
    camino_solucion = problema_jarras.reconstruir_camino(
        estado_objetivo, diccionario_padre, diccionario_accion
    )

    # 3) Mostrar logs detallados de TODAS las expansiones
    imprimir_logs_formateados_estrella(
        camino_solucion,
        logs_por_estado,
        pausa_segundos=pausa_segundos,
        modo_interactivo=modo_interactivo,
    )

    # Línea adicional similar al runner original
    print(f"Camino solución reconstruido con {len(camino_solucion)} pasos")
    if camino_solucion:
        print(f"Estado final alcanzado: {camino_solucion[-1][0]}\n")

    # 4) Métricas simples
    total_pasos = max(len(camino_solucion) - 1, 0)  # acciones ejecutadas
    total_estados_explorados = len(diccionario_padre)
    print(f"\nResumen:")
    print(f"- Acciones ejecutadas: {total_pasos}")
    print(f"- Estados descubiertos (nodos generados): {total_estados_explorados}")


def construir_argumentos():
    """
    Construye y devuelve el parser de argumentos de línea de comandos.
    """
    parser = argparse.ArgumentParser(
        description="Runner de consola para el problema de las jarras (A*)."
    )
    parser.add_argument(
        "--pausa",
        type=float,
        default=0.0,
        help="Pausa (en segundos) entre pasos. Ejemplo: --pausa 0.4",
    )
    parser.add_argument(
        "--interactivo",
        action="store_true",
        help="Muestra los pasos en modo interactivo (ENTER para avanzar).",
    )
    return parser


def main():
    parser = construir_argumentos()
    argumentos = parser.parse_args()

    # Validación simple de pausa
    if argumentos.pausa < 0:
        print("El valor de --pausa no puede ser negativo. Se usará 0.0.")
        argumentos.pausa = 0.0

    ejecutar_busqueda_y_mostrar(
        pausa_segundos=argumentos.pausa, modo_interactivo=argumentos.interactivo
    )


if __name__ == "__main__":
    main()


