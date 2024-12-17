def get_input(input_file):
    with open(input_file, 'r') as file:
        return file.read().splitlines()

def preprocess(rule):
    objective = int(rule.split(":")[0])
    operands = [int(number) for number in rule.split(":")[1].strip().split(" ")]
    return objective, operands

def is_solvable(rule):
    objective, operands = preprocess(rule)
    solvable = rec_solve(objective, operands[1:],operands[0])
    answer = objective if solvable else 0
    return answer

def rec_solve(objective,operands, total ):
    if len(operands) == 0 and objective != total:
        return False

    if len(operands) == 0 and objective == total:
        return True

    first = operands[0]
    return rec_solve(objective, operands[1:], total + first) or rec_solve(objective, operands[1:], total * first) or rec_solve(objective, operands[1:], int(str(total) + str(first)))

    


def solve(input_file):
    rules = get_input(input_file)
    total = 0
    for rule in rules:
        total += is_solvable(rule)
    print(f"Total: {total}")
   

solve('day7/input.txt')