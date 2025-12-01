ADD $v1, $at, $v0
SUB $a1, $v1, $a0
ADDI $t1, $a0, 100
LW $t2, 4($t2)
AND $t3, $v1, $t2
BEQ $t0, $t1, 1
J 12
ADDI $t0, $zero, 0