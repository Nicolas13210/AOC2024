#include <iostream>
#include <string>
#include <utility>
#include <vector>
#include <cmath>
#include <regex>
#include <map>
#include "../utils/stringHelper.cpp"
#include "../utils/Reader.cpp"


int update_start_position(std::string line,std::map<int, std::string> number_position, const int max_size, const int prev_start_pos, const int current_number )
{
    std::string string_num = std::to_string(current_number);
    int current_pos = 1;
    for (auto const& pair : number_position) {
        if (pair.second == string_num) {
            // int remaining_char = number_position.size() - current_pos;
            int space_remaining = line.size() - max_size + current_pos;
            if (pair.first + 1 <= space_remaining) {
                return pair.first + 1;
            } 
        }
    }
    return prev_start_pos;
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
                std::cout << "Found number: " << combined_number_str << std::endl;
                long long number = std::stol(combined_number_str);
                return number;
            }
        
        }
        start_position = update_start_position(line, number_position, num_size, start_position, j);
        std::cout << "Updated start position to: " << start_position << " after iteration " << j << std::endl;
    }

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