from collections import defaultdict
from functools import lru_cache
def get_input(input_file):
    with open(input_file, 'r') as file:
        return [ line.split("-") for line in file.read().splitlines()]


def get_all_combinations(input):
    combinations = []
    for line in input:
        a,b = line
        combinations.append({a,b})
    return combinations


def get_all_connections(input):
    connections = defaultdict(list)
    for line in input:
        a,b = line
        connections[a].append(b)
        connections[b].append(a)
    return connections

def get_interconnected(connections):
    interconnected = []
    for key in connections:
        for elem in connections[key]:
            if elem in connections:
                interconnected.append({key, elem})
    return interconnected

def get_triangle(connections):
    triangles = []
    for key in connections:
        for elem in connections[key]:
            if elem in connections:
                for elem2 in connections[elem]:
                    if elem2 in connections:
                        if key in connections[elem2]:
                            triangles.append((key, elem, elem2))
    return set(triangles)


def get_largest_rec(connections,elements,building):
    if len(elements) == 0 :
        return building
    
    for elem in elements:
        is_possible = True
        build_without = get_largest_rec(connections, elements - {elem}, building)
        for key in building:
            if elem not in connections[key] and key not in connections[elem]:
                is_possible = False
                break
        if is_possible:
            build_with = get_largest_rec(connections, elements - {elem}, building.union({elem}))
            if len(build_with) > len(build_without):
                return build_with
        return build_without
            





def get_largest_connection(connections):
    final_connections = []
    elements = set(connections.keys())
    largest =  get_largest_rec(connections, elements, set())
    sorted_list = sorted(list(largest))
    answer = ",".join(sorted_list)
    print(answer)

            




def get_final_triangles(triangles):
    final_triangles = []
    triangle_set = set()
    for triangle in triangles:
        triangle_set.add(frozenset(triangle))
    for triangle in triangle_set:
        if any([elem.startswith("t") for elem in triangle]):
            final_triangles.append(tuple(triangle))
    return final_triangles

def solve(input_file):
    input = get_input(input_file)
    connections = get_all_connections(input)
    get_largest_connection(connections)

  




solve("day23/input.txt")