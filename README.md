## Primer proyecto Intro. IA — Problema de las jarras

Proyecto educativo que resuelve el clásico problema de las jarras con dos variantes:

- Best-First (greedy) en el problema 5 L y 4 L con heurística h(R5, R4) = |J5 − 2| (objetivo: 2 litros en la jarra de 5 L).
- A* en el problema 3 L, 7 L y 9 L con costos Llenar=1, Vaciar=3, Transferir=2 (objetivo: 6 litros en la jarra de 7 L).

### ¿De qué trata?
- **Estado**: `(litros_jarra5, litros_jarra4)`
- **Capacidades**: jarra de 5 L y jarra de 4 L
- **Acciones**: `L5`, `L4`, `V5`, `V4`, `T54`, `T45`
- **Heurística**: `h(estado) = |litros_jarra5 − 2|`
- **Algoritmo**: Best-First usando una cola de prioridad que ordena por h(n)

Archivos principales:
- `jarras.py`: definición del problema 5L-4L y búsqueda Best-First.
- `runner.py`: runner Best-First (CLI) para mostrar pasos, logs y métricas.
- `jarras_a_estrella.py`: definición del problema 3L-7L-9L y búsqueda A* con costos.
- `runner2.py`: runner A* (CLI) que imprime TODAS las expansiones en orden real.

### Requisitos
- Python 3.8+ (sin dependencias externas)

### Cómo clonar el repositorio
SSH:
```bash
git clone git@github.com:JuanBap/p01_iaa.git
cd p01_iaa
```

HTTPS:
```bash
git clone https://github.com/JuanBap/p01_iaa.git
cd p01_iaa
```

### Cómo ejecutar (y qué resultados arroja)

#### 1) Best-First (problema 5 L y 4 L)

- Opción A: usar el runner con CLI (recomendado)
```bash
python3 runner.py                 # ejecución estándar
python3 runner.py --pausa 0.4     # pausa de 0.4 s entre pasos
python3 runner.py --interactivo   # modo paso a paso (ENTER para avanzar)
python3 runner.py --interactivo --pausa 0.3
```
Qué imprime `runner.py`:
- Encabezado de la solución con la heurística utilizada.
- Para cada expansión en orden real: estado, acción de entrada, sucesores (con h), "Sucesores añadidos", "Frontera total" y la cola como tabla.
- Contadores por paso: "Descubiertos únicos" y "Expandidos"; totales acumulados.
- Al final: "Camino solución reconstruido con N pasos", "Estado final alcanzado: (...)" y un "Resumen" con "Acciones ejecutadas" y "Estados descubiertos (nodos generados)".

- Opción B: ejecutar directamente el módulo del problema
```bash
python3 jarras.py
```
Qué imprime `jarras.py`:
- La secuencia de estados y acción aplicada para el camino solución.
- El estado final alcanzado. (No imprime el historial completo de expansiones.)

#### 2) A* (problema 3 L, 7 L y 9 L)

- Opción A: usar el runner con CLI (recomendado)
```bash
python3 runner2.py                # ejecución estándar
python3 runner2.py --pausa 0.4    # pausa de 0.4 s entre pasos
python3 runner2.py --interactivo  # modo paso a paso (ENTER para avanzar)
```
Qué imprime `runner2.py`:
- Encabezado de la solución con costos (L=1, V=3, T=2) y h(n)=|jarra2-6|.
- Muestra TODAS las expansiones en orden real (no sólo el camino): por cada expansión imprime g, h, f, tabla de sucesores (con acción y costo), "Sucesores añadidos", "Frontera total" y la cola en tabla.
- Contadores por paso y totales acumulados.
- Al final: "Camino solución reconstruido con N pasos", "Estado final alcanzado: (...)" y "Resumen" con métricas.

- Opción B: ejecutar directamente el módulo del problema
```bash
python3 jarras_a_estrella.py
```
Qué imprime `jarras_a_estrella.py`:
- Traza detallada a lo largo del camino solución: por cada estado del camino muestra sucesores, añadidos, frontera y cola, más contadores.
- Resumen final con acciones ejecutadas y estados descubiertos.

### Ejemplo de salida (recortado)
```text
Solución (Best-First con heurística |J5 - 2|):
Paso 00: Estado (0, 0)  <- Estado inicial
Paso 01: Estado (5, 0)  <- Llenar jarra de 5 L
...
Estado final alcanzado: (2, X)

Resumen:
- Acciones ejecutadas: N
- Estados descubiertos (nodos generados): M
```

Nota: Los valores pueden variar según el orden de expansión de estados con la heurística.

### Conceptos clave implementados
- Representación de estado y verificación de estado final
- Generación de acciones válidas con precondiciones
- Modelo de transición (incluye transferencias con `min`/`max` para sobrantes)
- Función heurística y cola de prioridad (greedy Best-First)
- Reconstrucción del camino y descripciones legibles de acciones

### Estructura del proyecto
```text
p01_iaa/
├── jarras.py               # 5L-4L Best-First
├── runner.py               # Runner Best-First (CLI)
├── jarras_a_estrella.py    # 3L-7L-9L A*
├── runner2.py              # Runner A* (CLI)
└── README.md
```

### Licencia
Uso educativo. Ajusta la licencia según tus necesidades si reutilizas el código.