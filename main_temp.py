import simulation


sim = simulation.Simulator()


sim.run()

for i in range(4):
    print(f"Register values of core {i} : {sim.cores[i].registers}")

for i in range(4):
    print(f"Stalls in core {i} : {sim.cores[i].stall_count}")

for i in range(4):
    print(f"IPC for core {i} : {sim.cores[i].ins_executed_count/sim.clock}")


print("Total clock cycles:", sim.clock)
print(" - - memory - - ")
for i in range(128):
     print(f"{i} = {sim.memory[i]} , {i+128} = {sim.memory[i+128]} , {i+128*2} = {sim.memory[i+128*2]} , {i+128*3} = {sim.memory[i+128*3]} , {i+128*4} = {sim.memory[i+128*4]} , {i+128*5} = {sim.memory[i+128*5]} , {i+128*6} = {sim.memory[i+128*6]} , {i+128*7} = {sim.memory[i+128*7]}")