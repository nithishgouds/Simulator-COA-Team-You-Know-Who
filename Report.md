#Simulator-COA-You-Know-Who
Authors:Anirudh, Nithish
ID: CS23B025, CS23B052

---

## SYNC report

Our SYNC opcode implementation:
- in phase 2 we used a queue for implemetation of single instruction fetch 
- now in phase 3 we extended it to check if any instruction pc is "sync" , if yes then we will stop the core till all other cores pc is same as stopped core pc


## Output Report

### Algorithms

We have to implement Strided array addition without using scratchpad memory and then using Strided array addition using scratchpad memory. In which we will take a stride and then add elements in the array by striding and sum this again and again 100 times.

### Codes

asm=
Algorithm - 1

.data
arr: .word 1, 2, 3, 4, 5 .... 9981, ... 10000
sum: .word 0, 0, 0, 0, 0

.text
add x1,x0,cid  #x1 = cid
add x2,x0,x0   #x2 = s
addi x3,x0,100 #x3 = x
addi x4,x0,4   #x4 = 4
la x5,arr      #x5 = arr base
la x6,sum      #x6 = sum base
addi x7,x0,0   #x7 = i
addi x8,x0,25  #x8 = 25
addi x30,x0,100 #x30 = 100


loop1:
    beq x7 x30 next2
    addi x7 x7 1
    addi x12 x0 0
    loop2:
    beq x12 x30 loop1
    mul x13 x4 x1 
    add x13 x13 x6
    lw x2 0(x13)

    mul x14 x3 x12
    mul x14 x14 x4
    add x14 x14 x5
    lw x15 0(x14)

    add x2 x2 x15

    sw x2,0(x13) 
    addi x12 x12 1
    j loop2

next2:
    beq x1,x0,total_sum 
    j exit

total_sum:
    add x2,x0,x0 
    la x11,sum 
    addi x12,x0,0 #i = 0
    addi x13,x0,4 #total cores = 4

sum_loop:
    beq x12,x13,store_total # if i == 4, exit loop
    lw x14,0(x11) #Load sum[i]
    add x2,x2,x14 #Add to total sum
    addi x11,x11,4 #Move to next sum element
    addi x12,x12,1 #i++
    j sum_loop

store_total:
    la x11,sum 
    addi x11,x11,0 #Point to the last word (total sum location)
    sw x2,0(x11) #Store total sum in the last word of sum array  
exit:
    add x0 x0 x0
   


asm=
Algorithm - 2

.data_scp
spm_arr: .word 0 0 ....0 #100 times

.data
arr: .word 1 2 3 4 .... 9889 ... 10000
sum: .word 0, 0, 0, 0, 0

.text
add x1,x0,cid  #x1 = cid
add x2,x0,x0   #x2 = s
addi x3,x0,100 #x3 = x
addi x4,x0,4   #x4 = 4
la x5,arr      #x5 = arr base
la x6,sum      #x6 = sum base
addi x7,x0,0   #x7 = i
addi x8,x0,25  #x8 = 25
la x11 spm_arr
addi x30,x0,100 #x30 = 100

loop1:
    beq x7 x30 next
    mul x9 x3 x7
    mul x9 x9 x4
    add x9 x9 x5
    lw x10 0(x9)
    sw_spm x10 0(x11)
    addi x11 x11 4
    addi x7 x7 1
    j loop1

next:
    addi x7 x0 0
    la x11 spm_arr
    loop2:
        beq x7 x30 next2
        addi x7 x7 1
        addi x12 x0 0
        loop3:
        beq x12 x30 loop2
        mul x13 x4 x1 
        add x13 x13 x6
        lw x2 0(x13)

        mul x14 x12 x4
        add x14 x14 x11
        lw_spm x15 0(x14)

        add x2 x2 x15

        sw x2,0(x13) 
        addi x12 x12 1
        j loop3

next2:
    beq x1,x0,total_sum 
    j exit

total_sum:
    add x2,x0,x0 
    la x11,sum 
    addi x12,x0,0 #i = 0
    addi x13,x0,4 #total cores = 4

