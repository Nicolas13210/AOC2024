import sys
import time
from collections import Counter
def get_input(file_path: str):
    with open(file_path, "r") as file:
        return file.read().strip().split(" ")
    

def part1(data,iterations):
    if iterations == 0:
        return len(data)
    
    new_data = []
    for elem in data:
        if elem == "0":
            new_data.append("1")
        elif len(elem)%2 ==0:
            new_data.append(elem[:len(elem)//2])
            new_data.append(str(int(elem[len(elem)//2:])))
        else:
            new_data.append(str(int(elem)*2024))
    return part1(new_data,iterations-1)
    

        
        
        



def iterate_dico(dico, input, iterations,my_dico):
    if input not in dico:
        raise ValueError("Input not in dico")
    
    if iterations == 0:
        return len(dico[input])
    
    total = 0
    if iterations-1 not in my_dico:
        my_dico[iterations-1] = {}
    
    

    for key in dico[input]:
        if key in my_dico[iterations-1]:
            total += my_dico[iterations-1][key]
        else:
            temp = iterate_dico(dico, key, iterations-1,my_dico)
            my_dico[iterations-1][key] = temp
            total += temp

 
    return total
    
    

def part2(data,iterations):
    total = 0
    
    dico = {}
    total_time = 0
    my_dico = {}
    
    for i in range(iterations):
        new_data = []
        index = iterations-i-1
        
        my_dico[index] = {}

        
        for k in data:
            start_time = time.time()
            if k in my_dico[index]:
                total += my_dico[index][k]
                continue
            try:
                length = iterate_dico(dico,k,index,my_dico)
            except ValueError:
                length = 0
            total_time += time.time() - start_time
            if length > 0:
                total += length
                my_dico[k] = length
                continue

            elif k in dico:
                new_data += dico[k]

            elif k == "0":
                dico[k] = ["1"]
                new_data.append("1")

            elif len(k)%2 ==0:
                dico[k] = [k[:len(k)//2],str(int(k[len(k)//2:]))]
                new_data.append(k[:len(k)//2])
                new_data.append(str(int(k[len(k)//2:])))
            else:
                dico[k] = [str(int(k)*2024)]
                new_data.append(str(int(k)*2024))
        data = new_data
        #print(dico)
    print(len(data))
    print(total_time)
    return total + len(data)


           


def solve(file_path: str):
    data = get_input(file_path)
    result = part2(data,75)
    print(f"Result: {result}")

solve("day11/input.txt")