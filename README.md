## Primer proyecto Intro. IA — Problema de las jarras (5 L y 4 L) con búsqueda Best-First

Proyecto educativo que resuelve el clásico problema de las jarras usando búsqueda Best-First (greedy) con la heurística h(R5, R4) = |J5 − 2|. El objetivo es obtener exactamente 2 litros en la jarra de 5 litros.

### ¿De qué trata?
- **Estado**: `(litros_jarra5, litros_jarra4)`
- **Capacidades**: jarra de 5 L y jarra de 4 L
- **Acciones**: `L5`, `L4`, `V5`, `V4`, `T54`, `T45`
- **Heurística**: `h(estado) = |litros_jarra5 − 2|`
- **Algoritmo**: Best-First usando una cola de prioridad que ordena por h(n)

Archivos principales:
- `jarras.py`: definición del problema, heurística, operadores y la búsqueda Best-First.
- `runner.py`: runner de consola para ejecutar la búsqueda y mostrar pasos y métricas.

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

### Cómo ejecutar
Opción 1: usar el runner con CLI (recomendado)
```bash
python3 runner.py                 # ejecución estándar
python3 runner.py --pausa 0.4     # pausa de 0.4 s entre pasos
python3 runner.py --interactivo   # modo paso a paso (ENTER para avanzar)
python3 runner.py --interactivo --pausa 0.3
```

Lo que muestra el runner:
- Secuencia de estados y la acción aplicada en cada paso
- Resumen final con número de acciones y estados descubiertos

Opción 2: ejecutar directamente el módulo del problema
```bash
python3 jarras.py
```

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
├── jarras.py    # Lógica del problema y de la búsqueda
├── runner.py    # Runner de consola con flags --pausa y --interactivo
└── README.md
```

### Licencia
Uso educativo. Ajusta la licencia según tus necesidades si reutilizas el código.