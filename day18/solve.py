import networkx as nx
DIRECTIONS = [(0,1),(0,-1),(1,0),(-1,0)]
def get_input(file_path: str):
    with open(file_path, "r") as file:
        return [(int(line.split(",")[1]),int(line.split(",")[0])) for line in file.readlines()]
    

def create_graph(blocks,size):
    G = nx.Graph()
    for i in range(size):
        for j in range(size):
            if (i,j) in blocks:
                continue
            G.add_node((i,j))
            for direction in DIRECTIONS:
                if (i+direction[0],j+direction[1]) not in blocks:
                    G.add_edge((i,j),(i+direction[0],j+direction[1]))
    return G

def print_maze(G,size,path):
    for i in range(size):
        for j in range(size):
            if (i,j) in path:
                print("o",end="")
            elif (i,j) in G.nodes:
                print(".",end="")
            else:
                print("#",end="")
        print()

def look_for_end(G,size,blocks):
    for block in blocks:
        print(block)
        G.remove_edges_from(list(G.edges((block))))
        G.remove_node(block)
        try:
            path = nx.shortest_path(G,(0,0),(size-1,size-1))
        
        except:
            return block[1],block[0]

    return None


def get_shortest_path(G,size):
    start = (0,0)
    end = (size-1,size-1)
    return nx.shortest_path(G,start,end)

def solve(input_file,size,instructions):
    blocks = get_input(input_file)
    part1 = blocks[:instructions]
    print(part1[-1])
    part2 = blocks[instructions:]
    last = look_for_end(create_graph(part1,size),size,part2)
    print(last)
    
    path = get_shortest_path(create_graph(part1,size),size)
    print(len(path)-1)

solve("day18/input.txt",71,1024)