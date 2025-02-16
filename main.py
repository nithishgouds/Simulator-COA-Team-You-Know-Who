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
        #print(pgm[self.pc])
        print("clock cycle:",sim.clock + 1," core :",self.coreid," instruction:",pgm[self.pc])
        parts = re.findall(r'\w+|\d+', pgm[self.pc])
        if len(parts) == 0:
            print("parts is empty")


        opcode = parts[0]
        pc_changed=False

        if opcode == "add": #add x1 x2 x3
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            rs2 = int(parts[3][1:])
            destination_value = self.registers[rs1] + self.registers[rs2]
            self.set_register(rd,destination_value)
        if opcode == "addi": #add x1 x2 x3
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            immediate_value = int(parts[3])
            destination_value = self.registers[rs1] + immediate_value
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
        elif opcode == "bne":#bne x1 x2 label
            rs1 = int(parts[1][1:])
            rs2 = int(parts[2][1:])
            label = parts[3]
            #print("rs1 ",rs1,"rs2 ",rs2,"label :",label)
            if self.registers[rs1] != self.registers[rs2]:
                new_pc=sim.labels_map[label]
                # print(label)
                # print(new_pc)
                self.pc=new_pc
                pc_changed=True    
            pass

        if not pc_changed:
            self.pc += 1



class Simulator:
    def __init__(self,instructions,labels_map):
        self.memory = [0] * (4096)
        self.clock = 0
        self.cores = [Cores(i) for i in range(4)]
        self.program = instructions
        self.labels_map = labels_map

    def run(self):
        while any(core.pc < len(self.program) for core in self.cores):
            for i in range(4):
                if self.cores[i].pc < len(self.program):
                    self.cores[i].execute(self.program, self.memory)
            self.clock += 1



def read_file(filename):
    lines_array = []  # List to store non-empty lines (without labels)
    labels_map = {}   # Dictionary to store label -> line number mapping
    line_number = 0   # Counter for non-empty lines
    line_number_original = 0
    last_label = None  # Keep track of labels that appear alone on a line

    with open(filename, "r") as file:
        for line in file:
            line_number_original += 1
            line = line.strip()  # Remove spaces and newlines
            if not line: 
                # lines_array.append(" ")
                # line_number +=1 
                continue  

            # Check if there's a label in the line (split only at the first colon)
            parts = line.split(":", 1)

            if len(parts) == 2:  # If ':' exists in the line
                label, instruction = parts[0], parts[1].strip()

                if label.endswith(" "):
                    print("invalid initialisation of label at line ",line_number_original)
                    quit()

                if label.isidentifier():  # Ensure valid label name
                    labels_map[label] = line_number  # Map label to instruction's line number

                    if instruction:  # If there's an instruction after the label
                        lines_array.append(instruction)
                        line_number += 1  # Count the instruction line
                    else:
                        if last_label is not None:
                            print("Error no instructions given after label")
                            quit()
                        last_label = label  # Store label for the next line
                    continue

            # If the previous line had a label alone, assign it to this line
            if last_label is not None:
                labels_map[last_label] = line_number
                last_label = None  

            # Store the instruction
            lines_array.append(line)
            line_number += 1 


    return lines_array, labels_map  


instructions, labels_map = read_file("test.asm")


sim = Simulator(instructions,labels_map)
sim.run()
for i in range(4):
    print(sim.cores[i].registers)

print(sim.cores[1].pc)
print("Total clock cycles:" ,sim.clock)