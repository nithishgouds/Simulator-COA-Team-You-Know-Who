import core
import utils
import sys

class Simulator:

    pc_changed = [False] * 4
    new_pc = [0] * 4
    clock = 0
    fetch_ins = [True] * 4

    def __init__(self):
        self.memory = [0] * (4096) 
        self.cores = [core.Cores(i) for i in range(4)]
        self.program = []
        self.labels_map = {}
        self.latency_map={
            "add":1,
            "sub": 1,
            "mul": 1,
            "addi": 1,
            "jalr": 1,
            "slli": 1,
            "lw": 1,
            "sw": 1,
            "la": 1,
            "jal": 1,
            "j": 1,
            "beq": 1,
            "bne": 1,
            "bge": 1
        }


    def instruction_fetch(self):
        # if self.fetch_ins == False:
        #     return
        # core1pc=self.cores[0].pc
        # for i in range(1):
        #     if core1pc//4 >= len(self.program):
        #         return
        #     print("if entered",self.fetch_ins)
        #     if self.fetch_ins[i] == False:
        #         continue
        #     if self.fetch_ins[i] == True:
        #         self.fetch_ins[i]= False
        #     self.cores[i].ID_register=self.program[core1pc//4]
        #     print("writing to id",self.program[core1pc//4])
        #     #print(self.pc_changed)
        #     if self.pc_changed[i]:
        #         self.cores[i].pc=self.new_pc[i]
        #         self.pc_changed[i] = False
        #         self.cores[i].ID_register=""
        #         dest_reg=self.cores[i].EX_register[1]
        #         opcode=self.cores[i].EX_register[0]
        #         if opcode in ["add","sub","mul","slt","sll","addi","jalr","slli","la","jal","lw"]:
        #             dest_reg_id=int(dest_reg[1:])
        #             self.cores[i].reg_status_active[dest_reg_id] -= 1
        #         self.cores[i].EX_register=[]
        #         self.fetch_ins[i] = True
        #     else:#self.pc_changed:
        #         self.cores[i].pc+=4
        
        for i in range(4):
            core1pc=self.cores[i].pc
            #print("if entered",self.fetch_ins,i)
            if self.fetch_ins[i] == False:
                continue
            if self.fetch_ins[i] == True:
                self.fetch_ins[i]= False

            #print(self.pc_changed)
            if self.pc_changed[i]:
                self.cores[i].pc=self.new_pc[i]
                self.pc_changed[i] = False
                self.cores[i].ID_register=""
                #print("i bef dest:",i)
                #print("exr bef dest:",self.cores[i].EX_register)
                dest_reg=self.cores[i].EX_register[1]
                opcode=self.cores[i].EX_register[0]
                if opcode in ["add","sub","mul","slt","sll","addi","jalr","slli","la","jal","lw"]:
                    dest_reg_id=int(dest_reg[1:])
                    self.cores[i].reg_status_active[dest_reg_id] -= 1
                self.cores[i].EX_register=[]
                self.fetch_ins[i] = True
                self.cores[i].execute_ID = True
                # self.cores[i].execute_EX = True
                # self.cores[i].execute_ME = True
            else:#self.pc_changed:
                if core1pc//4 >= len(self.program):
                    continue
                self.cores[i].ID_register=self.program[core1pc//4]
                #print("writing to id",self.program[core1pc//4])
                self.cores[i].pc+=4
            #print("---")
            if core1pc//4 >= len(self.program):
                continue
            
        return

    def run(self):
        filename=""
        if len(sys.argv) > 1:
            filename=sys.argv[1]  # Print the first argument
        else:
            print("Error: No filename provided")
        instructions,labels_map,data_array = utils.read_file(filename)
        #print(labels_map)
        self.program=instructions
        self.labels_map=labels_map
        if len(data_array) >= 4096:
            print("error : memory overflow")
        for i in range(len(data_array)):
            self.memory[i]=data_array[i]

        for i in range(4):
            self.cores[i].pgm=self.program
            self.cores[i].labels_map=self.labels_map
        #self.cores[1].labels_map=self.labels_map
        #self.cores[2].labels_map=self.labels_map
        #self.cores[3].labels_map=self.labels_map
            self.cores[i].mem=self.memory
            self.cores[i].latency_map=self.latency_map


        pipeline_active=True

        while pipeline_active:
        #for k in range(25):
            for i in range(4):
                self.cores[i].execute_pipeline()
            self.instruction_fetch()
            
            fetch_possible = True
            if (self.cores[0].pc)//4 >= len(self.program):
                fetch_possible = False
 
            if not fetch_possible and not self.cores[0].ID_register and not self.cores[0].EX_register and not self.cores[0].ME_register and not self.cores[0].WB_register :
                pipeline_active = False
            self.clock += 1