sum_loop:
    beq x12,x13,store_total # if i == 4, exit loop
    lw x14,0(x11) #Load sum[i]
    add x2,x2,x14 #Add to total sum
    addi x11,x11,4 #Move to next sum element
    addi x12,x12,1 #i++
    j sum_loop

store_total:
    la x11,sum 
    addi x11,x11,0 #Point to the last word (total sum location)
    sw x2,0(x11) #Store total sum in the last word of sum array  
exit:
    add x0 x0 x0 


### PART 1

This is the cache configuration for part1 and spm has 400 Bytes direct mapped cache is the type of cache here. The assembly codes for the both algorithms. 

Here the answer must be sum of all elements in the AP:
1 101 201 ... 9901 times 100 and then times 4 for all cores.

config=
L1D_cache_size,L1D_associativity,L1D_latency
400,1,4
L1I_cache_size,L1I_associativity,L1I_latency
400,4,4
L2_cache_size,L2_associativity,L2_latency
1024,8,8
cache_block_size,mm_latency
8,20
 


#### Algorithm 1


Stalls in core 0 : 306753
Stalls in core 1 : 306742
Stalls in core 2 : 323371
Stalls in core 3 : 306709
Total stalls in all cores: 1243575
 - - - - - - - -
IPC for core 0 : 0.045140899467389556
IPC for core 1 : 0.04512928105648084
IPC for core 2 : 0.04512928105648084
IPC for core 3 : 0.04512928105648084
Total clock cycles : 2668179
 - - - - - - - -
L1D Miss Rate : 23.015707678846713 %
L1I Miss Rate : 0.004152047997674853 %
L2D Miss Rate : 36.25904486251809 %
 - - - - - - - -

#### Algorithm 2


Stalls in core 0 : 93353
Stalls in core 1 : 93328
Stalls in core 2 : 93328
Stalls in core 3 : 93328
Total stalls in all cores: 373337
 - - - - - - - -
IPC for core 0 : 0.14815549094876623
IPC for core 1 : 0.14811557371050688
IPC for core 2 : 0.14811557371050688
IPC for core 3 : 0.14811557371050688
Total clock cycles : 751555
 - - - - - - - -
L1D Miss Rate : 0.12685778247621418 %
L1I Miss Rate : 0.00514281600032914 %
L2D Miss Rate : 100.0 %
 - - - - - - - -




### PART 2

This is the cache configuration for part1 and spm has 400 Bytes fully associative cache is the type of cache here. The assembly codes for the both algorithms. 

Here the answer must be sum of all elements in the AP:
1 101 201 ... 9901 times 100 and then times 4 for all cores.

cache=
cache_type,latency,block_size,associativity,cache_size
L1_Instr,4,8,4,400
L1_Data,4,8,50,400
L2,8,8,8,1024
Main_Memory,20,,,  

#### Algorithm - 1

Stalls in core 0 : 343573
Stalls in core 1 : 343548
Stalls in core 2 : 343548
Stalls in core 3 : 343548
Total stalls in all cores: 1374217
 - - - - - - - - 
IPC for core 0 : 0.11509727135640936
IPC for core 1 : 0.11506764750290027
IPC for core 2 : 0.11506764750290027
IPC for core 3 : 0.11506764750290027
Total clock cycles : 1046454
 - - - - - - - - 
L1D Miss Rate : 8.334652722803217 %
L1I Miss Rate : 0.003830713125555453 %
L2D Miss Rate : 66.83296747156257 %
 - - - - - - - - 

#### Algorithm - 2

Stalls in core 0 : 93353
Stalls in core 1 : 93328
Stalls in core 2 : 93328
Stalls in core 3 : 93328
Total stalls in all cores: 373337
 - - - - - - - -
IPC for core 0 : 0.14815549094876623
IPC for core 1 : 0.14811557371050688
IPC for core 2 : 0.14811557371050688
IPC for core 3 : 0.14811557371050688
Total clock cycles : 751555
 - - - - - - - -
