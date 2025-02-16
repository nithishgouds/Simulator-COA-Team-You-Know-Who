addi x1 x0 5
add x2 x1 x0

start:
    add x3 x1 x2
    bne x3 x1 exit
    addi x5 x0 5

exit:
    
    addi x6 x0 6
    addi x7 x0 7