#include <iostream>
#include <string>
#include <utility>
#include "../utils/Reader.cpp"

std::pair<int, int> make_rotations(const std::string& line, int init_value) {
    int value = init_value;
    char direction = line[0];
    int rotations = std::stoi(line.substr(1));
    int passages = 0;
    if (direction == 'L')
        value -= rotations;
    else if (direction == 'R')
        value += rotations;

    if (value == 0){
        passages +=1;
    }
    else if (value > 0) {
        passages += value / 100;
    } else {
        while (value <= 0) {
            value += 100;
            passages += 1;
        }
        if (init_value == 0) {
            passages -= 1;
        }
        
    }
    value = value % 100;

    return {value, passages};
}

int main(int argc, char* argv[]) {
    std::string file = argv[1];
    Reader reader = Reader(file);
    int line_count = reader.getLineCount();
    int init_value = 50;
    int password_part_1 = 0;
    int password_part_2 = 0;
    for (int i=0; i< line_count;i++){
        std::string line = reader.readLine();
        auto [new_value, passages] = make_rotations(line, init_value);
        init_value = new_value;
        password_part_2 += passages;
        if (init_value == 0) {
            password_part_1 += 1;
        }
        // std::cout << "After line " << line << ": Value = " << new_value << ", Passages = " << passages << ", Cumulative Password = " << password << std::endl;
    }

    std::cout << "Password Part 1: " << password_part_1 << std::endl;
    std::cout << "Password Part 2: " << password_part_2 << std::endl;
    return 0;
}