import simulation
import utils

instructions, labels_map = utils.read_file("bubble.asm")
print(labels_map)
sim = simulation.Simulator(instructions, labels_map)
#  for i in range(4):
#      sim.memory[0+i*1024]=3
#      sim.memory[1+i*1024]=2
#      sim.memory[2+i*1024]=4

sim.run()

for i in range(4):
    print(sim.cores[i].registers)

print(sim.cores[1].pc)
print("Total clock cycles:", sim.clock)
for i in range(4):
    print(sim.memory[0+i*1024]," ",sim.memory[1+i*1024]," ",sim.memory[2+i*1024]," ",sim.memory[3+i*1024]," ",sim.memory[4+i*1024]," ",sim.memory[5+i*1024]," ",sim.memory[6+i*1024])