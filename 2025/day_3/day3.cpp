#include <iostream>
#include <string>
#include <utility>
#include <vector>
#include <cmath>
#include <regex>
#include <map>
#include "../utils/stringHelper.cpp"
#include "../utils/Reader.cpp"


int get_start_position(int max_size, std::string line) {
    for (int i=9;i>-1;i--){
        std::regex pattern (std::to_string(i) );
        std::sregex_iterator it(line.begin(), line.end(), pattern);
        std::sregex_iterator end;
        while (it!=end) {
            int candidate = it->position();
            if (candidate < line.size() - max_size) {
                return candidate;
            }
        }
    }
    return 0;
}

long long process_line_rec(std::string line,int num_size,int position, std::string current_number) {
    if (current_number.size() == num_size) {
        return std::stol(current_number);
    }
    if (position >= line.size() - (num_size - current_number.size())+1) {
        return 0;
    }
    return std::max(
        process_line_rec(line,num_size,position+1,current_number),
        process_line_rec(line,num_size,position+1,current_number + line[position])
    );
}

long long process_line(std::string line, int num_size) {
    int start_position = get_start_position(num_size, line);
    long long result = process_line_rec(line, num_size, start_position, "");
    std::cout << "Processed line: " << line << " Result: " << result << std::endl;

    return result;
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