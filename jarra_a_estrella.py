# jarras_a_estrella.py
# --------------------------------------------------------
# Problema de las jarras (3 L, 7 L, 9 L) resuelto con búsqueda A*
# Costos de acciones:
#   - Llenar = 1
#   - Vaciar = 2
#   - Transferir = 3
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