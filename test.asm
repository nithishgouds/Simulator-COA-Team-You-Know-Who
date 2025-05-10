addi x1 x0 1
addi x2 x0 2

beq cid x0 exit
addi x4 x0 4
sync
addi x5 x0 5

exit:
add x3 x1 x0 