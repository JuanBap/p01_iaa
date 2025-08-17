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

    print("\nSolución (Best-First con heurística |J5 - 2|):\n")
    for indice, (estado, codigo_accion) in enumerate(camino_solucion):
        descripcion = problema_jarras.descripcion_de_accion(codigo_accion)
        print(f"Paso {indice:02d}: Estado {str(estado):>7}  <- {descripcion}")
        if modo_interactivo and indice < len(camino_solucion) - 1:
            input("Presiona ENTER para continuar...")
        elif pausa_segundos > 0:
            time.sleep(pausa_segundos)

    estado_final = camino_solucion[-1][0]
    print("\nEstado final alcanzado:", estado_final)


def ejecutar_busqueda_y_mostrar(pausa_segundos=0.0, modo_interactivo=False):
    """
    Ejecuta la búsqueda Best-First del módulo 'jarras' y muestra el resultado.
    Además imprime estadísticas simples del recorrido.
    """
    # 1) Ejecutar búsqueda
    estado_objetivo, diccionario_padre, diccionario_accion = problema_jarras.busqueda_best_first(
        problema_jarras.obtener_estado_inicial()
    )

    # 2) Reconstruir el camino solución
    camino_solucion = problema_jarras.reconstruir_camino(
        estado_objetivo, diccionario_padre, diccionario_accion
    )

    # 3) Mostrar solución
    mostrar_camino_solucion(
        camino_solucion=camino_solucion,
        pausa_segundos=pausa_segundos,
        modo_interactivo=modo_interactivo
    )

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

