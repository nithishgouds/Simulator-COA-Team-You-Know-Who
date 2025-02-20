LABELx: add x0,x0,x1 #rd , rs1 , rs2
sub x0,x0,x1 #rd , rs1, rs2
bne x0, x2 , LABELy #rs1, rs2 , offset 
sw x0, 0(x3) #rd , offset (rs 1)

LABELy: sub x0, x0, x2

jal x0, LABELx #rd , offset (again , label will work )