#include <iostream>
#include <string>
#include <utility>
#include <vector>
#include <cmath>
#include <regex>
#include <map>
#include "../utils/stringHelper.cpp"
#include "../utils/Reader.cpp"


int get_start_position(const std::map<int, std::string>& number_position, int line_size, int max_size) {
    if (number_position.empty()) {
        return 0;
    }
    if (number_position.begin()->first <= line_size - max_size) {
        return number_position.begin()->first;
    }
    return 0;
}

long long process_line(std::string line, int num_size) {
    std::map<int, std::string> number_position;
    int start_position = 0;
    for (int j=9;j>-1;j--){
        // std::cout << "Starting search for digit: " << j << " start position: " << start_position << std::endl;
        std::regex pattern (std::to_string(j) );
        std::sregex_iterator it(line.begin() + start_position, line.end(), pattern);
        std::sregex_iterator end;
        std::vector<std::smatch> matches;
        while(it!=end) {
            matches.push_back(*it);
            ++it;
        }
        for (auto rit = matches.rbegin(); rit != matches.rend(); ++rit) {
            std::smatch match = *rit;
            int actual_position = match.position() + start_position;
            number_position[actual_position] = std::to_string(j);
            if (number_position.size() == num_size) {
                std::string combined_number_str = "";
                for (const auto& pair : number_position) {
                    combined_number_str += pair.second;
                }
                long long number = std::stol(combined_number_str);
                return number;
            }
        
        }
        if (number_position.size() < num_size) {
            start_position = get_start_position(number_position, line.size() , num_size);
        }
    }
    // std::cout << "Could not find a number for line: " << line << std::endl;
    // if (!number_position.empty()) {
    //     for (const auto& pair : number_position) {
    //         std::cout << "Position: " << pair.first << " Digit: " << pair.second << std::endl;
    //     }
    // }
    std::cout << "No number found in line: " << line << std::endl;

    return 0;
}

int main(int argc, char* argv[]) {
    std::string file = argv[1];
    int num_size = std::stoi(argv[2]);
    Reader reader = Reader(file);
    int num_lines = reader.getLineCount();
    std::string line;
    long long total = 0;

    for (int i=0;i<num_lines;i++)
    {
        line = reader.readLine();
        total += process_line(line,num_size);
    }

   

    std::cout << "Total: " << total << std::endl;
    return 0;
}