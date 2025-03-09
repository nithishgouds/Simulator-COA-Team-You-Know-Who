.data

final_sum: .word 0

single_core_sum_arr: .word 0 0 0 0

base: .word 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 
      .word 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 
      .word 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3 
      .word 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4


.text
add x1 cid x0 #x1 = cid
addi x2 x0 25 #array length
la x3 base 
la x16 single_core_sum_arr
la x28 final_sum
addi x4 x0 4
mul x5 x4 x2 #to be added to base = 100
mul x6 x5 x1
add x7 x3 x6 #addresss

add x10 x0 x0 #i
add x11 x0 x0 #sum

loop:
    beq x10 x2 final
    mul x12 x10 x4
    add x13 x7 x12
    lw x14 0(x13)
    add x11 x11 x14 
    addi x10 x10 1
    j loop

final:
    
    mul x17 x4 x1
    add x18 x17 x16
    sw x11 0(x18)

bne x1 x0 exit #exit for all cores except core 0

add x21 x0 x0 #coreid
addi x22 x0 4 #4 cores
add x31 x0 x0 #final sum

loop2:
    beq x21 x22 exit2
    mul x24 x4 x21 #100*core_id 
    add x25 x16 x24
    lw x26 0(x25)
    add x31 x31 x26
    addi x21 x21 1
    j loop2

exit2:

    sw x31 0(x28) #storing final sum

exit:
    add x0 x0 x0 #final sum will be stored in x31 of core 0