import copy
import sys
sys.setrecursionlimit(10000000)


DIRECTIONS = {"^": (-1, 0), "v": (1, 0), "<": (0, -1), ">": (0, 1)}
def get_input(input_path):
    with open(input_path, 'r') as file:
        room,instructions = file.read().split('\n\n')
    room = [[k for k in line] for line in room.split('\n')]
    instructions = instructions.replace("\n","").strip()
    return room, instructions


def get_starting_position(room):
    for i in range(len(room)):
        for j in range(len(room[0])):
            if room[i][j] == '@':
                return i, j
            
def is_pushable(room, position,direction):
    i, j = position
    if room[i][j] == "#":
        return False
    if room[i][j] == ".":
        return True
    if room[i][j] == "O":
        return is_pushable(room, (i + direction[0], j + direction[1]),direction)
    if direction[0] != 0:
        if room[i][j] == "[":
            left = is_pushable(room,  (i + direction[0], j + direction[1]),direction)
            right = is_pushable(room,  (i + direction[0], j + 1 + direction[1]),direction)
            return left and right
        else:
            left = is_pushable(room,  (i + direction[0], j - 1 + direction[1]),direction)
            right = is_pushable(room,  (i + direction[0], j + direction[1]),direction)
            return left and right
    return is_pushable(room,  (i + direction[0], j + direction[1]),direction)
    

def push_object(room, position, direction,object):
    if not is_pushable(room, position, direction):
        return room
    i, j = position
    if room[i][j] == ".":
        room[i][j] = object
        return room
    
    if room[i][j] == "O":
        room[i][j] = object
        return push_object(room, (i + direction[0], j + direction[1]), direction, "O")
    if direction[0] !=0:
        if room[i][j] == "[":
            room[i][j] = object
            room[i][j + 1] = "."
            room = push_object(room, (i + direction[0], j + direction[1]), direction, "[")
            room = push_object(room, (i + direction[0], j + 1 + direction[1]), direction, "]")
            return room
        else:
            room[i][j] = object
            room[i][j - 1] = "."
            room = push_object(room, (i + direction[0], j - 1 + direction[1]), direction, "[")
            room = push_object(room, (i + direction[0], j + direction[1]), direction, "]")
            return room
    else:
        if room[i][j] in "[]":
            temp = room[i][j]
            room[i][j] = object
            room = push_object(room, (i + direction[0], j + direction[1]), direction,temp)
            return room
      



def recursive_solve(room, instructions, position):
    if instructions == "":
        return room
    i, j = position
    direction = DIRECTIONS[instructions[0]]
    if room[i + direction[0]][j + direction[1]] == "#":
        return recursive_solve(room, instructions[1:], (i, j))
    
    if room[i + direction[0]][j + direction[1]] == ".":
        room[i + direction[0]][j + direction[1]] = "@"
        room[i][j] = "."
        return recursive_solve(room, instructions[1:], (i + direction[0], j + direction[1]))
    else:
        if is_pushable(room, (i + direction[0], j + direction[1]), direction):
            room[i + direction[0]][j + direction[1]] = "@"
            room[i][j] = "."
            return recursive_solve(room, instructions[1:], (i + direction[0], j + direction[1]))
        else:
            return recursive_solve(room, instructions[1:], (i, j))

def iterative_solve(room, instructions, position):
    while instructions != "":
        i, j = position
        direction = DIRECTIONS[instructions[0]]
        if room[i + direction[0]][j + direction[1]] == "#":
            instructions = instructions[1:]
            continue
        if room[i + direction[0]][j + direction[1]] == ".":
            room[i + direction[0]][j + direction[1]] = "@"
            room[i][j] = "."
            position = (i + direction[0], j + direction[1])
            instructions = instructions[1:]
            continue
        else:
            if is_pushable(room, (i + direction[0], j + direction[1]), direction):
                push_object(room, (i + direction[0], j + direction[1]), direction, "@")
                room[i][j] = "."
                position = (i + direction[0], j + direction[1])
                instructions = instructions[1:]
                continue
            else:
                instructions = instructions[1:]
                continue
    return room

def upscale_room(room):
    new_map = []
    for i in range(len(room)):
        line =""
        for j in range(len(room[0])):
            if room[i][j] in "#.":
                line += 2*room[i][j]
            elif room[i][j] == "@":
                line += "@."
            elif room[i][j] == "O":
                line += "[]"
        new_map.append([k for k in line])
    return new_map

    
def get_room_score(room):
    score = 0
    for i in range(len(room)):
        for j in range(len(room[0])):
            if room[i][j] in "O[":
                score += i*100 + j
    return score


def print_room(room):
    for line in room:
        print("".join(line))
def solve(input_file):
    print("starting")
    room, instructions = get_input(input_file)
    starting_position = get_starting_position(room)
    final_room = iterative_solve(copy.deepcopy(room), instructions, starting_position)
    score = get_room_score(final_room)
    print(f"Score part 1: {score}")
    upscaled = upscale_room(copy.deepcopy(room))
    starting_position = get_starting_position(upscaled)
    final_bis = iterative_solve(upscaled, instructions, starting_position)
    score_bis = get_room_score(final_bis)
    
    print(f"Score part 2: {score_bis}")


solve("day15/input.txt")