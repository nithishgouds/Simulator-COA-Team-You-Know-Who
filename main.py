import simulation
import numpy as np
import matplotlib.pyplot as plt
sim = simulation.Simulator()
sim.run()
registers_per_core = [core.registers for core in sim.cores]  
registers_matrix = np.array(registers_per_core)
total_stalls = sum(core.stall_count for core in sim.cores)
for i, core in enumerate(sim.cores):
    print(f"Stalls in core {i} : {core.stall_count}")
print("Total stalls in all cores:", total_stalls)
print(" - - - - - - - - ")
for i, core in enumerate(sim.cores):
    print(f"IPC for core {i} : {core.ins_executed_count/sim.clock}")
print("Total clock cycles:", sim.clock)
print(" - - - - - - - - ")
fig, ax = plt.subplots(figsize=(15, 6))
ax.set_title(f"Registers - Cycle {sim.clock}", fontsize=14, fontweight='bold')
table_data = [["Core " + str(i)] + list(registers_matrix[i]) for i in range(len(registers_per_core))]
col_labels = ["Core"] + [str(i) for i in range(32)]
ax.axis("off")
table = ax.table(cellText=table_data, colLabels=col_labels, loc="center", cellLoc="center", 
                 cellColours=[["#EAF2F8" if i % 2 == 0 else "#D6EAF8"] * 33 for i in range(len(registers_per_core))])
table.auto_set_font_size(False)
table.set_fontsize(10)
table.auto_set_column_width([i for i in range(33)])
for i in range(33):
    cell = table[0, i]
    cell.set_text_props(weight='bold', color='white')
    cell.set_facecolor("#2E86C1")  # Dark Blue Header
plt.show()
memory_size = 1024
if len(sim.memory) < memory_size:
    print("Warning: Memory size is smaller than expected!")
memory_chunk = np.array(sim.memory[:memory_size]).reshape(32, 32)
fig, ax = plt.subplots(figsize=(15, 8))
ax.set_title(f"Memory (All {memory_size} address values)", fontsize=14, fontweight='bold')
memory_table_data = [["Block " + str(i)] + list(memory_chunk[i]) for i in range(len(memory_chunk))]
memory_col_labels = ["Memory Block"] + [str(i) for i in range(32)]
ax.axis("off")
mem_table = ax.table(cellText=memory_table_data, colLabels=memory_col_labels, loc="center", cellLoc="center",
                      cellColours=[["#FDEBD0" if i % 2 == 0 else "#F8C471"] * 33 for i in range(len(memory_chunk))])
mem_table.auto_set_font_size(False)
mem_table.set_fontsize(10)
mem_table.auto_set_column_width([i for i in range(33)])
for i in range(33):
    cell = mem_table[0, i]
    cell.set_text_props(weight='bold', color='black')
    cell.set_facecolor("#E67E22")  # Orange Header
plt.show()
