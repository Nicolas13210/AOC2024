from functools import lru_cache 
import networkx as nx


KEYBOARD = tuple([tuple(["7", "8", "9"]),tuple(["4", "5", "6"]), tuple(["1", "2", "3"]),tuple(["#","0","A"])])
DIRECTIONS = tuple([tuple(["#","^","A"]),tuple(["<","v",">"])])

def get_input(input_file):
    with open(input_file) as f:
        return [line.strip() for line in f.read().splitlines()]

def get_graph(pad):
    G = nx.Graph()
    for i, row in enumerate(pad):
        for j, cell in enumerate(row):
            if cell != '#':
                G.add_node(cell)
                for direction in [(0,1),(0,-1),(1,0),(-1,0)]:
                    new_position = (i+direction[0],j+direction[1])
                    
                    if new_position[0]<0 or new_position[0]>=len(pad) or new_position[1]<0 or new_position[1]>=len(pad[0]):
                        continue
                    next_cell = pad[new_position[0]][new_position[1]]
                    if next_cell != '#':
                        G.add_edge(cell, next_cell)
    return G

def get_path(G, start, end,pad):
    paths = nx.all_shortest_paths(G, start, end)
    my_paths = []
    for path in paths:
        temp = convert_instruction(path,pad) + "A"
        my_paths.append(temp)
    return my_paths


def format_code(code):
    answer = ""
    for k in code:
        answer += k
    return answer

def get_table_instructions(pad):
    table = {}
    for i, row in enumerate(pad):
        for j, cell in enumerate(row):
            if cell != '#':
                table[cell] = (i,j)
    return table
    
def get_relative_position(start, end, table):
    keyboard_table = get_table_instructions(table)
    start_position = keyboard_table[start]
    end_position = keyboard_table[end]
    row_diff = end_position[0] - start_position[0]
    col_diff = end_position[1] - start_position[1]
        
    if row_diff == 0 and col_diff == 1:
        return ">"
    elif row_diff == 0 and col_diff == -1:
        return "<"
    elif row_diff == 1 and col_diff == 0:
        return "v"
    elif row_diff == -1 and col_diff == 0:
        return "^"
    
    else:
        return None

def convert_instruction(instruction,pad):
    new_instructions =""
    for i in range(0,len(instruction)-1):
        new_instructions += get_relative_position(instruction[i],instruction[i+1],pad)
    return new_instructions

def get_directions_input(directions,codes,pad):
    list_inputs = ""
    start = "A"
    instructions_final = []
    for code in codes:
        instructions = [""]
        
        for k in code:
        
            temp = get_path(directions,start,k,pad)
            temp_instruction = []
            for t in temp:
                for i in instructions:
                    test = i+t
                    temp_instruction.append(i+t)
            instructions = temp_instruction

            start = k

        instructions_final += instructions
    return instructions_final



def get_full_direction_old(keyboard,directions,code):
    instruction = get_directions_input(keyboard,code,KEYBOARD)
    instructions1 = get_directions_input(directions,instruction,DIRECTIONS)
    instructions2 = get_directions_input(directions,instructions1,DIRECTIONS)

    return instructions2



def get_value(instruction,code):
    number = int(code[:-1])
    length = len(instruction)
    return length*number    

def filter_instructions(instructions):
    min_length = min([len(i) for i in instructions])
    new_instructions = [i for i in instructions if len(i) == min_length]
    return new_instructions

def get_full_direction(keyboard,directions,code):
    instruction = get_directions_input(keyboard,[code],KEYBOARD)
    instruction = filter_instructions(instruction)
    instructions1 = get_directions_input(directions,instruction,DIRECTIONS)
    instructions1 = filter_instructions(instructions1)
    instructions2 = get_directions_input(directions,instructions1,DIRECTIONS)
    final_instructions = filter_instructions(instructions2)
    return min(final_instructions,key = len)


@lru_cache
def solve_rec(start,end,directions,iteration):
    
    instructions = get_path(directions,start,end,DIRECTIONS)
    instructions = filter_instructions(instructions)
    if iteration == 1:
        return min([len(i) for i in instructions])
    totals = []

    for instruction in instructions:
        begin = "A"
        total = 0
        for i in instruction:
            total += solve_rec(begin,i,directions,iteration-1)
            begin = i
        totals.append(total)
    return min(totals)
        



    
    

    

def get_cost(code,keyboard,directions,iteration):
    instructions = get_directions_input(keyboard,[code],KEYBOARD)
    all_totals = []
    for instruction in instructions:
        total = 0
        start = "A"
        for i in instruction:
            total += solve_rec(start,i,directions,iteration)
     
            start = i
        all_totals.append(total)
    best = min(all_totals)
    print(f"Code: {code} - Best: {best}")
    return best * int(code[:-1])

def solve(input_file,iteration):
    total = 0
    codes = get_input(input_file)
    keyboard = get_graph(KEYBOARD)
    directions = get_graph(DIRECTIONS)
    for code in codes:
        total += get_cost(code,keyboard,directions,iteration)  
    print(f"Total: {total}") 


solve("day21/input.txt",25)