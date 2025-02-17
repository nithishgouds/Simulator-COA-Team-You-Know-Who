import simulation
import utils

instructions, labels_map = utils.read_file("test.asm")
sim = simulation.Simulator(instructions, labels_map)
sim.run()

for i in range(4):
    print(sim.cores[i].registers)

print(sim.cores[1].pc)
print("Total clock cycles:", sim.clock)
