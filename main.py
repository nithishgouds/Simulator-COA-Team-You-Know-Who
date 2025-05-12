import simulation
import numpy as np
import matplotlib.pyplot as plt
sim = simulation.Simulator()
for i in range(4):
    sim.cores[i].sim=sim
sim.run()

# for i in range(256):
#     print(f"{i*4} : {sim.memory[i]} | {(i+256)*4} : {sim.memory[i+256]} | {(i+512)*4} : {sim.memory[i+512]} | {(i+1024)*4} : {sim.memory[i+768]}")
# Dynamically calculate the maximum data width
max_len = max(len(str(v)) for v in sim.memory)
data_width = max(max_len, 10) + 2  # Add padding
addr_width = 4  # Increase to accommodate large addresses like 4092

# Print header

# print("Main Memory (All 4096 bytes) - 4 bytes per line")
# print(
#     f"{'Addr':<{addr_width}} : {'Data':<{data_width}} | "
#     f"{'Addr':<{addr_width}} : {'Data':<{data_width}} | "
#     f"{'Addr':<{addr_width}} : {'Data':<{data_width}} | "
#     f"{'Addr':<{addr_width}} : {'Data':<{data_width}}"
# )

# # Print values
# for i in range(256):
#     addr1 = i * 4
#     addr2 = (i + 256) * 4
#     addr3 = (i + 512) * 4
#     addr4 = (i + 768) * 4

#     data1 = str(sim.memory[i])
#     data2 = str(sim.memory[i + 256])
#     data3 = str(sim.memory[i + 512])
#     data4 = str(sim.memory[i + 768])

#     print(
#         f"{addr1:<{addr_width}} : {data1:<{data_width}} | "
#         f"{addr2:<{addr_width}} : {data2:<{data_width}} | "
#         f"{addr3:<{addr_width}} : {data3:<{data_width}} | "
#         f"{addr4:<{addr_width}} : {data4:<{data_width}}"
#     )

start = 1024 * 76     # 8192
end = 1024 * 80     # 12288
start_index = start // 4  # index in words
end_index = end // 4

# print("Main Memory (8192 to 12288 bytes) - 4 bytes per line")
# print(
#     f"{'Addr':<{addr_width}} : {'Data':<{data_width}} | "
#     f"{'Addr':<{addr_width}} : {'Data':<{data_width}} | "
#     f"{'Addr':<{addr_width}} : {'Data':<{data_width}} | "
#     f"{'Addr':<{addr_width}} : {'Data':<{data_width}}"
# )

# # Print values
# for i in range(start_index, end_index, 256):  # step by 256 to get 256 rows
#     for j in range(256):
#         addr1 = (i + j) * 4
#         addr2 = (i + j + 256) * 4
#         addr3 = (i + j + 512) * 4
#         addr4 = (i + j + 768) * 4

#         data1 = str(sim.memory[i + j])
#         data2 = str(sim.memory[i + j + 256])
#         data3 = str(sim.memory[i + j + 512])
#         data4 = str(sim.memory[i + j + 768])

#         print(
#             f"{addr1:<{addr_width}} : {data1:<{data_width}} | "
#             f"{addr2:<{addr_width}} : {data2:<{data_width}} | "
#             f"{addr3:<{addr_width}} : {data3:<{data_width}} | "
#             f"{addr4:<{addr_width}} : {data4:<{data_width}}"
#         )  # only run one 256-row block to cover 4096 bytes




registers_per_core = [core.registers for core in sim.cores]  
registers_matrix = np.array(registers_per_core)
total_stalls = sum(core.stall_count for core in sim.cores)
print(" - - - - - - - - ")
for i, core in enumerate(sim.cores):
    print(f"Stalls in core {i} : {core.stall_count}")
print("Total stalls in all cores:", total_stalls)
print(" - - - - - - - - ")
for i, core in enumerate(sim.cores):
    print(f"IPC for core {i} : {core.ins_executed_count/sim.clock}")
print("Total clock cycles :", sim.clock)
print(" - - - - - - - - ")
L1D_missrate = 0
L1I_missrate = 0
L2D_missrate = 0
if sim.L1D.cache_accesses != 0:
    L1D_missrate = sim.L1D.cache_misses / sim.L1D.cache_accesses
if sim.L1I.cache_accesses != 0:
    L1I_missrate = sim.L1I.cache_misses / sim.L1I.cache_accesses
if sim.L2.cache_accesses != 0:
    L2D_missrate = sim.L2.cache_misses / sim.L2.cache_accesses
print("L1D Miss Rate :", L1D_missrate*100)
print("L1I Miss Rate :", L1I_missrate*100)   
print("L2D Miss Rate :", L2D_missrate*100)    
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
#plt.show()
