def get_input(input_file):
    with open(input_file) as f:
        data = f.read()

    rules,sequences = data.split("\n\n")
    return rules,sequences

def process_rules(rules):
    rules = rules.split("\n")
    rules_dict = {}
    for rule in rules:
        rule = rule.split("|")
        if rule[0] in rules_dict:
            rules_dict[rule[0]].append(rule[1])
        else:
            rules_dict[rule[0]] = [rule[1]]
    return rules_dict

def process_sequence(sequence):
    sequence = sequence.split("\n")
    sequence = [line.split(",") for line in sequence]
    return sequence

def get_reverse_rules(rules):
    reverse_rules = {}
    for key in rules:
        for value in rules[key]:
            if value in reverse_rules:
                reverse_rules[value].append(key)
            else:
                reverse_rules[value] = [key]
    return reverse_rules

def is_valid(elems,processed,sequence):
    for elem in elems:
        if elem not in processed and elem in sequence:
            return False
    return True
    

def check_sequence(sequence,rules):
    processed = []
    reverse_rules = get_reverse_rules(rules)
    for elem in sequence:

        if elem in reverse_rules and not is_valid(reverse_rules[elem],processed,sequence):
            return False
        processed.append(elem)
    return True

def fix_sequence(sequence,rules):
    fixed_sequence = []
    original_sequence = sequence.copy()
    seq = sequence.copy()
    reverse_rules = get_reverse_rules(rules)
    while len(seq) > 0:
        for i,elem in enumerate(seq):
            if (elem in reverse_rules and is_valid(reverse_rules[seq[i]],fixed_sequence,original_sequence)) or (elem not in reverse_rules):
                fixed_sequence.append(elem)
                sequence.remove(elem)
        seq = sequence.copy()
    return fixed_sequence

def solve2(input_file):
    rules,sequences = get_input(input_file)
    rules = process_rules(rules)
    sequences = process_sequence(sequences)
    total = 0
    for sequence in sequences:
        if not check_sequence(sequence,rules):
            fixed_sequence = fix_sequence(sequence,rules)
            total+=int(fixed_sequence[len(fixed_sequence)//2])

    print(f"Total = {total}")

def solve(input_file):
    rules,sequences = get_input(input_file)
    rules = process_rules(rules)
    sequences = process_sequence(sequences)
    total = 0
    # check_sequence(sequences[4],rules)
    for sequence in sequences:
        if check_sequence(sequence,rules):
            middle = len(sequence)//2 
            total += int(sequence[middle])

    print(f"Total = {total}")




solve2("day5/input.txt")