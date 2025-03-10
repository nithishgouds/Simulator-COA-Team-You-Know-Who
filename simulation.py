import core
import utils
import sys

class Simulator:

    pc_changed = [False] * 4
    new_pc = [0] * 4
    clock = 0
    fetch_ins = [True] * 4

    def __init__(self):
        self.memory = [0] * (1024) 
        self.cores = [core.Cores(i) for i in range(4)]
        self.program = []
        self.labels_map = {}
        self.ins_queue=[]
        self.data_forwarding_enable=input("enable data forwarding y/n :")
        self.latency_map={
            "add":1,
            "sub": 1,
            "mul": 1,
            "slt":1,
            "sll":1,
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
            "bge": 1,
            "blt":1
        }


    def instruction_fetch(self):

        ins_fetch_available = [False,False,False,False]


        if self.cores[0].pc == self.cores[1].pc == self.cores[2].pc == self.cores[3].pc:
            ins_fetch_available = [True,True,True,True]
            self.ins_queue=[]
        else:
            
            # if not self.ins_queue:
            #     self.ins_queue.extend(range(4))
            # access_for_core = self.ins_queue.pop(0)
            # ins_fetch_available[access_for_core] = True
            if not self.ins_queue:
                for i in range(4):
                    if (self.cores[i].pc // 4) >= len(self.program):
                        continue
                    self.ins_queue.append(i)
            #print(self.ins_queue)
            access_for_core = self.ins_queue.pop(0)
            ins_fetch_available[access_for_core] = True


        
        for i in range(4):
            core1pc=self.cores[i].pc

            self.cores[i].write_back_executed_curr_cycle=False
            #print("if entered",self.fetch_ins,i)
            #print("fetch_ins",i,self.fetch_ins)
            if self.fetch_ins[i] == False:
                continue
            if self.fetch_ins[i] == True and not self.pc_changed[i] and ins_fetch_available[i]:
                self.fetch_ins[i]= False


            #print(self.pc_changed)
            if self.pc_changed[i]:
                self.cores[i].pc=self.new_pc[i]
                #print(i,self.cores[i].pc)
                self.pc_changed[i] = False
                self.cores[i].ID_register=""
                #print("i bef dest:",i)
                #print("exr bef dest:",self.cores[i].EX_register)
                if self.cores[i].EX_register :
                    dest_reg=self.cores[i].EX_register[1]
                    opcode=self.cores[i].EX_register[0]
                    if opcode in ["add","sub","mul","slt","sll","addi","jalr","slli","la","jal","lw"]:
                        dest_reg_id=int(dest_reg[1:])
                        self.cores[i].reg_status_active[dest_reg_id] -= 1
                self.cores[i].EX_register=[]
                self.fetch_ins[i] = True
                self.cores[i].execute_ID = True
                continue
                # self.cores[i].execute_EX = True
                # self.cores[i].execute_ME = True
            #print(i,ins_fetch_available[i])
            if ins_fetch_available[i]:#self.pc_changed:
                #print("entering fetch",i)
                if core1pc//4 >= len(self.program):
                    #print("exceeded pc",i)
                    continue
                self.cores[i].ID_register=self.program[core1pc//4]
                #print("writing to id of core",i,self.program[core1pc//4])
                self.cores[i].pc+=4
            #print("---")

            if core1pc//4 >= len(self.program):
                continue
            
        return

    def get_latency(self):
        print("Enter opcode and latency in the format: opcode latency (e.g., add 2)")
        print("Type 'done' when finished.")
        print("Available opcodes:", ", ".join(self.latency_map.keys()))

        while True:
            user_input = input("Enter opcode and latency: ").strip()
            if user_input.lower() == "done":
                break  
            try:
                opcode, latency = user_input.split()
                latency = int(latency)
                if opcode in self.latency_map:
                    if latency > 0:
                        self.latency_map[opcode] = latency  # Update if valid
                    else:
                        print("Latency must be positive.")
                else:
                    print(f"Invalid opcode '{opcode}'. Please enter a valid opcode.")

            except ValueError:
                print("Invalid format. Please enter in 'opcode latency' format.")
            except IndexError:
                print("Please enter both opcode and latency.")



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
        if len(data_array) >= 1024:
            print("error : memory overflow")
        for i in range(len(data_array)):
            self.memory[i]=data_array[i]

        df_enable=False
        if self.data_forwarding_enable =="y":
            df_enable = True

        
        self.get_latency()

        for i in range(4):
            self.cores[i].pgm=self.program
            self.cores[i].labels_map=self.labels_map
            self.cores[i].mem=self.memory
            self.cores[i].Data_Forwarding=df_enable
            self.cores[i].latency_map=self.latency_map


        pipeline_active=True

        print(" - - console - - ")



        while pipeline_active:
        #for k in range(20):
            for i in range(4):
                self.cores[i].execute_pipeline()
            self.instruction_fetch()
         

            fetch_possible = not all(core.pc // 4 >= len(self.program) for core in self.cores)

            if (not fetch_possible and all(not core.ID_register and not core.EX_register and not core.ME_register and not core.WB_register for core in self.cores)):
                pipeline_active = False

            
            if not pipeline_active:
                print(" - - - - - - - - ")
            # if not fetch_possible and not self.cores[0].ID_register and not self.cores[0].EX_register and not self.cores[0].ME_register and not self.cores[0].WB_register :
            #     pipeline_active = False
            self.clock += 1
