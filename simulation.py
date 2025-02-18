import core
import utils

class Simulator:
    def __init__(self):
        self.memory = [0] * (4096)
        self.clock = 0
        self.cores = [core.Cores(i) for i in range(4)]
        self.program = []
        self.labels_map = {}

    def run(self):
        instructions,labels_map,data_array = utils.read_file("bubble2.asm")
        #print(labels_map)
        self.program=instructions
        self.labels_map=labels_map
        for i in range(len(data_array)):
            self.memory[i+1024*0]=data_array[i]
            self.memory[i+1024*1]=data_array[i]
            self.memory[i+1024*2]=data_array[i]
            self.memory[i+1024*3]=data_array[i]

        while any(core.pc < len(self.program) for core in self.cores):
            for i in range(4):
                if self.cores[i].pc < len(self.program):
                    self.cores[i].execute(self.program, self.memory, self.clock, self.labels_map)
                self.clock += 1
