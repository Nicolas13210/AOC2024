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
        
    
    def __str__(self) -> str:
        return (f"Register A: {self.register_a}\nRegister B: {self.register_b}\nRegister C: {self.register_c}\nOutput: {self.output}")

    
    


    def get_binary(self,operand):
        result = ""
        while operand > 0:
            result = str(operand%2) + result
            operand = operand//2
        if result == "":
            result = "0"
        return result
    
    def get_decimal(self,operand):
        result = 0
        for i in range(len(operand)):
            result += int(operand[i]) * 2**(len(operand) - i - 1)
        return result

    def get_xor(self,operand1,operand2):
        result = ""
        length = len(operand1)
        length2 = len(operand2)
        max_length = max(length,length2)
        if length < max_length:
            operand1 = "0"*(max_length - length) + operand1
        if length2 < max_length:
            operand2 = "0"*(max_length - length2) + operand2


        for i in range(max_length):
            if operand1[i] !=operand2[i]:
                result += "1"
            else:
                result += "0"
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


if __name__ == "__main__":
    main("day17/input.txt")

