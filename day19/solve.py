def get_input(input_file: str):
    with open(input_file, "r") as file:
        available_patterns,patterns = file.read().split("\n\n")
        return available_patterns.split(","),patterns.split("\n")



def has_match(available,pattern,current_pattern):
    too_long = len(pattern) < len(current_pattern)
    lenght = len(current_pattern)
    temp_pattern = pattern[:lenght]
    mismatch = (temp_pattern != current_pattern) and lenght>0
   

    if  too_long or mismatch:
        return False
    
    if pattern == current_pattern:
        return True
    
    answer = False

    for i in range(len(available)):
        temp_ans = current_pattern + available[i]
        if not temp_ans not in available:
            available.append(temp_ans)
        answer = answer or has_match(available, pattern, temp_ans)
    return answer    
    
def pattern_is_valid(available,pattern):
    available = list(set(available))
    new_string = ""
    return has_match(available,pattern,new_string)

def get_minimal_legnth(patterns):
    return min([len(elem) for elem in patterns])

def get_all_minimal_patterns(available,current_pattern,minimum_length):
    if len(current_pattern) >= minimum_length:
        return 
    last_key = sorted(list(available.keys()))[-1]
    available[last_key+1] = []
    for i in range(len(available[last_key])):
        temp = current_pattern + available[last_key][i]
        print(temp)
        if not temp in available[last_key+1]:
            available[last_key+1].append(temp)
        get_all_minimal_patterns(available,temp,minimum_length)

    
def solve(input_file: str):
    available,patterns = get_input(input_file)
    available = {1:[elem.strip() for elem in available]}
    patterns = [elem.strip() for elem in patterns]
    total = 0
    minimal_length = get_minimal_legnth(patterns)
    get_all_minimal_patterns(available,"",minimal_length)
    print(available)
    """for pattern in patterns:
        if pattern_is_valid(available,pattern):
            total += 1
    print(f"Total valid patterns: {total}")   """ 






solve("day19/example.txt")