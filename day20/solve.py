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
            
def get_path(maze, start, end):
    i = 0
    maze[start[0]][start[1]] = i
    last_position = start
    while start !=end:
        i +=1
        for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            new_position = (start[0] + direction[0], start[1] + direction[1])
            if new_position == last_position:
                continue
            elif maze[new_position[0]][new_position[1]] in '.ES':
                maze[new_position[0]][new_position[1]] = i
                last_position = start
                start = new_position

                break
    return maze

def display_maze(maze):
    for row in maze:
        print(''.join(str(cell) for cell in row))

def get_neighbours(maze, position):
    neighbours = []
    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        new_position = (position[0] + direction[0], position[1] + direction[1])
        if new_position [0] < 0 or new_position[0] >= len(maze) or new_position[1] < 0 or new_position[1] >= len(maze[0]):
            continue
        
        neighbours.append(new_position)
    return neighbours

def rec_shortest_path(maze,position,num_cheats):
    if num_cheats == 0:
        return [(0,0)]
    if maze[position[0]][position[1]] != '#':
        #print(f"position: {position}, value: {maze[position[0]][position[1]]}, start_value: {start_value}")
        
        return [position]
    neighbours = get_neighbours(maze, position)
    finish = []
    for neighbour in neighbours:
        finish += rec_shortest_path(maze, neighbour, num_cheats - 1) 

    return finish

def compute_saved(maze,start,end):
    saved = maze[end[0]][end[1]] - start - 2
    return start - maze[end[0]][end[1]]- 2
    
def get_time_saved(maze,position,num_cheats):
    neighbours = [k for k in get_neighbours(maze, position) if maze[k[0]][k[1]] !="#"]
    if len(neighbours) < 2:
        return [0]
    start_value = max(maze[position[0]][position[1]] for position in neighbours)
    finish_position = rec_shortest_path(maze, position, num_cheats)
    finish_position = [position for position in finish_position if position!=(0,0)]
    all_duration  = [compute_saved(maze,start_value,position) for position in finish_position]
    durations = [durations for durations in all_duration if durations > 0]
    # durations = [durations for durations in [compute_saved(maze,position,finish_position) for position in neighbours] if durations > 0]
    return durations


def get_time_saved_bis(maze, position):
    neighnours = get_neighbours(maze, position)
    if len(neighnours)< 2:
        return 0
    start = min(neighnours, key = lambda x: maze[x[0]][x[1]])
    end = max(neighnours, key = lambda x: maze[x[0]][x[1]])
    return maze[end[0]][end[1]] - maze[start[0]][start[1]] - 2



def get_all_cheats(maze,num_cheats):
    cheats = {}
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell =="#":
                cheat = get_time_saved(maze, (i, j),num_cheats)
                for time_saved in cheat:
                    if not time_saved in cheats:
                        cheats[time_saved] = 1
                    else:
                        cheats[time_saved] += 1
    cheats.pop(0, None)
    return cheats

def get_cheats_above_threshold(maze, threshold,num_cheats):
    cheats = get_all_cheats(maze,num_cheats)
    return sum(count for time_saved, count in cheats.items() if time_saved >= threshold)

def get_path_cell(maze):
    path = {}
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell != '#':
                path[cell] = (i, j)
    path = dict(sorted(path.items(),reverse=True))
    return path

def get_manhattan_distance(start,end):
    return abs(start[0]-end[0]) + abs(start[1]-end[1])

def get_potential_candidates(path,min_saved,max_distance):
    candidates = []
    for k in range(min_saved, len(path)):
        for i in range(0,k-min_saved-1):
            if get_manhattan_distance(path[k],path[i]) <= max_distance:
                candidates.append((path[k],path[i]))

    return candidates

def get_graph(maze):
    G = nx.Graph()
    for i, row in enumerate(maze):
        for j, cell in enumerate(row):
            if cell == '#':
                G.add_node((i,j))
                for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    new_position = (i + direction[0], j + direction[1])
                    if new_position[0] < 0 or new_position[0] >= len(maze) or new_position[1] < 0 or new_position[1] >= len(maze[0]):
                        continue
                    if maze[new_position[0]][new_position[1]] == '#':
                        G.add_edge((i,j), new_position)
    return G 

def get_shortest_path(G_original,maze,start,end,max_distance):
    G = G_original.copy()
    G.add_node(start)
    G.add_node(end)
    for direction in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        for position in [end,start]:
            new_position = (position[0] + direction[0], position[1] + direction[1])
            if new_position[0] < 0 or new_position[0] >= len(maze) or new_position[1] < 0 or new_position[1] >= len(maze[0]):
                continue
            if maze[new_position[0]][new_position[1]] == '#':
                G.add_edge(position, new_position)
    
    
   


    path = nx.shortest_path(G,start,end)
    
    if len(path) >max_distance+1:
        return 0
    print(f"start: {start}, end: {end}, path: {len(path)}")
    return 1

def solve(input_file,num_cheats,min_saved):
    maze = get_maze(input_file)
    start = get_start(maze)
    end = get_end(maze)
    solved_maze = get_path(maze, end, start)
    path = get_path_cell(solved_maze)
    candidates = get_potential_candidates(path,min_saved,num_cheats)
    G = get_graph(solved_maze)
    total = 0
    for candidate in candidates:
        temp = G.copy()
        total += get_shortest_path(temp,solved_maze,candidate[0],candidate[1],num_cheats)
    print(total)
    print(len(candidates))
    #print(len(candidates))

    
solve("day20/example.txt",20,50)