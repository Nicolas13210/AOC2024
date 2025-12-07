from functools import lru_cache 
import networkx as nx
def get_maze(input_file):
    with open(input_file) as f:
        return [list(line) for line in f.read().splitlines()]
    
def get_start(maze):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'S':
                return (i, j)

def get_end(maze):
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == 'E':
                return (i, j)
def solve_path(maze,start,end):
    i=1
    last_position = start
    maze[start[0]][start[1]] = i
    path = {0:start}

    while start != end:
        for direction in [(0,1),(0,-1),(1,0),(-1,0)]:
            new_position = (start[0]+direction[0],start[1]+direction[1])
            if new_position == last_position:
                continue
            if new_position[0]<0 or new_position[0]>=len(maze) or new_position[1]<0 or new_position[1]>=len(maze[0]):
                continue
            if maze[new_position[0]][new_position[1]] != '#':

                last_position = start
                start = new_position
                maze[start[0]][start[1]] = i
                path[i] = start
                i+=1
                break
    return maze,path

def get_manhattan_distance(start,end):
    return abs(start[0]-end[0])+abs(start[1]-end[1])

def get_candidates(path, min_saved,max_path):
    candidates = set()
    for k in range(len(path)-max_path):
        for j in range(k +max_path,len(path)):
            distance = get_manhattan_distance(path[j], path[k])
            if distance<= max_path and j -k -distance >= min_saved:
                candidates.add((k,j))
    return len(candidates)

def get_wal_graph(maze):
    G = nx.Graph()
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == '#':
                G.add_node((i, j))
                for direction in [(0,1),(0,-1),(1,0),(-1,0)]:
                    new_position = (i+direction[0],j+direction[1])
                    if new_position[0]<0 or new_position[0]>=len(maze) or new_position[1]<0 or new_position[1]>=len(maze[0]):
                        continue
                    if maze[new_position[0]][new_position[1]] == '#':
                        G.add_edge((i,j),new_position)
    return G

def get_temp_graph(G_original,maze,start,end):
    G = G_original.copy()
    G.add_node(start)
    G.add_node(end)
    for direction in [(0,1),(0,-1),(1,0),(-1,0)]:
        new_start = (start[0]+direction[0],start[1]+direction[1])
        if new_start[0]<0 or new_start[0]>=len(maze) or new_start[1]<0 or new_start[1]>=len(maze[0]):
            continue
        if maze[new_start[0]][new_start[1]] == '#':
            G.add_edge(start,new_start)
    for direction in [(0,1),(0,-1),(1,0),(-1,0)]:
        new_end = (end[0]+direction[0],end[1]+direction[1])
        if new_end[0]<0 or new_end[0]>=len(maze) or new_end[1]<0 or new_end[1]>=len(maze[0]):
            continue
        if maze[new_end[0]][new_end[1]] == '#':
            G.add_edge(end,new_end)

    return G

def get_time_saved(G, maze, candidate, min_saved, max_path):
    start,end,score = candidate
    G = get_temp_graph(G,maze,start,end)
    try:
        path = nx.shortest_path(G,start,end)
        time_saved = score - len(path) + 1
    except nx.NetworkXNoPath:
        time_saved = 0

    if len(path) > max_path + 1:
        time_saved = 0

    return time_saved

def get_all_time_saved(G, maze, path, min_saved, max_path):
    candidates = get_candidates(path, min_saved,max_path)
    result = {}
    time_saved = [get_time_saved(G, maze, candidate, min_saved, max_path) for candidate in candidates]
    for elem in time_saved:
        if elem in result:
            result[elem] += 1
        else:
            result[elem] = 1

    
    return result



def solve(input_file,max_path, min_saved):
    maze = get_maze(input_file)
    start = get_start(maze)
    end = get_end(maze)
    solved_maze, path= solve_path(maze,start,end)
    total = get_candidates(path, min_saved,max_path)
    print(f'Total candidates: {total}')
    
solve("day20/input.txt",20,100)