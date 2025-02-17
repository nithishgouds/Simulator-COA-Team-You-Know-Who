import re

class Cores:
    def __init__(self, cid):
        self.registers = [0] * 32
        self.pc = 0
        self.coreid = cid

    def set_register(self, index, value):
        if index != 0:  # Prevent modifying register 0
            self.registers[index] = value

    def execute(self, pgm, mem, clock, labels_map):
        print("clock cycle:", clock + 1, " core :", self.coreid, " instruction:", pgm[self.pc])
        parts = re.findall(r'\w+|\d+', pgm[self.pc])
        if len(parts) == 0:
            print("parts is empty")

        opcode = parts[0]
        pc_changed = False

        if opcode == "add":
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            rs2 = int(parts[3][1:])
            destination_value = self.registers[rs1] + self.registers[rs2]
            self.set_register(rd, destination_value)
        elif opcode == "addi":
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            immediate_value = int(parts[3])
            destination_value = self.registers[rs1] + immediate_value
            self.set_register(rd, destination_value)
        elif opcode == "sub":
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            rs2 = int(parts[3][1:])
            destination_value = self.registers[rs1] - self.registers[rs2]
            self.set_register(rd, destination_value)
        elif opcode == "lw":
            rd = int(parts[1][1:])
            rs_offset = int(parts[2])
            rs_address = int(parts[3][1:])
            effective_address = (rs_offset // 4) + self.registers[rs_address]
            effective_address = effective_address - self.coreid * 1024
            memory_value = mem[effective_address]
            destination_value = memory_value
            self.set_register(rd, destination_value)
        elif opcode == "sw":
            rs = int(parts[1][1:])
            offset = int(parts[2])
            base_address = int(parts[3][1:])
            effective_address = (offset // 4) + self.registers[base_address]
            effective_address = effective_address - self.coreid * 1024
            mem[effective_address] = self.registers[rs]
        elif opcode == "bne":
            rs1 = int(parts[1][1:])
            rs2 = int(parts[2][1:])
            label = parts[3]
            if self.registers[rs1] != self.registers[rs2]:
                new_pc = labels_map[label]
                self.pc = new_pc
                pc_changed = True
        elif opcode == "jal":
            if len(parts) == 2:
                rd = 1
                label = parts[1]
            else:
                rd = int(parts[1][1:])
                label = parts[2]
            self.registers[rd] = self.pc + 4
            new_pc = labels_map[label]
            self.pc = new_pc
            pc_changed = True
        elif opcode == "j":
            label = parts[1]
            new_pc = labels_map[label]
            self.pc = new_pc
            pc_changed = True
        elif opcode == "jalr":
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            offset = int(parts[3])
            self.registers[rd] = self.pc + 4
            new_pc = (self.registers[rs1] + offset) & ~1
            self.pc = new_pc
            pc_changed = True
        elif opcode == "sll":
            rd = int(parts[1][1:])
            rs1 = int(parts[2][1:])
            rs2 = int(parts[3][1:])

            shift_amount = self.registers[rs2] & 0x1F # Mask the shift amount to 5 bits (0-31)
            value_to_shift = self.registers[rs1]

            destination_value = value_to_shift<<shift_amount

            self.set_register(rd,destination_value)
            pass

        if not pc_changed:
            self.pc += 1
