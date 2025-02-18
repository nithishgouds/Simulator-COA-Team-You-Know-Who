import simulation


sim = simulation.Simulator()


sim.run()

for i in range(4):
    print(sim.cores[i].registers)

print(sim.cores[0].pc)
print("Total clock cycles:", sim.clock)
for i in range(4):
    print(sim.memory[0+i*1024]," ",sim.memory[1+i*1024]," ",sim.memory[2+i*1024]," ",sim.memory[3+i*1024]," ",sim.memory[4+i*1024]," ",sim.memory[5+i*1024]," ",sim.memory[6+i*1024]," ",sim.memory[7+i*1024]," ",sim.memory[8+i*1024]," ",sim.memory[9+i*1024])