import core

class Simulator:
    def __init__(self, instructions, labels_map):
        self.memory = [0] * (4096)
        self.clock = 0
        self.cores = [core.Cores(i) for i in range(4)]
        self.program = instructions
        self.labels_map = labels_map

    def run(self):
        while any(core.pc < len(self.program) for core in self.cores):
            for i in range(4):
                if self.cores[i].pc < len(self.program):
                    self.cores[i].execute(self.program, self.memory, self.clock, self.labels_map)
            self.clock += 1
