import z3
import re
import sys
class Machine:
    def __init__(self, description,multiplier = 10000000000000):
        description = description.strip().splitlines()

        regex = re.compile(r"[+-=]\d+")
        coordinates = [regex.findall(line) for line in description]
        self.buttons = {}
        self.prize = (0,0)
        self.price_A = 3
        self.price_B = 1
        self.multiplier = multiplier
        for k in range(len(coordinates)):
            if description[k].startswith("Button"):
                self.buttons[description[k].split(":")[0]] = self.get_coordinates(coordinates[k])
            elif description[k].startswith("Prize"):
                self.prize = self.get_coordinates(coordinates[k],multiplier)
            else:
                print("Invalid input")
                return
        
    def get_number(self,string,multiplier ):
        if string[0] in '+-':
            return int(string) + multiplier
        else:
            return int(string[1:]) + multiplier
        
    def get_coordinates(self, coordinates,multiplier = 0):
        x = self.get_number(coordinates[0],multiplier)
        y = self.get_number(coordinates[1],multiplier)
        return (x, y)
    
    def is_solvable(self):
        answer = solve_machine(self.buttons["Button A"][0],self.buttons["Button A"][1],self.buttons["Button B"][0],self.buttons["Button B"][1],self.prize[0],self.prize[1])
        if answer:
            return 3* answer[0] + answer[1]
        else:
            return 0

    
  
def get_input(file_path):
    with open(file_path, "r") as file:
        return file.read().split("\n\n")
    
def solve(file_path,multiplier = 10000000000000):
    total = 0
    description = get_input(file_path)
    for desc in description:
        machine = Machine(desc,multiplier=multiplier)
        total +=machine.is_solvable()
    print(f"Total: {total}")


        

def solve_machine(xa, ya, xb, yb, xs, ys):
    a = z3.Int('a')
    b = z3.Int('b')
    s = z3.Solver()
    s.add(a * xa + b * xb == xs)
    s.add(a * ya + b * yb == ys)

    if s.check() == z3.sat:
        model = s.model()
        A = model[a].as_long()
        B = model[b].as_long()
        return A,B
    else:
        return False


solve("day13/input.txt")