L1D Miss Rate : 0.12685778247621418 %
L1I Miss Rate : 0.00514281600032914 %
L2D Miss Rate : 100.0 %
 - - - - - - - -


### PART 3

As observed above in part 1 and 2 eventhough there is a difference in the algorithm 1 when using direct mapped and fully associative cache because we don't use scratchpad at all in algorithm 1. 

But when we use scratchpad memory like in algorithm 2 we don't see any difference because we load from memory and first load is always a miss so cache doesn't account for any stalls or cycle changes. All the main operations are scratch pad operations only hence we can infer that even if there is a change in associativity when using only scratch pad for operations we don't see any difference.

#### Why is SPM better than L1D?

Scratchpad Memories (SPMs) generally have lower latencies and power requirements than caches because they are simpler, software-managed memories without the need for complex control logic like tag comparisons, replacement policies, or coherence protocols. In caches, each memory access involves checking the tag store and potentially performing replacement or write-back operations, which adds hardware overhead and power consumption. In contrast, SPMs behave like regular RAM with predictable access patterns determined by software, allowing faster and more energy-efficient data retrieval.

#### Alogorithms With Changes

Now to determine how scratch pad improves the no of cycles and improves the performance. To prove this we will run the sum cycle 200 times, once without using SPM at all, then we will use SPM for the first 100 strides, and use the memory system directly for the next 100 strides. We will check both the outputs and determine which is better and why. 

#### Cache config
L1D_cache_size,L1D_associativity,L1D_latency
400,50,1
L1I_cache_size,L1I_associativity,L1I_latency
400,4,4
L2_cache_size,L2_associativity,L2_latency
1024,8,8
cache_block_size,mm_latency
8,20


#### Output
Without SPM
code=
Algorithm - 3

.data
arr: .word 1 2 3 4 ..... 20000 
sum: .word 0, 0, 0, 0, 0


.text
add x1 x0 cid  #x1 = cid
add x2 x0 x0   #x2 = s
addi x3 x0 100 #x3 = x
addi x4 x0 4   #x4 = 4
la x5 arr      #x5 = arr base
la x6 sum      #x6 = sum base
addi x7 x0 0   #x7 = i
addi x8 x0 25  #x8 = 25
addi x30 x0 100 #x30 = 100
addi x29 x0 200


loop1:
    beq x7 x30 next2
    addi x7 x7 1
    addi x12 x0 0
    loop2:
    beq x12 x29 loop1
    mul x13 x4 x1
    add x13 x13 x6
    lw x2 0(x13)

    mul x14 x3 x12
    mul x14 x14 x4
    add x14 x14 x5
    lw x15 0(x14)

    add x2 x2 x15

    sw x2 0(x13)
    addi x12 x12 1
    j loop2

next2:
    beq x1 x0 total_sum
    j exit

total_sum:
    add x2 x0 x0
    la x11 sum
    addi x12 x0 0 #i = 0
    addi x13 x0 4 #total cores = 4

sum_loop:
    beq x12 x13 store_total # if i == 4  exit loop
    lw x14 0(x11) #Load sum[i]
    add x2 x2 x14 #Add to total sum
    addi x11 x11 4 #Move to next sum element
    addi x12 x12 1 #i++
    j sum_loop

store_total:
    la x11 sum
    addi x11 x11 0 #Point to the last word (total sum location)
    sw x2 0(x11) #Store total sum in the last word of sum array  
exit:
    addi x1 x0 0


Stalls in core 0 : 640038
Stalls in core 1 : 640028
Stalls in core 2 : 640028
Stalls in core 3 : 640028
Total stalls in all cores: 2560122
 - - - - - - - - 
IPC for core 0 : 0.11769649776496825
IPC for core 1 : 0.11768132343640782
IPC for core 2 : 0.11768132343640782
IPC for core 3 : 0.11768132343640782
Total clock cycles : 2042924
 - - - - - - - -
L1D Miss Rate : 8.33399304181163 %
L1I Miss Rate : 0.002015161692735822 %
L2D Miss Rate : 100.0 %
 - - - - - - - -

