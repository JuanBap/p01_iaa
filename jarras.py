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