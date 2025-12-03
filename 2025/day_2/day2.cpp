#include <iostream>
#include <string>
#include <utility>
#include <vector>
#include <cmath>
#include "../utils/stringHelper.cpp"
#include "../utils/Reader.cpp"

long process_id(const std::string& id) {
    int id_size = id.size();
    long id_value = std::stol(id);
    
    for (int i = 1; i < id_size; i++) {
        long sum_pattern = 0;
        std::string pattern_str = id.substr(id_size - i);
        if (pattern_str[0] == '0') {
            continue; // Skip patterns that start with '0' to avoid leading zero issues
        }
        long pattern = std::stol(pattern_str);
        
        for (int j=0;j<id_size;j+=i){
            sum_pattern += (std::pow(10,(j)) * pattern);
        }
        if (sum_pattern == id_value) {
            std::cout << "Found pattern for ID " << id << ": " << id_value << std::endl;
            return id_value;
        }
    }

    return 0;

    
}


long process_range(const std::string& range) {
    std::vector<std::string> ids = split(range, '-');
    long total = 0;
    std::string first_id = ids[0];
    std::string last_id = ids[1];
    long lower_bound = std::stol(first_id);
    long upper_bound = std::stol(last_id);
    for (long id = lower_bound; id <= upper_bound; id++) {
        total += process_id(std::to_string(id));
    }
    return total;
    
}

int main(int argc, char* argv[]) {
    std::string file = argv[1];
    Reader reader = Reader(file);
    std::string input = reader.readLine();
    long answer = 0;
    std::vector<std::string> id_ranges = split(input,',');
    for (const std::string& range : id_ranges) {
        std::cout << "Processing range: " << range << std::endl;
        answer += process_range(range);
        
    }
    std::cout << "Total patterns found: " << answer << std::endl;
}