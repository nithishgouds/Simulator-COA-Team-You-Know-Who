# Simulator-COA ( TEAM NAME - You Know Who )




## Project Overview:<br>

This project is an Instruction Set Simulator built in Python to simulate the execution of various instructions such as add, addi, sub, and more. The simulator models a multi-core environment and incorporates advanced architectural features including a 5-stage pipeline (Fetch, Decode, Execute, Memory, Write-back) to closely mimic real-world processor behavior. It includes support for scratchpad memory and implements a cache subsystem with both LRU (Least Recently Used) and SRRIP (Static Re-reference Interval Prediction) replacement policies. The simulator provides detailed insights into how instructions are fetched, decoded, and executed, as well as how registers and different levels of memory are managed during program execution.

---

## Features:<br>

1.Instruction Support: Supports a wide range of instructions such as add, addi, lw, sw, beq, bne, and more.<br>
2.Register and Memory Management: Simulates a register file, scratchpad memory, and main memory operations with realistic access patterns.<br>
3.Cache Architecture: Implements a cache subsystem featuring both LRU (Least Recently Used) and SRRIP (Static Re-reference Interval Prediction) replacement policies to simulate efficient memory access.<br>
4.Pipelined Execution: Models a 5-stage pipeline (Fetch, Decode, Execute, Memory, Write-back), demonstrating instruction-level parallelism and hazards.<br>
5.Detailed Output: Provides step-by-step execution details, including pipeline state, register contents, cache hits/misses, and memory states.<br>


## Important Points:<br>

Internal structure:<br>
- Each core contains 32 registers
- total size of memory = 1024*4 bytes
- total size of scratchpad memory = 400 bytes (can be modified) 
- In current version all cores have shared Instruction Fetch unit and shared Memory
- two levels of cache with seperate first level cache for instructions and data
- lw_spm loads a word from the scratchpad memory address computed as rs1 + offset into register rd.
- sw_spm stores the value from register rs2 into the scratchpad memory at the address rs1 + offset.

### Output is divided into 5 parts:
- Part1: First graph simulation shows register values of all cores <br>
- Part2: prints the console<br>
- Part3: prints Memory contents <br>
- Part4: Prints stalls in each core and total stalls <br>
- Part5: IPC for each core and total clock cycles <br>
- Part6: Prints Miss rates of all caches <br>

---

## Meeting Minutes:<br>

Doc link: [Meeting Minutes](https://github.com/nithishgouds/Simulator-COA/blob/main/Meeting%20Minutes.md)


---

## Getting Started
1. Clone the repository.
2. Navigate to the project directory.
3. Modify cache_config.csv to desired values
4. Run the simulator using
   ```bash
   python main.py {filename.asm}
5. Enter "y" to enable Data Forwarding.
6. Enter "0" to continue with LRU cache replacement policy or "1" to continue with SRRIP cache replacement policy 
7. Enter the Latencies of desired opcodes and enter "done" when done entering latencies.


