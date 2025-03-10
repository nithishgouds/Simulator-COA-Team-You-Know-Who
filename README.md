# Simulator-COA ( TEAM NAME - You Know Who )




## Project Overview:<br>

This project is an Instruction Set Simulator built in Python to simulate the execution of various instructions such as add, addi, sub, and more. The simulator models a multi-core environment, demonstrating how instructions are fetched, decoded, executed, and how registers and memory are managed during program execution.

---

## Features:<br>

1.Instruction Support: Supports a range of instructions such as add, addi, lw, sw, beq, bne, etc.<br>
2.Register and Memory Management: Simulates a register file and memory operations.<br>
3.Detailed Output: Provides step-by-step execution details, including register and memory states.<br>


## Important Points:<br>


Internal structure:<br>
- Each core contains 32 registers
- total size of memory = 1024*4 bytes 
- In current version all cores have shared Instruction Fetch unit and shared Memory
### Output is divided into 5 parts:
- Part1: First graph simulation shows register values of all cores <br>
- Part2: Second graph simulation shows Memory <br>
- Part3: prints the console<br>
- Part4: Prints stalls in each core and total stalls <br>
- Part5: IPC for each core and total clock cycles <br>

---

## Meeting Minutes:<br>

Doc link: [Meeting Minutes](https://github.com/nithishgouds/Simulator-COA/blob/main/Meeting%20Minutes.md)


---

## Getting Started
1. Clone the repository.
2. Navigate to the project directory.
3. Run the simulator using
   ```bash
   python main.py {filename.asm}
4. Enter "y" to enable Data Forwarding.
5. Enter the Latencies of desired opcodes and enter "done" when done entering latencies.
6. Question given in Doc is done in array_sum.asm to run it 
   ```bash
   python main.py array_sum.asm

