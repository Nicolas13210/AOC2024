import networkx as nx

def create_maze_graph_with_costs(maze):
    rows, cols = len(maze), len(maze[0])
    G = nx.DiGraph()  # Use a directed graph to handle different costs for different directions
    
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] in ".SE":  # 0 represents a walkable cell
                for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                    G.add_node((r,c, direction), weight=1)
                    
                    y, x = r + direction[0], c + direction[1]
                    if 0 <= y < rows and 0 <= x < cols and maze[y][x] in ".SE":
                        for direction_2 in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
                            if direction_2 != direction:
                                G.add_edge((r, c, direction), (y, x, direction_2), weight=1001)
                            else:
                                G.add_edge((r, c,direction), (y, x,direction_2), weight=1)
               
   
    return G

def find_shortest_path_with_costs(G, start, end):
    try:
        path = nx.shortest_path(G, source=start, target=end, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None

def calculate_path_cost(G, path):
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += G[path[i]][path[i + 1]]['weight']
    return total_cost

def find_shortest_path(maze, start, end):
    path = find_shortest_path_with_costs(maze, start, end)
    if path is None:
        return None,float('inf')
    cost = calculate_path_cost(maze, path)
    return path,cost

def get_optimal_end(maze, start,end):
    best_score = float('inf')
    best_direction = []
    for direction in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        the_end = (end[0], end[1], direction)
        path,score = find_shortest_path(maze, start, the_end)
        if score < best_score:
            best_score = score
            best_direction = [direction]
        elif score == best_score:
            best_direction.append(direction)
    print(f"Best score: {best_score}")
    return best_direction

def find_all_shortest_paths(G, start, end):
    print("Solving every path")
    all_paths = list(nx.all_shortest_paths(G, source=start, target=end,weight='weight'))
    paths = []
    for path in all_paths:
        current_path = []
        for tile in path:
            current_path.append((tile[0], tile[1]))
        paths.append(current_path)
    return paths



def get_maze_from_file(file_path):
    with open(file_path, 'r') as file:
        maze = [list(line.strip()) for line in file]
    return maze
def get_start(maze):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == "S":
                return (r, c,(0,1))
    return None

def get_end(maze):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == "E":
                return (r, c)
    return None

def display_maze(maze,path):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if (r, c) in path:
                print("o", end="")
            else:
                print(maze[r][c], end="")
        print()

def solve(file_path):
    maze = get_maze_from_file(file_path)
    start = get_start(maze)
    end = get_end(maze)
    r,c,direction = start
    G = create_maze_graph_with_costs(maze)
    for direction1 in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
        if direction1 != direction:
            G.add_edge((r, c, direction), (r, c, direction1), weight=1000)
    print("Finding shortest path")
    best_direction = get_optimal_end(G, start, end)
    my_paths = []
    for direction in best_direction:
        
        the_end = (end[0], end[1], direction)
        my_paths += find_all_shortest_paths(G, start, the_end)
    
    cell = []
    print("Displaying paths")
    for path in my_paths:
        cell += path
    print(len(set(cell)))

    
    
    
   


solve("day16/example.txt")