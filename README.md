# Simulator-COA



📜 Project Overview
This project is a RISC-V Instruction Set Simulator built in Python as part of a Computer Organization and Architecture (COA) course. The simulator can execute a set of RISC-V instructions such as add, addi, sub, and more. The project is designed to simulate multiple cores and provides insights into how instructions are fetched, decoded, executed, and how registers and memory are managed in a simulated RISC-V environment.

🛠️ Project Structure
The project consists of the following key modules:

1. main.py
The entry point of the simulator.
Initializes the simulation environment, loads instructions, and starts execution.
Manages input/output operations and user-defined configurations.
2. simulator.py
Handles the instruction fetch-decode-execute cycle.
Simulates the RISC-V instruction set, including arithmetic, logical, and control flow instructions.
Manages registers, memory, and the program counter.
3. cores.py
Simulates multiple cores to model parallel processing.
Each core executes instructions independently, sharing memory and simulating concurrency.
Supports synchronization primitives such as locks and barriers.
🚀 Features
✅ Supports RISC-V instructions: add, addi, sub, and, or, xor, lw, sw, beq, bne, etc.
✅ Multicore Simulation: Simulates parallel execution of instructions across multiple cores.
✅ Register and Memory Management: Simulates a register file and memory operations.
✅ Instruction Pipeline: Models basic pipeline stages (optional or planned).
✅ Detailed Output: Displays step-by-step execution with registers and memory status.
