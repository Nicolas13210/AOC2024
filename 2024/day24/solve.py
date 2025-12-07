import itertools
import pandas as pd
import graphviz
import random


COLORS = {"AND":"blue","OR":"red","XOR":"green"}
def get_input(input_file):
    with open(input_file, 'r') as file:
        initial,instructions = file.read().strip().split('\n\n')
    initial = {key:int(value) for key,value in [line.split(":") for line in initial.split('\n')]}
    instructions = instructions.split('\n')
    return initial,instructions


def process_instruction(registers,instruction):
    operand_a, operator, operand_b,destination = instruction

    if operand_a in registers and operand_b in registers:
        if operator == "XOR":
            registers[destination] = registers[operand_a] ^ registers[operand_b]
        elif operator == "AND":
            registers[destination] = registers[operand_a] & registers[operand_b]
        elif operator == "OR":
            registers[destination] = registers[operand_a] | registers[operand_b]
        return True
    return False

def process_all(instructions,registers):
    ordered_instruction = []
    
    while(len(instructions) > 0):
        instructions_left = []
        for instruction in instructions:
            answer = process_instruction(registers,instruction)
            if not answer:
                instructions_left.append(instruction)
            else:
                ordered_instruction.append(instruction)
        instructions = instructions_left
    return ordered_instruction

def get_answer(registers):
    register = {key:value for key,value in registers.items() if key.startswith("z")}
    register = sorted(register.items(),reverse=True)
    bin = "".join([str(value[1]) for value in register])
    answer = int(bin,2)
    return answer



def get_number(register, name):
    number = [(key,value) for key,value in register.items() if key.startswith(name)]
    number = sorted(number,reverse=True)
    bin = "".join([str(value) for key,value in number])
    return int(bin,2),bin


def get_wrong(registers):
    wrong_bits = []
    x, x_bin = get_number(registers, "x")
    y, y_bin = get_number(registers, "y")
    z, z_bin = get_number(registers, "z")
    total = x + y
    total_bin = str(bin(total)[2:])  # Convert total to binary
    if len(total_bin) != len(z_bin):
        z_bin = "0" * (len(total_bin)-len(z_bin)) + z_bin
    for i in range(len(total_bin)):
        if total_bin[i] != z_bin[i]:
            wrong_bits.append(len(total_bin)-i)

    print(x)
    print(y)
    print(z)

    wrong_bits = ["z" +str(bit) if len(str(bit)) == 2 else "z0" + str(bit) for bit in wrong_bits]
    print(z_bin)
    print(total_bin)
    return wrong_bits

def get_wrong_instruction(instructions,wrongs):
    for i, instruction in enumerate(instructions):
        if instruction[-2:] in wrongs:
            return i
        
def get_safe_instructions(instructions,first_wrong_instruction):
    last_safe = -1
    for k in range(first_wrong_instruction):
        if instructions[k][-3] == "z":
            last_safe = k
    return last_safe

def get_instructions(instructions):
    instructions = [instruction.split(" ") for instruction in instructions]
    instructions = [(instruction[0],instruction[1],instruction[2],instruction[-1]) for instruction in instructions]
    return instructions









def saved_ordered(instructions):
    df = pd.DataFrame(instructions,columns=["operand_a","operator","operand_b","destination"])
    df.to_csv("day24/ordered_instructions.csv",index=False)




def get_graph(instructions,wrongs):
    dot = graphviz.Digraph()
    for instruction in instructions:
        if instruction[-1] in wrongs:
            dot.node(instruction[-1],color="red")
        else:
            dot.node(instruction[-1])
        dot.node(instruction[0])
        dot.node(instruction[2])
        dot.edge(instruction[0],instruction[-1],color = COLORS[instruction[1]])
        dot.edge(instruction[2],instruction[-1],color = COLORS[instruction[1]])
    dot.render("day24/graphprob.gv",view=True)


def random_add(instructions):
    a = 33671415327010
    b = 21454294971125
    a_bin = bin(a)[2:]
    b_bin = bin(b)[2:]

    a_bin = a_bin[::-1]
    b_bin = b_bin[::-1]
    registers = {}

    for k in range(len(a_bin)):
        key = str(k) if k>=10 else "0" + str(k)
        registers["x"+key] = int(a_bin[k])
    for k in range(len(b_bin)):
        key = str(k) if k>=10 else "0" + str(k)
        registers["y"+key] =int(b_bin[k])
    
    process_all(instructions,registers)
    wrongs = get_wrong(registers)
    print(wrongs)
    return a,b


    

    #process_all(instructions, registers)

    #wrongs = get_wrong(registers)
    

def solve(input_file):
    registers, instructions = get_input(input_file)
    instructions = get_instructions(instructions)
    instructions = [list(instruction) for instruction in instructions]
    a,b = random_add(instructions)
    print("answer")
    print(a,b)
    
    #unsafe = get_rec_unsafe(instructions,wrongs)

    #get_graph(ordered_instructions,wrongs)


solve("day24/input.txt")