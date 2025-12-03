import pandas as pd
import re

def get_input(input_file):
    with open(input_file, 'r') as file:
        data = file.read().splitlines()

    output = "".join(data)
    return output

def process_matches_1(matches):
    total = 0
    for match in matches:
        a, b = match.split(',')
        a, b = int(a), int(b)
        result = a * b
        total += result
    return total

def process_matches_2(matches):
    total = 0
    process = True
    for match in matches:
        print(match)
        if match[1] == "don't":
            process = False
        elif match[2] == "do":
            process = True
        elif process:
            a, b = match[0].split(',')
            a, b = int(a), int(b)
            result = a * b
            total += result
    print(total)

def solve(input_file):
    total = 0
    data = get_input(input_file)
    pattern = r"mul\((\d+,\d+)\)|(don't)|(do)"  
    matches = re.findall(pattern, data)
    process_matches_2(matches)

solve('day3/input.txt')
# solve('day3/example.txt')
