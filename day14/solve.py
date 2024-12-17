import re
from tkinter import *

class Robot:
    def __init__(self, description,width, height, num_movements = 100):
        position,velocity = description.strip().split(" ")
        self.position = self.get_vector(position)
        self.velocity = self.get_vector(velocity)
        self.num_movements = num_movements
        self.width = width
        self.height = height
    
    def get_vector(self,string):
        x,y = re.findall(r"[-\d]+",string)
        return (int(x),int(y))
    
    def get_final_position(self):
        final_x = int(self.position[0]) + int(self.velocity[0])*self.num_movements
        final_y = int(self.position[1]) + int(self.velocity[1])*self.num_movements
        final_x = final_x % self.width
        final_y = final_y % self.height
        self.position = (final_x,final_y)
        return (final_x,final_y)
    
    def get_final_quadrant(self):
        final_x,final_y = self.get_final_position()
        is_on_left = final_x < self.width//2
        is_on_top = final_y < self.height//2
        if final_x == self.width//2 or final_y == self.height//2:
            return 0
        if is_on_left and is_on_top:
            return 1 #Top left quadrant
        elif is_on_left and not is_on_top:
            return 2 #Bottom left quadrant
        elif not is_on_left and is_on_top:
            return 3 #Top right quadrant
        else:
            return 4 #Bottom right quadrant
    def move(self):
        self.position = (self.position[0] + self.velocity[0],self.position[1] + self.velocity[1])
        self.position = (self.position[0] % self.width,self.position[1] % self.height)

    def move_back(self):
        self.position = (self.position[0] - self.velocity[0],self.position[1] - self.velocity[1])
        self.position = (self.position[0] % self.width,self.position[1] % self.height)

    def get_position(self):
        return self.position
   

def get_input(file):
    with open(file) as f:
        return f.read().splitlines()
    
def solve_part1(input_file, width,height,num_movements = 100):
    input = get_input(input_file)
    quadrants = [0]*5
    
    for i in input:
        robot = Robot(i,width,height,num_movements)
        quadrant = robot.get_final_quadrant()
        quadrants[quadrant] += 1
    print(quadrants)
    total = 1
    for i in quadrants[1:]:
        total *= i
    print(f"Total: {total}")


def display(map):
    for i in range(len(map)):
        for j in range(len(map[0])):
            print(map[i][j],end = "")
        print()
def get_map(map):
    text = ""
    for i in range(len(map)):
        for j in range(len(map[0])):
            text+=map[i][j]
        text+="\n"
        
    return text



def move_all_roots(robots,width,height):

    my_map = [["." for i in range(width)] for j in range(height)]
    all_positions = []
    for robot in robots:
        robot.move()
        position = robot.get_position()
        all_positions.append(position)
    all_positions = set(all_positions)
    for position in all_positions:
        my_map[position[1]][position[0]] = "#"
    return my_map

def move_all_roots_back(robots,width,height):

    my_map = [["." for i in range(width)] for j in range(height)]
    all_positions = []
    for robot in robots:
        robot.move_back()
        position = robot.get_position()
        all_positions.append(position)
    all_positions = set(all_positions)
    for position in all_positions:
        my_map[position[1]][position[0]] = "#"
    return my_map




def show_map(root, my_map, iteration):
    
    text = get_map(my_map)
    
    # Clear the previous label widget
    for widget in root.winfo_children():
        widget.destroy()
    root.title(f"Day 14 - Iteration {iteration}")
    # Create a new label widget with updated text
    label = Label(root, text=text)
    label.pack()
    

def solve(input_file,width,height,num_movements = 100):
    my_input = get_input(input_file)
    robots = []
    for i in my_input:
        robots.append(Robot(i,width,height,num_movements))
    final_pos = []
    for robot in robots:
        final_pos.append(robot.get_final_position())

    my_map = [["." for i in range(width)] for j in range(height)]
    for position in final_pos:
        my_map[position[1]][position[0]] = "#"

    keep_display = True
    iteration = 8259

    
    root =  Tk()
    root.title("Day 14")
    my_map = move_all_roots(robots, width, height)
    show_map(root,my_map,iteration)
    
    def key_press(event):
        nonlocal iteration  # Declare iteration as nonlocal
        nonlocal root
        nonlocal robots
        nonlocal width
        nonlocal height
        if event.keysym == "space":
            my_map = move_all_roots(robots, width, height)
            show_map(root,my_map,iteration)
            print("Iteration:", iteration)
            iteration += 1
        if event.keysym == "BackSpace": 
            my_map = move_all_roots_back(robots, width, height)
            show_map(root,my_map,iteration)
            print("Iteration:", iteration)
            iteration -= 1
            

    
    root.bind("<Key>", key_press)  # Bind key press event
    
    root.mainloop()
        
    
    
solve("day14/input.txt",101,103,8259)