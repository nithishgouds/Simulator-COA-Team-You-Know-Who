import re
import sys


class Cores:
    def __init__(self, cid):
        self.registers = [0] * 32
        self.pc = 0
        self.coreid = cid
        self.debug=False
        self.invalid_instruction_flag = False

    def set_register(self, index, value):
        if index != 0:  # Prevent modifying register 0
            self.registers[index] = value

    def validate(self, instruction):
        patterns = {
            "add": r"^add x\d{1,2} x\d{1,2} x\d{1,2}$",
            "addi": r"^addi x\d{1,2} x\d{1,2} -?\d+$",
            "mul": r"^mul x\d{1,2} x\d{1,2} x\d{1,2}$",
            "sub": r"^sub x\d{1,2} x\d{1,2} x\d{1,2}$",
            "lw": r"^lw x\d{1,2} \d+\(x\d{1,2}\)$",
            "sw": r"^sw x\d{1,2} \d+\(x\d{1,2}\)$",
            "bne": r"^bne x\d{1,2} x\d{1,2} \w+$",
            "blt": r"^blt x\d{1,2} x\d{1,2} \w+$",
            "bge": r"^bge x\d{1,2} x\d{1,2} \w+$",
            "jal": r"^jal( x\d{1,2})? \w+$",
            "j": r"^j \w+$",
            "jalr": r"^jalr x\d{1,2} x\d{1,2} -?\d+$",
            "sll": r"^sll x\d{1,2} x\d{1,2} x\d{1,2}$",
            "slli": r"^slli x\d{1,2} x\d{1,2} \d+$"
        }

        for opcode, pattern in patterns.items():
            if re.match(pattern, instruction):
                return True
        return False
    def execute(self, pgm, mem, clock, labels_map):
        instruction = pgm[self.pc]
        if not self.invalid_instruction_flag and not self.validate(instruction):
            self.invalid_instruction_flag = True
            print(f"Invalid instruction at PC {self.pc}: '{instruction}'")
            sys.exit() 
            return
        if self.invalid_instruction_flag:
            return
        print("clock cycle:", clock + 1, " core :", self.coreid, " instruction:", pgm[self.pc])
        #parts = re.findall(r'\w+|\d+', pgm[self.pc])
        parts = re.findall(r'-?\w+', pgm[self.pc])

        if len(parts) == 0:
            print("parts is empty")

        opcode = parts[0]
        pc_changed = False

        if opcode == "add":#add x1 x2 x3
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            rs2 = int(parts[3][1:])
            destination_value = self.registers[rs1] + self.registers[rs2]
            self.set_register(rd, destination_value)
        elif opcode == "addi":#addi x1 x2 10
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            immediate_value = int(parts[3])
            destination_value = self.registers[rs1] + immediate_value
            self.set_register(rd, destination_value)
        elif opcode == "mul":#sub x1 x2 x3
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            rs2 = int(parts[3][1:])
            destination_value = self.registers[rs1] * self.registers[rs2]
            self.set_register(rd, destination_value)
        elif opcode == "sub":#sub x1 x2 x3
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            rs2 = int(parts[3][1:])
            destination_value = self.registers[rs1] - self.registers[rs2]
            self.set_register(rd, destination_value)
        elif opcode == "lw":#lw x1 8(x2)
            rd = int(parts[1][1:])
            rs_offset = int(parts[2])
            rs_address = int(parts[3][1:])
            effective_address = (rs_offset  + self.registers[rs_address])//4
            effective_address = effective_address + self.coreid * 1024
            memory_value = mem[effective_address]
            destination_value = memory_value
            self.set_register(rd, destination_value)
        elif opcode == "sw":#sw x1 8(x2)
            rs = int(parts[1][1:])
            offset = int(parts[2])
            base_address = int(parts[3][1:])
            effective_address = (offset + self.registers[base_address])//4
            effective_address = effective_address + self.coreid * 1024
            mem[effective_address] = self.registers[rs]
        elif opcode == "bne":#bne x1 x2 label
            rs1 = int(parts[1][1:])
            rs2 = int(parts[2][1:])
            label = parts[3]
            if self.registers[rs1] != self.registers[rs2]:
                new_pc = labels_map[label]
                self.pc = new_pc
                pc_changed = True
        elif opcode == "blt":#bne x1 x2 label
            rs1 = int(parts[1][1:])
            rs2 = int(parts[2][1:])
            label = parts[3]

            print("v[rs1] = ",self.registers[rs1] ," v[rs2]", self.registers[rs2])
            
            if self.registers[rs1] < self.registers[rs2]:
                new_pc = labels_map[label]
                # if self.debug:
                print("label:",label,"newpc:",new_pc,"prevpc:",self.pc)
                #     exit()
                self.pc = new_pc
                pc_changed = True
            
        elif opcode == "bge":#bge x1 x2 label
            rs1 = int(parts[1][1:])
            rs2 = int(parts[2][1:])
            label = parts[3]
            if self.registers[rs1] >= self.registers[rs2]:
                new_pc = labels_map[label]
                self.pc = new_pc
                pc_changed = True
        elif opcode == "jal":#jal x1 label
            if len(parts) == 2:
                rd = 1
                label = parts[1]
            else:
                rd = int(parts[1][1:])
                label = parts[2]
            self.set_register(rd,(self.pc*4+4)//4)
            new_pc = labels_map[label]
            self.pc = new_pc
            pc_changed = True
        elif opcode == "j":#j label
            label = parts[1]
            new_pc = labels_map[label]
            self.pc = new_pc
            pc_changed = True
        elif opcode == "jalr":#jalr rd rs1 offset
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            offset = int(parts[3])
            self.set_register(rd,(self.pc*4 + 4)//4) 
            if offset%4 != 0:
                print("offset should only be in multiples of 4")
                exit()
            effective_pc = self.registers[rs1]+offset//4
            new_pc = effective_pc
            self.pc = new_pc
            pc_changed = True
        elif opcode == "sll":#sll rd rs1 rs2
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            rs2 = int(parts[3][1:])

            shift_amount = self.registers[rs2] 
            value_to_shift = self.registers[rs1]

            destination_value = value_to_shift<<shift_amount

            self.set_register(rd,destination_value)
        elif opcode == "slli":#sll rd rs1 100
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            rs2 = int(parts[3])

            shift_amount = self.registers[rs2] 
            value_to_shift = self.registers[rs1]

            destination_value = value_to_shift<<shift_amount

            self.set_register(rd,destination_value)
            pass

        if not pc_changed:
            self.pc += 1
