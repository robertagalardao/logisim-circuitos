# CASO 1 - EMERGÊNCIA
# Entradas:
# DIST_ATUAL = 2
# VEL_ATUAL = 60
# DIST_SEGURA = 3
# VEL_MAX = 30
#
# Saída esperada:
# Mem[0x20] = 2
# Mem[0x21] = 2

ADDI R1, R0, 2
SW R1, R0, 0x10

ADDI R1, R0, 31
ADDI R1, R1, 29
SW R1, R0, 0x11

ADDI R1, R0, 3
SW R1, R0, 0x12

ADDI R1, R0, 30
SW R1, R0, 0x13

LW R1, R0, 0x10
LW R2, R0, 0x11
LW R3, R0, 0x12
LW R4, R0, 0x13

SLT R5, R1, R3
BEQ R5, R0, normal

SLT R6, R4, R2
BEQ R6, R0, alerta

emergencia:
ADDI R7, R0, 2
ADDI R6, R0, 31
ADDI R6, R6, 1
SW R7, R6, 0
SW R7, R6, 1
JAL R0, fim

alerta:
ADDI R7, R0, 1
ADDI R6, R0, 31
ADDI R6, R6, 1
SW R7, R6, 0
SW R7, R6, 1
JAL R0, fim

normal:
ADDI R7, R0, 0
ADDI R6, R0, 31
ADDI R6, R6, 1
SW R7, R6, 0
SW R7, R6, 1

fim:
JAL R0, fim