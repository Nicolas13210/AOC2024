import numpy as np

def get_all_keys(input_file):
    with open(input_file) as f:
        keys = f.read().strip().split("\n\n")
        keys = [key.split("\n") for key in keys]
        keys = [[[k for k in line] for line in key]for key in keys]
    return np.array(keys)

def separate_keys_locks(keys):
    locks = []
    final_keys = []
    for k in keys:
        if "." in k[0]:
            final_keys.append(k)
        else:
            locks.append(k)
    return final_keys,locks

def get_key(key):
    key_repr = []
    for i in range(len(key[0])):
        column = [key[a][i] for a in range(len(key)) if key[a][i] == "#"]
        key_repr.append(len(column)-1)
    return np.array(key_repr)
        
def can_fit(key,lock,max_height):
    key_repr = get_key(key)
    lock_repr = get_key(lock)
    fit = key_repr + lock_repr

    for k in fit:
        if k > max_height:
            return False
    
    return True


def solve(input_file):
    keys = get_all_keys(input_file)
    keys,locks = separate_keys_locks(keys)
    max_height = len(keys[0])-2
    total = 0
    for lock in locks:
        for key in keys:
            if can_fit(key,lock,max_height):
                total += 1
    print(f"Total: {total}")

solve("day25/input.txt")