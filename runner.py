# runner.py
# ------------------------------------------------------
# Runner de consola para el problema de las jarras.
# - Importa el módulo 'jarras' y ejecuta la búsqueda
#   Best-First mostrando los pasos de la solución.
# - Incluye un modo "paso a paso" interactivo opcional.
# ------------------------------------------------------
import argparse
import time
import jarras as problema_jarras


def mostrar_camino_solucion(camino_solucion, pausa_segundos=0.0, modo_interactivo=False):
    """
    Imprime la secuencia de estados y acciones de la solución.
    Si 'modo_interactivo' es True, espera ENTER en cada paso.
    Si 'pausa_segundos' > 0, duerme esa cantidad entre pasos.
    """
    if not camino_solucion:
        print("No se encontró una solución.")
        return

    # Encabezado ya lo imprime imprimir_logs_formateados
    for indice, (estado, codigo_accion) in enumerate(camino_solucion):
        descripcion = problema_jarras.descripcion_de_accion(codigo_accion)
        print(f"Paso {indice:02d}: Estado {str(estado):>7}  <- {descripcion}")
        if modo_interactivo and indice < len(camino_solucion) - 1:
            input("Presiona ENTER para continuar...")
        elif pausa_segundos > 0:
            time.sleep(pausa_segundos)

    estado_final = camino_solucion[-1][0]
    print("\nEstado final alcanzado:", estado_final)


def _tabla_ascii_frontera(frontera_total):
    """
    Recibe una lista de tuplas (h, estado) y devuelve una cadena con
    una tabla ASCII de dos filas: estados y posiciones (índice en la frontera).
    """
    if not frontera_total:
        return ""

    estados = [str(estado) for (h, estado) in frontera_total]
    posiciones = [str(i) for i in range(len(estados))]

    # Calcular anchos por columna para alineación
    anchos = [max(len(estados[i]), len(posiciones[i])) for i in range(len(estados))]

    def fila(celdas):
        partes = [celdas[i].ljust(anchos[i]) for i in range(len(celdas))]
        return "| " + " | ".join(partes) + " |"

    primera = fila(estados)
    separador = "-" * len(primera)
    segunda = fila(posiciones)

    return "\n".join([primera, separador, segunda])


def imprimir_logs_formateados(camino_solucion, logs_por_estado, pausa_segundos=0.0, modo_interactivo=False):
    """
    Imprime los logs de expansión de acuerdo al formato solicitado por el usuario.
    Se asume que 'camino_solucion' y 'logs_por_estado' provienen de la misma ejecución.
    """
    if not camino_solucion:
        return

    # Encabezado global
    print("Solución Solución Best-First con heurística |J5-2|:\n\n")

    # Mostrar TODAS las expansiones en orden real (orden de extracción de la frontera)
    # Ordenamos por 'expansion_index' los logs que no sean objetivo y que se hayan expandido.
    logs_expandidos = [v for v in logs_por_estado.values() if not v.get("es_objetivo")]
    logs_expandidos.sort(key=lambda x: x["expansion_index"])

    for idx, log in enumerate(logs_expandidos):
        estado = log["estado"]
        accion_entrada = log.get("accion_entrada")
        descripcion = problema_jarras.descripcion_de_accion(accion_entrada)

        print(f"- Paso {idx:02d} | Estado {estado} <- {descripcion}")
        print(f"  Expansión #{log['expansion_index']:02d} (orden real) | h={log['heuristica']}")
        print("  Sucesores descubiertos (estado, acción, h):")
        for (suc, acc, h_suc) in log["sucesores"]:
            print(f"    - {suc}  <- {problema_jarras.descripcion_de_accion(acc)}  [h={h_suc}]")

        if log["sucesores_anadidos"]:
            añadidos_str = ", ".join([f"h={h}:{s}" for (h, s) in log["sucesores_anadidos"]])
        else:
            añadidos_str = ""
        print(f"  Sucesores añadidos: [{añadidos_str}]")

        if log["frontera_total"]:
            frontera_str = ", ".join([f"h={h}:{s}" for (h, s) in log["frontera_total"]])
        else:
            frontera_str = ""
        print(f"  Frontera total: [{frontera_str}]")

        # También mostrar la cola como tabla ASCII (estados/posición)
        if log["frontera_total"]:
            print("  Cola (formato tabla):")
            print(_tabla_ascii_frontera(log["frontera_total"]))

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
        print(f"- Paso {len(logs_expandidos):02d} | Estado {estado} <- {problema_jarras.descripcion_de_accion(obj.get('accion_entrada'))}")
        print("  [Objetivo detectado: no se expandió]")
        print("  Nuevos   | Descubiertos únicos: 0  |  Expandidos: 0")
        print("")
        print(f"Estado final alcanzado: {estado}")


def ejecutar_busqueda_y_mostrar(pausa_segundos=0.0, modo_interactivo=False):
    """
    Ejecuta la búsqueda Best-First del módulo 'jarras' y muestra el resultado.
    Además imprime estadísticas simples del recorrido.
    """
    # 1) Ejecutar búsqueda
    estado_objetivo, diccionario_padre, diccionario_accion, logs_por_estado = problema_jarras.busqueda_best_first(
        problema_jarras.obtener_estado_inicial()
    )

    # 2) Reconstruir el camino solución
    camino_solucion = problema_jarras.reconstruir_camino(
        estado_objetivo, diccionario_padre, diccionario_accion
    )

    # 3) Mostrar logs detallados
    imprimir_logs_formateados(
        camino_solucion,
        logs_por_estado,
        pausa_segundos=pausa_segundos,
        modo_interactivo=modo_interactivo,
    )

    # Línea adicional requerida por el ejemplo
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
        description="Runner de consola para el problema de las jarras (Best-First)."
    )
    parser.add_argument(
        "--pausa",
        type=float,
        default=0.0,
        help="Pausa (en segundos) entre pasos. Ejemplo: --pausa 0.4"
    )
    parser.add_argument(
        "--interactivo",
        action="store_true",
        help="Muestra los pasos en modo interactivo (ENTER para avanzar)."
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
        pausa_segundos=argumentos.pausa,
        modo_interactivo=argumentos.interactivo
    )


if __name__ == "__main__":
    main()

