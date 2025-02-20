# Simulator-COA




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
- 4096*4 bytes of memory
- In current version all cores are independent and each core can only access 1024*4 bytes of memory which is specific to each core
### Output is divided into 4 parts:
- Part1: Clock cycle and core and insruction which is executed<br>
- Part2: All register values of all cores<br>
- Part3: Total clock cycles took to run the code<br>
- Part4: Prints all memory values in form {index of memory}={value stored}<br>

---

## Meeting Minutes:<br>

Doc link: [Meeting Minutes](https://github.com/nithishgouds/Simulator-COA/blob/main/Meeting%20Minutes.md)


---

## Getting Started
1. Clone the repository.
2. Navigate to the project directory.
3. Run the simulator using python main.py.