With SPM
code=
Algorithm - 4

.scratchpad
spm_arr:.word 0 0 0 0 0
.data
arr: .word 1 2 3 .... 20000
sum: .word 0, 0, 0, 0, 0

.text
add x1,x0,cid       # x1 = cid
add x2,x0,x0        # x2 = s (initial sum)
addi x3,x0,100      # x3 = stride factor X = 100
addi x4,x0,4        # x4 = size of word (4 bytes)
la x5,arr           # x5 = base address of arr
la x6,sum           # x6 = base address of sum
addi x7,x0,0        # x7 = loop counter i
addi x30,x0,100     # x30 = constant 100
addi x29,x0,200     # x29 = constant 200 (for full range)

loop1:
    beq x7 x30 next2        # if i == 100, jump to next2
    addi x7 x7 1            # i++
    addi x12 x0,0           # j = 0

    loop2:
        beq x12 x30 loop1   # if j == 100, go to next i
        mul x13 x4 x1       # x13 = 4 * cid
        add x13 x13 x6      # x13 = &sum[cid]
        lw x2 0(x13)        # load sum[cid] into x2

        mul x14 x3 x12      # x14 = stride * j
        mul x14 x14 x4      # x14 = byte offset
        add x14 x14 x5      # x14 = address of a[j * stride]
        lw x15 0(x14)       # load a[j * stride] into x15

        add x2 x2 x15       # sum += value
        sw x2 0(x13)        # store updated sum

        addi x12 x12 1      # j++
        j loop2

next2:
    la x11,spm_arr          # initialize x11 to base of spm_arr
    addi x7 x0 100


loop3:
    beq x7 x29 next3
    mul x9 x3 x7
    mul x9 x9 x4
    add x9 x9 x5
    lw x10 0(x9)
    sw_spm x10 0(x11)
    addi x11 x11 4
    addi x7 x7 1
    j loop3

next3:  
    addi x7 x0 0
    la x11 spm_arr
    loop4:
        beq x7 x30 next4
        addi x7 x7 1
        addi x12 x0 0
        loop5:
        beq x12 x30 loop4

        mul x14 x12 x4
        add x14 x14 x11
        lw_spm x15 0(x14)

        add x2 x2 x15
        addi x12 x12 1
        j loop5

next4:
    mul x13 x4 x1
    add x13 x13 x6
    sw x2 0(x13)
    beq x1,x0,total_sum 
    j exit

total_sum:
    add x2,x0,x0 
    la x11,sum 
    addi x12,x0,0 #i = 0
    addi x13,x0,4 #total cores = 4

sum_loop:
    beq x12,x13,store_total # if i == 4, exit loop
    lw x14,0(x11) #Load sum[i]
    add x2,x2,x14 #Add to total sum
    addi x11,x11,4 #Move to next sum element
    addi x12,x12,1 #i++
    j sum_loop

store_total:
    la x11,sum 
    addi x11,x11,0 #Point to the last word (total sum location)
    sw x2,0(x11) #Store total sum in the last word of sum array  
exit:
    add x0 x0 x0

 - - - - - - - - 
Stalls in core 0 : 266567
Stalls in core 1 : 266557
Stalls in core 2 : 266557
Stalls in core 3 : 266557
Total stalls in all cores: 1066238
 - - - - - - - -
IPC for core 0 : 0.13624578568358078
IPC for core 1 : 0.13622375933011463
IPC for core 2 : 0.13622375933011463
IPC for core 3 : 0.13622375933011463
Total clock cycles : 1407405
 - - - - - - - -
L1D Miss Rate : 8.391399314004767 %
L1I Miss Rate : 0.0038908670738321506 %
L2D Miss Rate : 67.18950379796784 %
 - - - - - - - -

Almost half a million cycle difference.
So as we can observe there is a significant decrease in the no of cycles taken. So SPM performs better since the Hit Rate in SPM is same as memory that is 100%, so the stalls and miss penalities of the cache are reduced.


