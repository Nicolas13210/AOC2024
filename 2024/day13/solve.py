
import re
import sys
class Machine:
    def __init__(self, description,limit = 100,multiplier = 10000000000000):
        description = description.strip().splitlines()

        regex = re.compile(r"[+-=]\d+")
        coordinates = [regex.findall(line) for line in description]
        self.buttons = {}
        self.prize = (0,0)
        self.price_A = 3
        self.price_B = 1
        self.limit = limit
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
    
    def get_combination_recursive(self,x,y,price,limit,memory): #Useless but fun
        print(f"Price {price}, Coordinates = {x},{y}")
        if (x,y) == self.prize:
            return price
        if memory["Button A"] >= limit and memory["Button B"] >= limit:
            return sys.maxsize
        
        #Button A
        memoryA = memory.copy()
        memoryA["Button A"] += 1
        combinationA = self.get_combination(x+self.buttons["Button A"][0],y+self.buttons["Button A"][1],price+self.price_A,limit-1,memoryA)

        #Button B
        memoryB = memory.copy()
        memoryB["Button B"] += 1
        combinationB = self.get_combination(x+self.buttons["Button B"][0],y+self.buttons["Button B"][1],price+self.price_B,limit-1,memoryB)

        


        return min(combinationA,combinationB)
    
    def get_best_combination_rec(self):
        combination =  self.get_combination(0,0,0,self.limit,{"Button A": 0, "Button B": 0})
        if combination == sys.maxsize:
            return "No solution found"
        return combination
    
    def get_best_combination(self):
        ax,ay = self.buttons["Button A"]
        bx,by = self.buttons["Button B"]
        px,py = self.prize
        prices = []
        for a in range(self.limit):
            for b in range(self.limit):
                if a*ax + b*bx == px and a*ay + b*by == py:
                    prices.append(a*self.price_A + b*self.price_B)
        if not prices:
            return 0
        return min(prices)
    
    def find_best_combination(self):
        max = sys.maxsize
        answer = self.is_solvable()
        if not answer:
            return 0
        for combination in answer:
            if combination[0] * self.price_A + combination[1] * self.price_B < max:
                max = combination[0] * self.price_A + combination[1] * self.price_B
        print(max)
        return max
    
    def is_solvable(self):
        max = self.prize[0] + self.prize[1]
        min = 100000
        solutions_x = find_all_solutions(self.buttons["Button A"][0],self.buttons["Button B"][0],self.prize[0],100000,max)
        if solutions_x == 0:
            return False
        solutions_y = find_all_solutions(self.buttons["Button A"][1],self.buttons["Button B"][1],self.prize[1],100000,max)
        if solutions_y == 0:
            return False
        answer = find_common_elements(solutions_x,solutions_y)
        return answer
       # print(answer)
        
    
def get_gcd(a,b):
    while b:
        a, b = b, a % b
    return a

        
def get_input(file_path):
    with open(file_path, "r") as file:
        return file.read().split("\n\n")
    
def solve(file_path,multiplier = 10000000000000):
    total = 0
    description = get_input(file_path)
    for desc in description:
        machine = Machine(desc,limit=sys.maxsize,multiplier=multiplier)
        total +=machine.find_best_combination()
    print(f"Total: {total}")

        
def gcdExtended(a, b): 
    # Base Case 
    if a == 0 : 
        return b,0,1
             
    gcd,x1,y1 = gcdExtended(b%a, a) 
     
    # Update x and y using results of recursive 
    # call 
    x = y1 - (b//a) * x1 
    y = x1 
     
    return gcd,x,y

def find_any_solution(a,b,c):
    d1,x1,y1 = gcdExtended(a,b)
    if c % d1 != 0:
        return False
    x0 = x1 * (c // d1)
    y0 = y1 * (c // d1)
    return [x0,y0,d1]


def shift_solution(x,y,a,b,cnt):
    x += cnt * b
    y -= cnt * a
    return x,y

def find_common_elements(list1,list2):
    return [element for element in list1 if element in list2]

    
def find_all_solutions(a,b,c,min,max):
    answer = find_any_solution(a,b,c)
    if not answer :
        return 0
    x,y,g = answer
    sign = 1 if x<0 else -1
    solutions = []
    while(y<min or x < min):
        sign = 1 if x<0 else -1
        if x<min and y<min:
            return 0
        x,y = shift_solution(x,y,a,b,sign)
    
    while(y>max or x > max):
        solutions.append((x,y))
        sign = -1 if x>0 else 1
        if x>max and y>max:
            return 0
        x,y = shift_solution(x,y,a,b,sign)
    
    while(y>min and x < max):
        solutions.append((x,y))
        x,y = shift_solution(x,y,a,b,1)

    while(y<max and x > min):
        solutions.append((x,y))
        x,y = shift_solution(x,y,a,b,-1)
    return set(solutions)
    
solve("day13/example.txt")
#print(find_combination(94,34,22,67,8400,5400))