import re

class Cores:
    def __init__(self, cid):
        self.registers = [0] * 32
        self.pc = 0
        self.coreid = cid

    def set_register(self, index, value):
        if index != 0:  # Prevent modifying register 0
            self.registers[index] = value

    def execute(self, pgm, mem):
        #parts = pgm[self.pc].split()
        parts = re.findall(r'\w+|\d+', pgm[self.pc])
        opcode = parts[0]

        if opcode == "add": #add x1 x2 x3
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            rs2 = int(parts[3][1:])
            destination_value = self.registers[rs1] + self.registers[rs2]
            self.set_register(rd,destination_value)
        elif opcode == "sub": #sub x1 x2 x3
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            rs2 = int(parts[3][1:])
            destination_value = self.registers[rs1] - self.registers[rs2]
            self.set_register(rd,destination_value)
        elif opcode == "lw": #lw x1 0(x8)
            rd = int(parts[1][1:])
            rs_offset = int(parts[2])
            rs_address = int(parts[3][1:])
            effective_address=(rs_offset//4)+self.registers[rs_address]
            effective_address=effective_address-self.coreid*1024
            memory_value=sim.memory[effective_address]
            destination_value = memory_value
            self.set_register(rd,destination_value)
            pass
        self.pc += 1

class Simulator:
    def __init__(self):
        self.memory = [0] * (4096)
        self.clock = 0
        self.cores = [Cores(i) for i in range(4)]
        self.program = []

    def run(self):
        while any(core.pc < len(self.program) for core in self.cores):
            for i in range(4):
                if self.cores[i].pc < len(self.program):
                    self.cores[i].execute(self.program, self.memory)
            self.clock += 1


sim = Simulator()
sim.program = ["sub x4 x5 x6", "add x7 x8 x9","lw x1 0(x2)"]

sim.memory[2]=99

for i in range(4):
    sim.cores[i].registers[2] = 2
    sim.cores[i].registers[5] = 3
    sim.cores[i].registers[6] = 4
    sim.cores[i].registers[8] = 5
    sim.cores[i].registers[9] = 6

sim.run()
for i in range(4):
    print(sim.cores[i].registers)

print(sim.cores[1].pc)
print(sim.clock)