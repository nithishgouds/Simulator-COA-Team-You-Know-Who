import simulation


sim = simulation.Simulator()


sim.run()

for i in range(4):
    print(sim.cores[i].registers)


print("Total clock cycles:", sim.clock)
for i in range(20):
     print(f"{i} = {sim.memory[i]} , {i+512} = {sim.memory[i+512]} , {i+512*2} = {sim.memory[i+512*2]} , {i+512*3} = {sim.memory[i+512*3]} , {i+512*4} = {sim.memory[i+512*4]} , {i+512*5} = {sim.memory[i+512*5]} , {i+512*6} = {sim.memory[i+512*6]} , {i+512*7} = {sim.memory[i+512*7]}")