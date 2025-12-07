from functools import lru_cache
def get_input(input_file):
    with open(input_file, 'r') as f:
        data = [int(line.strip()) for line in f.read().splitlines()]
    return data


def prune(number):
    return number % 16777216

def mix(number,value):
    return number ^ value

def first_step(number):
    temp = number << 6
    number = mix(number,temp)
    number = prune(number)
    return number


def second_step(number):
    temp = number>>5
    number = mix(number,temp)
    number = prune(number)
    return number


def third_step(number):
    temp = number << 11
    number = mix(number,temp)
    number = prune(number)
    return number

@lru_cache(maxsize=None)
def get_next_value(number):
    number = first_step(number)
    number = second_step(number)
    number = third_step(number)
    return number

def get_secret(number,iterations):
    changes = []
    initial = int(str(number)[-1])

    for i in range(iterations):
        number = get_next_value(number)
        count = int(str(number)[-1])
        changes.append((count,count-initial))
        initial = count
        
    return changes

def get_sequences(changes):
    gain = {}
    for k in range(len(changes)-4):
        sequence = tuple([changes[k+i][1] for i in range(4)])
        if sequence not in gain:
            gain[sequence] = changes[k+3][0]
        else:
            continue

    return gain
        


def solve(input_file,iterations):
    data = get_input(input_file)
    total = 0
    global_gain = {}
    for number in data:
        secrets = get_secret(number,iterations)
        gain = get_sequences(secrets)
        for k,v in gain.items():
            if k not in global_gain:
                global_gain[k] = v
            else:
                global_gain[k] += v
    total = max(global_gain.values())
    print(f"Total: {total}")

solve("day22/input.txt",2000)