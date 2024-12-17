def get_input(file_name):
    with open(file_name) as f:
        return f.read().strip()
    
def part_one(data):
    check_str = ""
    checksum = 0
    index = 0
    id_start = 0
    id_end = len(data)//2
    data = data if len(data)%2 != 0 else data[:-1]
    index_end = len(data)-1
    num_end = int(data[-1])
    i = 0
    while(i < index_end):
        num = int(data[i])
        if i%2 != 1:
            for k in range(0,num):
                check_str +=str(id_start)
                checksum += id_start * index
                index += 1
            id_start+=1
        else:
            for k in range(0,num):
                if num_end == 0:
                    index_end -= 2
                    num_end = int(data[index_end])
                    id_end -= 1
                check_str += str(id_end)
                checksum += id_end * index
                index += 1
                num_end -= 1
        i += 1
    while(num_end > 0):
        check_str += str(id_end)
        checksum += id_end * index
        index += 1
        num_end -= 1
    print(f"id_end: {id_end}")
    return checksum

def create_id_size(data):
    occupied_sizes = data[::2]
    id_sizes = {i:int(occupied_sizes[i]) for i in range(len(occupied_sizes))}
    return id_sizes

def part_two(data):
    id_size = create_id_size(data)
    check_str = ""
    checksum = 0
    index = 0
    list_pos = 0
    start_id = 0
    removed = {}
    while(len(id_size) > 0):
        if list_pos %2 == 0 and start_id in id_size:
            current_size = int(start_id)
            for i in range(id_size[current_size]):
                check_str += str(start_id)
                checksum += start_id * index
                index += 1
            removed[start_id] = id_size[start_id]
            del id_size[start_id]
            start_id += 1
        elif list_pos %2 == 0 and start_id not in id_size:
            index += removed[start_id]
            start_id += 1
        else:
            free_size = int(data[list_pos])
            reverse_sorted = sorted(id_size.keys(),reverse=True)
            i = 0
            while(i<len(reverse_sorted)):
                current_id = reverse_sorted[i]
                if id_size[current_id]<= free_size:
                    for k in range(id_size[current_id]):
                        check_str += str(current_id)
                        checksum += current_id * index
                        index += 1
                    free_size -= id_size[current_id]
                    removed[current_id] = id_size[current_id]
                    del id_size[current_id]
           
                i+=1
            index += free_size
        list_pos += 1
    return checksum


        

    
def solve(input_file):
    data = get_input(input_file)
    total = part_two(data)
    print(f"Total: {total}")
    
solve('day9/input.txt')