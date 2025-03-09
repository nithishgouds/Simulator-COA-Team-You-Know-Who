import re
import sys
import simulation


class Cores:

    pgm = []
    labels_map = {}
    mem = []

    def __init__(self, cid):
        self.registers = [0] * 32
        self.reg_status_active = [0] * 32
        self.pc = 0
        self.coreid = cid

     
        #self.IF_register=""
        self.ID_register=""
        self.EX_register=[]
        self.ME_register=[]
        self.WB_register=[]

        self.execute_ID=True
        self.execute_EX=True
        self.execute_ME=True

        self.execution_time_rem_ex=0
        self.execution_time_rem_me=0
        self.latency_map={}

        self.stall_count=0
        self.ins_executed_count=0

        self.Data_Forwarding = False
        

    def set_register(self, index, value):
        if index != 0:  # Prevent modifying register 0
            self.registers[index] = value

    def get_register(self, index) -> any:
        if index.startswith("x"):
            reg_id=int(index[1:])
            # if self.reg_status_active[reg_id] == True:
            #     simulation.Simulator.fetch_ins = False
            #     return False
            reg_val=self.registers[reg_id]
            return reg_val
        elif index == "cid":
            cid_val=self.coreid
            return cid_val
        else:
            print("register error")
            exit()

    def validate(self, instruction):
        patterns = {
            "add": r"^add\s+x\d{1,2},?\s+x\d{1,2},?\s+x\d{1,2}$",
            "addi": r"^addi\s+x\d{1,2},?\s+x\d{1,2},?\s+-?\d+$",
            "mul": r"^mul\s+x\d{1,2},?\s+x\d{1,2},?\s+x\d{1,2}$",
            "sub": r"^sub\s+x\d{1,2},?\s+x\d{1,2},?\s+x\d{1,2}$",
            "lw": r"^lw\s+x\d{1,2},?\s+(\d+\(x\d{1,2}\)|\w+)$",
            "sw": r"^sw\s+x\d{1,2},?\s+\d+\(x\d{1,2}\)$",
            "bne": r"^bne\s+x\d{1,2},?\s+x\d{1,2},?\s+\w+$",
            "blt": r"^blt\s+x\d{1,2},?\s+x\d{1,2},?\s+\w+$",
            "bge": r"^bge\s+x\d{1,2},?\s+x\d{1,2},?\s+\w+$",
            "beq": r"^beq\s+x\d{1,2},?\s+x\d{1,2},?\s+\w+$",
            "jal": r"^jal\s+(x\d{1,2},?\s+)?\w+$",
            "j": r"^j\s+\w+$",
            "jalr": r"^jalr\s+x\d{1,2},?\s+x\d{1,2},?\s+-?\d+$",
            "sll": r"^sll\s+x\d{1,2},?\s+x\d{1,2},?\s+x\d{1,2}$",
            "slli": r"^slli\s+x\d{1,2},?\s+x\d{1,2},?\s+\d+$",
            "la": r"^la\s+x\d{1,2},?\s+\w+$",
            "slt": r"^slt\s+x\d{1,2},?\s+x\d{1,2},?\s+x\d{1,2}$"
        }
        
        # Iterate over pattern values only
        for regex in patterns.values():
            if re.match(regex, instruction):
                return True
        return False


    # def instruction_fetch(self):
    #     self.ID_register=self.IF_register
    #     self.pc += 4
    #     return

    #def reg_active_status_check(self,reg)

    def data_from_EXr(self,dest_id) -> any:
        #print("checking in ex",dest_id)
        parts=self.ME_register
        #print(parts)
        if not parts:
            return "False"
        if dest_id == int(parts[1][1:]) and parts[0] not in ["lw","la"]:
            data=parts[2]
            return data
        elif dest_id == int(parts[1][1:]) and parts[0] in ["lw","la"]:
            #print("inside exr but lw")
            return "stall"
        else:
            return "False"

    def data_from_MEr(self,dest_id) -> any:
        #print("checking in me",dest_id)
        parts=self.WB_register
        if not parts:
            return "False"        
        if dest_id == int(parts[1][1:]):
            data=parts[2]
            return data
        else:
            return "False" 
        
    def do_data_forwarding(self,dest_id) -> any:
        if self.Data_Forwarding == False:
            return "False"
        in_exr = self.data_from_EXr(dest_id)
        if in_exr == "stall":
            return "False"
        elif in_exr == "False":
            in_mer = self.data_from_MEr(dest_id)
            if in_mer == "False":
                return "False"
            else:
                return in_mer
        else:
            return in_exr    


    def instruction_decode(self):


        ins=self.ID_register

        if not ins: 
            return
        
        validate=self.validate(ins)
        if not validate:
            print(f"Error : Invalid Instruction {ins}")
            exit()
        #print("entered id",self.execute_ID)
        if self.execute_ID == False:
            return
        
        #print("id decoding",self.pc,self.ID_register)
        ins=ins.replace(",", " ")
        parts = re.findall(r'-?\w+', ins)
        opcode=parts[0]
        decoded_fetched=[]
        decoded_fetched.append(opcode)

        if opcode in ["add","sub","mul","slt","sll"]:#opcode rd rs1 rs2
            decoded_fetched.append(parts[1]) #rd
            dest_id = int(parts[1][1:])
            sr1_id = parts[2]
            sr2_id = parts[3]
            stall=False
            sr1_data = None
            sr2_data = None
            rs1_active_status = False
            rs2_active_status = False
            if sr1_id != "cid":
                rs1_active_status = self.reg_status_active[int(parts[2][1:])] > 0
            if sr2_id != "cid":
                rs2_active_status = self.reg_status_active[int(parts[3][1:])] > 0

            if  rs1_active_status or rs2_active_status :
                if rs1_active_status:
                    sr1_from_forwarding = self.do_data_forwarding(int(parts[2][1:]))
                    if sr1_from_forwarding == "False":
                        stall = True
                    else:
                        sr1_data = sr1_from_forwarding
                if rs2_active_status:
                    sr2_from_forwarding = self.do_data_forwarding(int(parts[3][1:]))
                    if sr2_from_forwarding == "False":
                        stall = True
                    else:
                        sr2_data = sr2_from_forwarding                    
            if stall:
                self.stall_count+=1
                return        

            if sr1_data is not None:
                decoded_fetched.append(sr1_data)
            else:
                decoded_fetched.append(self.get_register(parts[2]))

            if sr2_data is not None:
                decoded_fetched.append(sr2_data)
            else:
                decoded_fetched.append(self.get_register(parts[3]))
            
            self.reg_status_active[dest_id] += 1

            # decoded_fetched.append(self.get_register(parts[2])) #rs1 value
            # decoded_fetched.append(self.get_register(parts[3])) #rs2 value
            
        if opcode in ["addi","jalr","slli"]:#opcode rd rs1 offset
            decoded_fetched.append(parts[1]) #rd

            dest_id = int(parts[1][1:])
            sr1_id = parts[2]
            stall=False
            sr1_data = None
            rs1_active_status = False
            if sr1_id != "cid":
                rs1_active_status = self.reg_status_active[int(parts[2][1:])] > 0 
                          
            if rs1_active_status:
                sr1_from_forwarding = self.do_data_forwarding(int(parts[2][1:]))
                if sr1_from_forwarding == "False":
                    stall = True
                else:
                    sr1_data = sr1_from_forwarding

            if stall:
                self.stall_count+=1
                return 
            #print(sr1_data)
            if sr1_data is not None:
                decoded_fetched.append(sr1_data)
            else:
                decoded_fetched.append(self.get_register(parts[2]))
            # if self.reg_status_active[dest_id] == False:
            #     self.reg_status_active[dest_id] = True
            self.reg_status_active[dest_id] += 1
            #decoded_fetched.append(self.get_register(parts[2]))#rs1 value
            decoded_fetched.append(parts[3])#imm/offset
            #print(decoded_fetched)

        if opcode in ["lw"]:#opcode rd offset rs
            if len(parts) == 4:
                decoded_fetched.append(parts[1]) #rd
                decoded_fetched.append(parts[2]) #offset
                #print(parts)
                dest_id = int(parts[1][1:])
                sr1_id = int(parts[3][1:])
                stall=False
                sr1_data = None
                if self.reg_status_active[sr1_id] > 0 :
                    sr1_from_forwarding = self.do_data_forwarding(sr1_id)
                    if sr1_from_forwarding == "False":
                        stall = True
                    else:
                        sr1_data = sr1_from_forwarding
                    return
                if stall:
                    self.stall_count+=1
                    return 
                #print(sr1_data)
                if sr1_data is not None:
                    decoded_fetched.append(sr1_data)
                else:
                    decoded_fetched.append(self.get_register(parts[3]))
                # if self.reg_status_active[dest_id] == False:
                #     self.reg_status_active[dest_id] = True
                self.reg_status_active[dest_id] += 1
                #decoded_fetched.append(self.get_register(parts[3])) #rs
            else:#lw x1 base
                decoded_fetched.append(parts[1]) #rd
                decoded_fetched.append(parts[2]) #label
                dest_id = int(parts[1][1:])
                self.reg_status_active[dest_id] += 1

        if opcode in ["sw"]:#opcode rs1 offset rs2 

            sr1_id = parts[1]
            sr2_id = int(parts[3][1:])
            stall=False
            sr1_data = None
            sr2_data = None
            rs1_active_status = False
            if sr1_id != "cid":
                rs1_active_status = self.reg_status_active[int(parts[1][1:])] > 0 
            if rs1_active_status or self.reg_status_active[sr2_id] > 0:
                if rs1_active_status:
                    sr1_from_forwarding = self.do_data_forwarding(int(parts[1][1:]))
                    if sr1_from_forwarding == "False":
                        stall = True
                    else:
                        sr1_data = sr1_from_forwarding
                if self.reg_status_active[sr2_id] > 0:
                    sr2_from_forwarding = self.do_data_forwarding(sr2_id)
                    if sr2_from_forwarding == "False":
                        stall = True
                    else:
                        sr2_data = sr2_from_forwarding                    
            if stall:
                self.stall_count+=1
                return 
            if sr1_data is not None:
                decoded_fetched.append(sr1_data)
            else:
                decoded_fetched.append(self.get_register(parts[1]))            
            #decoded_fetched.append(self.get_register(parts[1])) #rs1
            decoded_fetched.append(parts[2]) #offset
            if sr2_data is not None:
                decoded_fetched.append(sr2_data)
            else:
                decoded_fetched.append(self.get_register(parts[3]))
            #decoded_fetched.append(self.get_register(parts[3])) #rs2

        if opcode in ["bne","blt","bge","beq"]:#opcode rs1 rs2 label

            sr1_id = parts[1]
            sr2_id = parts[2]
            stall=False
            sr1_data = None
            sr2_data = None
            rs1_active_status = False
            rs2_active_status = False
            if sr1_id != "cid":
                rs1_active_status = self.reg_status_active[int(parts[1][1:])] > 0
            if sr2_id != "cid":
                rs2_active_status = self.reg_status_active[int(parts[2][1:])] > 0
            if rs1_active_status or rs2_active_status:
                if rs1_active_status:
                    sr1_from_forwarding = self.do_data_forwarding(int(parts[1][1:]))
                    if sr1_from_forwarding == "False":
                        stall = True
                    else:
                        sr1_data = sr1_from_forwarding
                if rs2_active_status:
                    sr2_from_forwarding = self.do_data_forwarding(int(parts[2][1:]))
                    if sr2_from_forwarding == "False":
                        stall = True
                    else:
                        sr2_data = sr2_from_forwarding                    
            if stall:
                self.stall_count+=1
                return 
            if sr1_data is not None:
                decoded_fetched.append(sr1_data)
            else:
                decoded_fetched.append(self.get_register(parts[1])) 
            if sr2_data is not None:
                decoded_fetched.append(sr2_data)
            else:
                decoded_fetched.append(self.get_register(parts[2])) 
            #decoded_fetched.append(self.get_register(parts[1])) #rs1 val
            #decoded_fetched.append(self.get_register(parts[2])) #rs2 val
            decoded_fetched.append(parts[3]) #label

        if opcode in ["la","jal"]:#opcode rd/x1 label
            decoded_fetched.append(parts[1]) #rd/x1

            dest_id = int(parts[1][1:])
            # sr1_id = int(parts[2][1:])
            # if self.reg_status_active[sr1_id] > 0 :
            #     return
            # if self.reg_status_active[dest_id] == False:
            #     self.reg_status_active[dest_id] = True
            self.reg_status_active[dest_id] += 1
            decoded_fetched.append(parts[2]) #label

        if opcode in ["j"]:#opcode label
            decoded_fetched.append(parts[1]) #label
        
        simulation.Simulator.fetch_ins[self.coreid]=True
        self.execute_ID = False

        if decoded_fetched[0] in ["lw","sw","la"]:
            self.execution_time_rem_ex=0
        elif decoded_fetched[0] in self.latency_map:
            self.execution_time_rem_ex=self.latency_map[decoded_fetched[0]]-1
        else:
            self.execution_time_rem_ex=0
        self.ID_register=""
        self.EX_register=decoded_fetched       
        return
    
    def execute(self):
        parts=self.EX_register


        if not parts:
            return
        if self.execute_EX == False:
            return
               
        if self.execution_time_rem_ex >0:
            #self.stall_count+=1
            self.execution_time_rem_ex -=1
            return
        
        opcode=parts[0]
        #print("ex",parts)
        executed=[]
        executed.append(opcode)
        if opcode in ["add","sub","mul","slt","sll"]:#opcode rd rs1 rs2
            executed.append(parts[1])
            if opcode == "add":
                arthemetic_op = int(parts[2]) + int(parts[3]) #arthimetic_output
                executed.append(arthemetic_op)
            if opcode == "sub":
                arthemetic_op = int(parts[2]) - int(parts[3])
                executed.append(arthemetic_op)
            if opcode == "mul":
                arthemetic_op = int(parts[2]) * int(parts[3])
                executed.append(arthemetic_op)
            if opcode == "slt":
                arthemetic_op=0
                if int(parts[2]) < int(parts[3]):
                    arthemetic_op=1
                executed.append(arthemetic_op)
            if opcode == "sll":
                arthemetic_op = int(parts[2]) << int(parts[3])
                executed.append(arthemetic_op)

        if opcode in ["addi","jalr","slli"]:#opcode rd rs1 offset/imm
            if opcode == "addi":
                executed.append(parts[1])
                arthemetic_op = int(parts[2]) + int(parts[3])
                executed.append(arthemetic_op)
            if opcode == "slli":
                executed.append(parts[1])
                arthemetic_op = int(parts[2]) << int(parts[3])
                executed.append(arthemetic_op)
            if opcode == "jalr":
                executed.append(parts[1])
                offset=int(parts[3]) 
                if offset%4 != 0:
                    print("offset should only be in multiples of 4")
                    exit()
                new_pc = int(parts[2])+int(parts[3])
                #self.pc=new_pc
                simulation.Simulator.new_pc[self.coreid] = new_pc
                simulation.Simulator.pc_changed[self.coreid] = True
                arthemetic_op = (self.pc + 4)
                executed.append(arthemetic_op)
        
        if opcode in ["lw","sw"]:#opcode rd/rs offset rs/rd 
            # offset=int(parts[2]) 
            # if offset%4 != 0:
            #     print("offset should only be in multiples of 4")
            #     exit()
            if opcode == "lw": 
                if len(parts) == 4:#lw rd offset rs1
                    offset=int(parts[2]) 
                    if offset%4 != 0:
                        print("offset should only be in multiples of 4")
                        exit()
                    effective_addr=int(parts[2])+int(parts[3])
                    executed.append(parts[1])
                    executed.append(effective_addr)
                else:#opcode rd label
                    label=parts[2]
                    label_value=self.labels_map[label]
                    address=label_value*4
                    executed.append(parts[1])
                    executed.append(address)
            if opcode == "sw":
                offset=int(parts[2]) 
                if offset%4 != 0:
                    print("offset should only be in multiples of 4")
                    exit()
                effective_addr=int(parts[2])+int(parts[3])
                executed.append(parts[1])
                executed.append(effective_addr)

        if opcode in ["bne","blt","bge","beq"]:#opcode rs1 rs2 label
            label = parts[3]
            if opcode == "bne":
                if int(parts[1]) != int(parts[2]):
                    new_pc = self.labels_map[label]
                    #self.pc=new_pc*4
                    simulation.Simulator.new_pc[self.coreid] = new_pc*4
                    simulation.Simulator.pc_changed[self.coreid] = True
            if opcode == "blt":
                if int(parts[1]) < int(parts[2]):
                    new_pc = self.labels_map[label]
                    #self.pc=new_pc*4
                    simulation.Simulator.new_pc[self.coreid] = new_pc*4
                    simulation.Simulator.pc_changed[self.coreid] = True
            if opcode == "beq":
                if int(parts[1]) == int(parts[2]):
                    #print(self.labels_map[label])
                    new_pc = self.labels_map[label]
                    #self.pc=new_pc*4
                    simulation.Simulator.new_pc[self.coreid] = new_pc*4
                    simulation.Simulator.pc_changed[self.coreid] = True
            if opcode == "bge":
                if int(parts[1]) >= int(parts[2]):
                    new_pc = self.labels_map[label]
                    #self.pc=new_pc*4
                    simulation.Simulator.new_pc[self.coreid] = new_pc*4
                    simulation.Simulator.pc_changed[self.coreid] = True

        if opcode in ["la","jal"]:#opcode rd/x1 label
            label = parts[2]
            if opcode == "la":
                executed.append(parts[1])
                label = parts[2]
                label_value = self.labels_map[label]
                destination_addr = label_value*4
                executed.append(destination_addr)
            if opcode == "jal":
                new_pc = self.labels_map[label]
                #self.pc=new_pc*4
                simulation.Simulator.new_pc[self.coreid] = new_pc*4
                simulation.Simulator.pc_changed[self.coreid] = True
                arthemetic_op = (self.pc + 4)
                executed.append(parts[1])
                executed.append(arthemetic_op)
        if opcode in ["j"]:#opcode label
            label=parts[1]
            new_pc = self.labels_map[label]
            #self.pc=new_pc*4
            simulation.Simulator.new_pc[self.coreid] = new_pc*4
            simulation.Simulator.pc_changed[self.coreid] = True 
        #print("before ex:",self.execute_ID)  
        self.execute_ID = True 
        self.execute_EX = False 
        if executed[0] in ["lw","sw","la"] and executed[0] in self.latency_map:
            self.execution_time_rem_me=self.latency_map[executed[0]]-1
        else:
            self.execution_time_rem_me=0        
        #print("after ex:",self.execute_ID)
        self.EX_register = []       
        self.ME_register = executed
        return
    
    def memory_access(self):
        parts=self.ME_register
        #print("entered me",parts)
        if not parts:
            return
        
        if self.execute_ME == False:
            return
        
        if self.execution_time_rem_me >0:
            #self.stall_count+=1
            self.execution_time_rem_me -=1
            return
        #print("me",self.coreid)
        opcode=parts[0]
        #print("me",parts)
        mem_fetched=[]
        mem_fetched.append(opcode)
        if opcode == "lw":#opcode rd addr
            effective_addr=int(parts[2])//4
            #print(effective_addr)
            memory_value=self.mem[effective_addr]
            mem_fetched.append(parts[1])
            mem_fetched.append(memory_value)
            self.WB_register=mem_fetched

        elif opcode == "sw":#opcode value addr
            effective_addr=int(parts[2])//4
            value=int(parts[1])
            self.mem[effective_addr] = value
            self.WB_register=mem_fetched
        
        else :
            self.WB_register=parts
        self.execute_EX = True
        self.execute_ME = False
        self.ME_register=[]
        #print("flushed me",parts)
        return
    
    def write_back(self):
        parts = self.WB_register

        if not parts:
            return
        #print("wb",self.coreid)
        
        opcode=parts[0]
        #print("wb",parts)
        if opcode in ["add","sub","mul","slt","sll"]:#opcode rd value
            value = int(parts[2])
            reg_id = int(parts[1][1:])
            self.set_register(reg_id,value)
            self.reg_status_active[reg_id] -= 1
        elif opcode in ["addi","jalr","slli"]:#opcode rd value/pc+4
            value = int(parts[2])
            reg_id = int(parts[1][1:])
            self.set_register(reg_id,value)
            self.reg_status_active[reg_id] -= 1           
        elif opcode in ["lw","sw"]:#opcode rd value for lw
            if opcode == "lw":
                value = int(parts[2])
                reg_id = int(parts[1][1:])
                self.set_register(reg_id,value)
                self.reg_status_active[reg_id] -= 1
        elif opcode in ["bne","blt","bge","beq"]:#opcode rs1 rs2 label
            pass
        elif opcode in ["la","jal"]:#opcode rd/x1 label
            value = int(parts[2])
            reg_id = int(parts[1][1:])
            self.set_register(reg_id,value)
            self.reg_status_active[reg_id] -= 1
        elif opcode in ["j"]:#opcode label    
            pass  
        else:
            print("error in WB")
            exit()
        self.execute_ME = True
        self.ins_executed_count+=1
        self.WB_register=[]
        return

    def execute_pipeline(self):
        #print(f"- - new cycle {self.coreid} - -")
        self.write_back()
        self.memory_access()
        self.execute()
        self.instruction_decode()

    