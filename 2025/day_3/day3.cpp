#include <iostream>
#include <string>
#include <utility>
#include <vector>
#include <cmath>
#include <regex>
#include <map>
#include "../utils/stringHelper.cpp"
#include "../utils/Reader.cpp"

long process_line(std::string line, int num_size) {
    std::map<int, std::string> number_position;
    int start_position = 0;
    for (int j=9;j>-1;j--){
        std::regex pattern (std::to_string(j) );
        std::sregex_iterator it(line.begin() + start_position, line.end(), pattern);
        std::sregex_iterator end;
        while (it != end) {
            std::smatch match = *it;
            int actual_position = match.position() + start_position;
            number_position[actual_position] = std::to_string(j);
            if (number_position.size() == num_size) {
                std::string combined_number_str = "";
                for (const auto& pair : number_position) {
                    combined_number_str += pair.second;
                }
                std::cout << "Found number: " << combined_number_str << std::endl;
                long number = std::stol(combined_number_str);
                return number;
            }
            ++it;
        
        }
        if (number_position.size() < num_size && !number_position.empty()) {
            start_position = number_position.begin()->first + 1;
            if (start_position > line.size() - num_size + 1) {
                start_position = 0;
            }
        }
    }
    return 0;
}

int main(int argc, char* argv[]) {
    std::string file = argv[1];
    int num_size = std::stoi(argv[2]);
    Reader reader = Reader(file);
    int num_lines = reader.getLineCount();
    std::string line;
    long total = 0;

    for (int i=0;i<num_lines;i++)
    {
        line = reader.readLine();
        total += process_line(line,num_size);
    }

   

    std::cout << "Total: " << total << std::endl;
    return 0;
}