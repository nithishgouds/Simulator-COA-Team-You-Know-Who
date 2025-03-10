import simulation
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
sim = simulation.Simulator()
sim.run()
registers_per_core = [core.registers for core in sim.cores]  
registers_matrix = np.array(registers_per_core)

total_stalls=0
for i in range(4):
    total_stalls+=sim.cores[i].stall_count
    print(f"Stalls in core {i} : {sim.cores[i].stall_count}")

print("Total stalls in all cores :",total_stalls)
print(" - - - - - - - - ")

for i in range(4):
    print(f"IPC for core {i} : {sim.cores[i].ins_executed_count/sim.clock}")


print("Total clock cycles:", sim.clock)
print(" - - - - - - - - ")

fig, ax = plt.subplots(figsize=(12, 5))
sns.heatmap(registers_matrix, annot=True, fmt="d", cmap="Blues", linewidths=0.5, ax=ax)
ax.set_xlabel("Registers (0-31)")
ax.set_ylabel("Cores")
ax.set_title(f"Registers - Cycle {sim.clock}")
ax.set_yticklabels([f"Core {i}" for i in range(len(registers_per_core))], rotation=0)
plt.show()
for i, core_regs in enumerate(registers_per_core):
    pass
    #print(f"Core {i} Registers: {core_regs}")
memory_size = 1024
if len(sim.memory) < memory_size:
    print("Warning: Memory size is smaller than expected!")
memory_chunk = np.array(sim.memory[:memory_size]).reshape(32, 32)
fig, ax = plt.subplots(figsize=(12, 6))
sns.heatmap(memory_chunk, annot=True, fmt="d", cmap="Oranges", linewidths=0.5, ax=ax)
ax.set_title(f"Memory (All {memory_size} address values) ")
ax.set_xlabel("Address Offset (0-31)")
ax.set_ylabel("Memory Blocks")
plt.show()