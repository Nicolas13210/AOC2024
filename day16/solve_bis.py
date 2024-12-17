import networkx as nx

def create_maze_graph_with_costs(maze):
    rows, cols = len(maze), len(maze[0])
    G = nx.DiGraph()  # Use a directed graph to handle different costs for different directions
    
    for r in range(rows):
        for c in range(cols):
            if maze[r][c] in ".SE":  # 0 represents a walkable cell
                G.add_node((r, c))
                if r > 0 and maze[r-1][c] in ".SE":
                    G.add_edge((r, c), (r-1, c), weight=1)
                if c > 0 and maze[r][c-1] in ".SE":
                    G.add_edge((r, c), (r, c-1), weight=1)
                if r < rows - 1 and maze[r+1][c] in ".SE":
                    G.add_edge((r, c), (r+1, c), weight=1)
                if c < cols - 1 and maze[r][c+1] in ".SE":
                    G.add_edge((r, c), (r, c+1), weight=1)
   
    return G

def find_shortest_path_with_costs(maze, start, end):
    G = create_maze_graph_with_costs(maze)
    try:
        path = nx.shortest_path(G, source=start, target=end, weight='weight')
        return path
    except nx.NetworkXNoPath:
        return None

def calculate_path_cost(G, path):
    cost = 0
    direction = (0,1)
    for i in range(len(path) - 1):
        current = path[i]
        next = path[i + 1]
        cost += 1
        y_direction = next[0] - current[0]
        x_direction = next[1] - current[1]
        if (y_direction, x_direction) != direction:
            cost += 1000
            direction = (y_direction, x_direction)
    return cost

def find_all_shortest_paths_with_costs(maze, start, end):
    G = create_maze_graph_with_costs(maze)
    print("Solving every path")
    all_paths = list(nx.all_simple_paths(G, source=start, target=end))
    if not all_paths:
        return None
    print("Calculating costs")
    # Calculate the cost of each path
    path_costs = [(path, calculate_path_cost(G, path)) for path in all_paths]
    
    # Find the minimum cost
    min_cost = min(cost for path, cost in path_costs)
    
    # Filter paths with the minimum cost
    shortest_paths = [path for path, cost in path_costs if cost == min_cost]
    
    return shortest_paths



def get_maze_from_file(file_path):
    with open(file_path, 'r') as file:
        maze = [list(line.strip()) for line in file]
    return maze
def get_start(maze):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == "S":
                return (r, c)
    return None

def get_end(maze):
    for r in range(len(maze)):
        for c in range(len(maze[0])):
            if maze[r][c] == "E":
                return (r, c)
    return None

def solve(file_path):
    maze = get_maze_from_file(file_path)
    start = get_start(maze)
    end = get_end(maze)
    path = find_all_shortest_paths_with_costs(maze, start, end)
    my_paths = []
    for i in path:
        my_paths += i
    my_paths = list(set(my_paths))
    if path:
        print("Shortest path:", len(my_paths))
    else:
        print("No path found")


solve("day16/input.txt")