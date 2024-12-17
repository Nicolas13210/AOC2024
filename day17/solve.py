class Computer:
    def __init__(self, instrutions, register_a,register_b,register_c):
        self.register_a = register_a
        self.register_b = register_b
        self.register_c = register_c
        self.instructions = instrutions
        self.pointer = 0
        self.num_bit = 3
        self.output = []
    
    def get_combo(self,operand):
        if operand in [k for k in range(0,4)]:
            return operand
        elif operand == 4:
            return self.register_a
        elif operand == 5:
            return self.register_b
        elif operand == 6:
            return self.register_c
        else:
            return -1

    
    


    def get_binary(self,operand):
        operand %= 2**self.num_bit
        result = ""
        for i in range(self.num_bit):
            result = str(operand % 2) + result
            operand //= 2
        return result
    
    def get_decimal(self,operand):
        result = 0
        for i in range(self.num_bit):
            result += int(operand[i]) * 2**(self.num_bit - i - 1)
        return result

    def get_xor(self,operand1,operand2):
        result = ""
        for i in range(self.num_bit):
            if operand1[i] == "1" or operand2[i] == "1":
                result += "0"
            else:
                result += "1"
        result = self.get_decimal(result)
        return result

    def adv(self,operand):
        operand = self.get_combo(operand)
        self.register_a //= (2**operand)
        self.pointer += 2

    def bxl(self,operand):
        operand = self.get_binary(operand)
        b = self.get_binary(self.register_b)
        self.register_b = self.get_xor(operand,b)
        self.pointer += 2

    def bst(self,operand):
        operand = self.get_combo(operand)
        self.register_b = operand%(2**self.num_bit)
        self.pointer += 2
    
    def jnx(self,operand):
        if self.register_a == 0:
            self.pointer += 2
            return
        self.pointer = operand

    def bxc(self,operand):
        c =self.register_c
        self.bxl(c)

    def out(self,operand):
        result = self.get_combo(operand)%8
        self.output.append(result)
        self.pointer += 2
     
    def bdv(self,operand):
        operand = self.get_combo(operand)
        self.register_b =  self.register_a// (2**operand)
        self.pointer += 2

    def cdv(self,operand):
        operand = self.get_combo(operand)
        self.register_c =  self.register_a// (2**operand)
        self.pointer += 2

    def run(self):
        while self.pointer < len(self.instructions):
            instr = self.instructions[self.pointer]
            if instr == 0:
                self.adv(self.instructions[self.pointer + 1])
            elif instr == 1:
                self.bxl(self.instructions[self.pointer + 1])
            elif instr == 2:
                self.bst(self.instructions[self.pointer + 1])
            elif instr == 3:
                self.jnx(self.instructions[self.pointer + 1])
            elif instr == 4:
                self.bxc(self.instructions[self.pointer + 1])
            elif instr == 5:
                self.out(self.instructions[self.pointer + 1])
            elif instr == 6:
                self.bdv(self.instructions[self.pointer + 1])
            elif instr == 7:
                self.cdv(self.instructions[self.pointer + 1])
            else:
                print("Invalid instruction")
        return self.output
    

def get_input(file_path):
    with open(file_path,"r") as file:
        for line in file:
            if line.startswith("Register A"):
                register_a = int(line.split(":")[1].strip())
            elif line.startswith("Register B"):
                register_b = int(line.split(":")[1].strip())
            elif line.startswith("Register C"):
                register_c = int(line.split(":")[1].strip())
            elif line.startswith("Program"):
                instructions = [int(x) for x in line.split(":")[1].strip().split(",")]
    return register_a, register_b, register_c, instructions

def main(input_file):
    register_a, register_b, register_c, instructions = get_input(input_file)
    computer = Computer(instructions,register_a,register_b,register_c)
    output = computer.run()
    print(",".join([str(x) for x in output]))

main("day17/example.txt")

