addi x1 x0 3
sw x1 0(x0)
addi x1 x0 2
sw x1 4(x0)
addi x1 x0 4
sw x1 8(x0)
lw x1 0(x0)       
lw x2 4(x0)       
blt x2 x1 swap01  
j next01          
swap01:
add x3 x1 x0      
add x1 x2 x0     
add x2 x3 x0     
next01:
sw x1 0(x0)      
sw x2 4(x0)      
lw x1 4(x0)       
lw x2 8(x0)       
blt x2 x1 swap12  
j next12
swap12:
add x3 x1 x0      
add x1 x2 x0      
add x2 x3 x0      
next12:
sw x1 4(x0)       
sw x2 8(x0)      
lw x1 0(x0)      
lw x2 4(x0)       
blt x2 x1 swap01b 
j done
swap01b:
add x3 x1 x0     
add x1 x2 x0      
add x2 x3 x0     
sw x1 0(x0)       
sw x2 4(x0)      
done:
    sub x9 x9 x9
    add x0 x0 x0