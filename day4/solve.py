import re


REGEX = r"XMAS"
REGEX_REVERSE = r"SAMX"
def get_input(input_file):
    with open(input_file, 'r') as file:
        data = file.read().splitlines()
    return data


def get_xmas_line(data):
    total = 0
    for line in data:
        occurences = re.findall(REGEX, line)
        occurences_bis = re.findall(REGEX_REVERSE, line)
        total += len(occurences) + len(occurences_bis)
    return total

def get_xmas_diagonal(data):
    total = 0
    diagonals = []
    for k in range(len(data)):
        line = [data[k-j][j] for j in range(k+1)]
        diagonals.append("".join(line))

    for k in range(1,len(data)):
        line = [data[k+j][j] for j in range(len(data)-k)]
        diagonals.append("".join(line))

    print(diagonalsBis)


    total += get_xmas_line(diagonals)
    print(f"Diagonal: {total}")
    print(f"Number of diagonals: {len(diagonals)}")
    print(diagonals)
    return total

def get_xmas_vertical(data):
    total = 0
    verticals = []
    for k in range(len(data)):
        line = [data[i][k] for i in range(len(data))]
        verticals.append("".join(line))
    total += get_xmas_line(verticals)
    print(f"Vertical: {total}")
    return total

def get_reverse_data(data):
    reverse_data = []
    for line in data:
        reverse_data.append(line[::-1])
    return reverse_data

def process(data, x, y):
    for i in [-1,1]:
        for j in [-1,1]:
            if (data[x+i][y+j] == "A") or (data[x+i][y+j] == data[x-i][y-j] ) or (data[x+i][y+j] == "X"):
                return False
            
    return True 


def solve2(input_file):
    data = get_input(input_file)
    total = 0
    it=0
    for i in range(1,len(data)-1):
        for j in range(1,len(data)-1):
            if data[i][j]=="A":
                it +=1
                if process(data, i, j):
                    total += 1
    print(f"Total = {total}")
def solve(input_file):
    data = get_input(input_file)
    total = 0
    total += get_xmas_line(data)
    print(f"line = {total}")
    total += get_xmas_diagonal(data)
    
    total += get_xmas_vertical(data)
    reversed = get_reverse_data(data)
    total += get_xmas_diagonal(reversed)
    print(f"total = {total}")

solve2('day4/input.txt')
# solve2('day4/example.txt')
