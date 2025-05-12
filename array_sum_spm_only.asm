.data_scp 
arr: .word 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1 
      .word 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2 
      .word 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3 
      .word 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4

.data
partial_sum:.word 0 0 0 0 0

.text
add x2 x0 cid                     # Load cid (Ensure cid is set, modify this based on your needs)
la x1, arr                     # Load base address of arr
la x30, partial_sum            # Load storing address

addi x3, x0, 100
mul x4, x3, x2                 # Multiply offset by cid
add x1, x1, x4                 # Compute actual address for arr index

addi x3, x0, 4     
mul x4, x3, x2                 # Multiply offset by cid
add x30, x30, x4               # Compute actual storing address for partial_sum

addi x5, x0, 25                 # 3 elements per partial sum
addi x6, x0, 0                 # i = 0
addi x7, x0, 0                 # sum = 0

loop:
    beq x5, x6, end            # If i == 3, exit loop
    slli x20, x6, 2            # i * 4 (index offset)
    add x21, x1, x20           # Base + offset
    lw_spm x8, 0(x21)              # Load from correct address
    add x7, x7, x8             # Accumulate sum
    addi x6, x6, 1             # Increment i
    j loop

end:
    sw x7, 0(x30)              # Store the computed sum

beq cid x0 all
j finish

all:
    addi x9 x0 4                #Sum 4 partial sums
    addi x10 x0 0               #i = 0
    addi x11 x0 0               #sum = 0
    j loop2
loop2:
    beq x9 x10 finish2
    slli x20, x10, 2            # i * 4 (index offset)
    add x21, x30, x20           # Base + offset
    lw x8, 0(x21)              # Load from correct address
    add x11, x11, x8             # Accumulate sum
    addi x10, x10, 1             # Increment i
    j loop2
finish2:
    add x31 x0 x11
    addi x21 x21 4
    sw x11 0(x21)

    add x10 x0 x11
    addi x17 x0 1 
    ecall
    
finish:
    add x0 x0 x0