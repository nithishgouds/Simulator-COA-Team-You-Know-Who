.data 
arr: .word 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16 17 18 19 20 21 22 23 24 25  
     .word 26 27 28 29 30 31 32 33 34 35 36 37 38 39 40 41 42 43 44 45 46 47 48 49 50
     .word 51 52 53 54 55 56 57 58 59 60 61 62 63 64 65 66 67 68 69 70 71 72 73 74 75 
     .word 76 77 78 79 80 81 82 83 84 85 86 87 88 89 90 91 92 93 94 95 96 97 98 99 100
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
    lw x8, 0(x21)              # Load from correct address
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