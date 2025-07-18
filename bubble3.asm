.data
array:  .word 9 ,5 ,1 0b10 7 0xFFFFFFFF 7 10 1 -10    # Unsorted array (5 elements)
len:    .word 10   
.word 3 3 3          

.text
  
main:
    la    x1, array      # x1 = base address of the array
    la    x2, len        # x2 = address of len
    lw    x3, 0(x2)       # x3 = array length
    addi  x4, x0, 0       # x4 = i = 0 (outer loop index)
OuterLoop:
    addi  x5, x3, -1      # x5 = (length - 1)
    blt   x4, x5, OuterBody   # if i < (length - 1), then continue outer loop
    jal   x0, EndSort     # else, jump to EndSort
OuterBody:
    addi  x7, x0, 0       # x7 = j = 0 (inner loop index)
    sub   x6, x3, x4      # x6 = length - i
    addi  x6, x6, -1      # x6 = (length - i - 1), inner loop limit
InnerLoop:
    slt   x13, x7, x6     # if j < (length - i - 1), x13 = 1
    bne   x13, x0, InnerBodyLabel   # if x13 != 0, execute inner loop
    jal   x0, OuterIncrement        # else, jump to outer loop increment
InnerBodyLabel:
    add   x8, x7, x7      # x8 = j * 2
    add   x8, x8, x8      # x8 = j * 4 (byte offset)
    add   x9, x1, x8      # x9 = address of array[j]
    lw    x10, 0(x9)      # x10 = array[j]
    lw    x11, 4(x9)      # x11 = array[j+1]
    slt   x12, x11, x10   # x12 = 1 if array[j+1] < array[j], else 0
    bne   x12, x0, Swap   # if x12 != 0, branch to Swap
    jal   x0, NoSwap      # else, jump to NoSwap
Swap:
    sw    x11, 0(x9)      # store array[j+1] into array[j]
    sw    x10, 4(x9)      # store array[j] into array[j+1]
NoSwap:
    addi  x7, x7, 1       # j = j + 1
    jal   x0, InnerLoop   # repeat inner loop
OuterIncrement:
    addi  x4, x4, 1       # i = i + 1
    jal   x0, OuterLoop   # repeat outer loop
EndSort:
   add x0 x0 x0
