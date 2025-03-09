addi x1 x0 3
sw x1 0(x0)
addi x1 x0 2
sw x1 4(x0)
addi x1 x0 1
sw x1 8(x0)
addi x1 x0 5
sw x1 12(x0)
addi x1 x0 6
sw x1 16(x0)
addi x1 x0 21
sw x1 20(x0)
addi x1 x0 20
sw x1 24(x0)
addi x1 x0 19
sw x1 28(x0)
addi x1 x0 -6
sw x1 32(x0)
add x1 x0 x0



addi x1 x0 10 # n length of array

addi x2 x0 0 # i - index of outer loop

addi x3 x1 -1 # n-1

addi x10 x0 0
#lw x10 base #base address

addi x11 x0 4 #register to store multiplication of 4 bytes



loop1:

    bge x2 x3 exit

    addi x4 x0 0 # j - index of inner loop

    sub x5 x3 x2 # n-1-i

    blt x4 x5 loop2

loop1med:

    addi x2 x2 1

    j loop1

    

    

loop2:

    j swapinit

loop2med:

    addi x4 x4 1

    bge x4 x5 loop1med # cl

    j loop2

    

    

swapinit:

    mul x12 x4 x11 #j*4

    addi x13 x12 4 #j*4+4

    add x12 x10 x12 #base+j

    add x13 x10 x13 #base+j+1

    lw x14 0(x12) #a[j]

    lw x15 0(x13) #a[j+1]

    blt x15 x14 swapfin

swapfinmed:

    j loop2med



swapfin:

    sw x14 0(x13)

    sw x15 0(x12)

    j swapfinmed   

    

exit:

    add x0 x0 x0

