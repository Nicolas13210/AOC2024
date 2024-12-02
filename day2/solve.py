import pandas as pd
import numpy as np
import time

def get_input(input_path):
    safe = []
    
    with open(input_path, "r") as f:
        lines = f.readlines()
    for line in lines:
        safe.append(is_dampener_safe([int(x) for x in line.split(" ")]))
    return safe

def is_dampener_safe(row):
    first_try = is_safe(row)
    if first_try:
        return True
    for k in range(len(row)):
        copy_row = row.copy()
        copy_row.pop(k)
        if is_safe(copy_row):
            return True
    return False

def is_safe(row):
    if sorted(row) != row and sorted(row, reverse=True) != row:
        return False
    for k in range(len(row)-1):
        if abs(row[k] - row[k+1]) < 1 or abs(row[k] - row[k+1]) > 3:
            return False
    return True

def exo1(input_path):
    start = time.time()
    df = get_input(input_path)
    end = time.time()
    duration = end - start
    print(f"Duration: {duration}")
    print(df.count(True))

exo1("day2/input.txt")