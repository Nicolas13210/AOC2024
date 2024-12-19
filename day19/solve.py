from functools import lru_cache 
import time
def get_input(input_file: str):
    with open(input_file, "r") as file:
        available_patterns,patterns = file.read().split("\n\n")
        return available_patterns.split(","),patterns.split("\n")

@lru_cache
def has_match(available, pattern):
    available_list = list(available)
    if pattern == "":
        return 1
    total = 0
    for elem in available_list:
        if pattern.endswith(elem):
            total += has_match(available, pattern[:-len(elem)])
         
    return total
    
    
def pattern_is_valid(available,pattern):
    return has_match(available,pattern)


    
def solve(input_file: str):
    print("here")
    available,patterns = get_input(input_file)
    available = tuple([elem.strip() for elem in available])
    patterns = [elem.strip() for elem in patterns]
    total= 0 
    start = time.time()

    for pattern in patterns:    
        total += pattern_is_valid(available,pattern)
            
    end = time.time()
    print(f"Time: {end-start}")
    print(f"Total valid patterns: {total}") 





solve("day19/input.txt")