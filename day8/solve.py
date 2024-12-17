import copy
def get_map(input_file):
    with open(input_file, 'r') as file:
        return [[k for k in line] for line in file.read().splitlines()]
    
def print_map(map):
    for line in map:
        print(''.join(line))


def get_all_nodes(map, node):
    nodes = []
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == node:
                nodes.append((y,x))
    return nodes


def create_harmonics(node,y_distance,x_distance,size):
    y,x = node
    harmonics = []
    while(x+x_distance >= 0 and x+x_distance < size and y+y_distance >= 0 and y+y_distance < size):
        y += y_distance
        x += x_distance
        harmonics.append((y,x))
    return harmonics


def  get_antinode_bis(node_a, node_b,size):
    antinodes = []
    x_distance = node_a[1] - node_b[1]
    y_distance = node_a[0] - node_b[0]
    harmonics_a = create_harmonics(node_a,y_distance,x_distance,size)
    harmonics_b = create_harmonics(node_b,-y_distance,-x_distance,size)
    harmonics = harmonics_a + harmonics_b
    harmonics.append(node_a)
    harmonics.append(node_b)
    return harmonics

def get_antinode(node_a, node_b):
    x_distance = node_a[1] - node_b[1]
    y_distance = node_a[0] - node_b[0]
    antinode_a = (node_a[0] + y_distance, node_a[1] + x_distance)
    antinode_b = (node_b[0] - y_distance, node_b[1] - x_distance)
    return antinode_a, antinode_b

def get_all_antinodes_bis(map, frequencies):
    antinodes = set()
    for nodes in frequencies.values():
        for k in range(len(nodes)-1):
            for j in range(k+1, len(nodes)):
                temp_antinodes = get_antinode_bis(nodes[k], nodes[j],len(map))
                for elem in temp_antinodes:
                    antinodes.add(elem)
    
    antinodes = list(antinodes)


    return len(antinodes)

def get_all_antinodes(map, frequencies):
    antinodes = set()
    for nodes in frequencies.values():
        for k in range(len(nodes)-1):
            for j in range(k+1, len(nodes)):
                antinode_a,antinode_b = get_antinode(nodes[k], nodes[j])
                antinodes.add(antinode_a)
                antinodes.add(antinode_b)
    
    antinodes = list(antinodes)

    for node in copy.deepcopy(antinodes):
        if node[0] < 0 or node[0] >= len(map) or node[1] < 0 or node[1] >= len(map[0]):
            antinodes.remove(node)

    return len(antinodes)

def get_all_frequency(map):
    frequency = {}
    for y in range(len(map)):
        for x in range(len(map[y])):
            if map[y][x] == ".":
                continue
            if map[y][x] in frequency:
                frequency[map[y][x]].append((y,x))
            else:
                frequency[map[y][x]] = [(y,x)]
    return frequency

def solve(input_file):
    map = get_map(input_file)
    frequencies = get_all_frequency(map)
    total = get_all_antinodes_bis(map, frequencies)
    print(f"Total antinodes: {total}")



solve('day8/input.txt')