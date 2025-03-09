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
for i in range(512):
     print(f"{i} = {sim.memory[i]} , {i+512} = {sim.memory[i+512]} , {i+512*2} = {sim.memory[i+512*2]} , {i+512*3} = {sim.memory[i+512*3]} , {i+512*4} = {sim.memory[i+512*4]} , {i+512*5} = {sim.memory[i+512*5]} , {i+512*6} = {sim.memory[i+512*6]} , {i+512*7} = {sim.memory[i+512*7]}")