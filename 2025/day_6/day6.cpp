#include <iostream>
#include <string>
#include <utility>
#include <vector>
#include <cmath>
#include <regex>
#include <map>
#include "../utils/stringHelper.cpp"
#include "../utils/Reader.cpp"


std::vector<int> get_operands(const std::string& content, std::vector<std::string>& ops) {
    int first_pos = -1;
    std::vector<int> positions;
    std::regex re(R"((\+|\*))");
    std::sregex_iterator first{content.begin(), content.end(), re}, last;
    for (auto it=first; it != last; ++it) {
        std::string op = it->str();
        ops.push_back(op);
        size_t pos = it->position();
        if (first_pos == -1) {
            first_pos = static_cast<int>(pos);
        }
        positions.push_back(static_cast<int>(pos) - first_pos);

    }
    return positions;
}


void get_numbers(Reader& reader, std::vector<std::vector<std::string>>& nums, const std::vector<int>& positions) {
    int lineCount = reader.getLineCount();
    for (int i = 0; i < lineCount-1; ++i) {
        std::string line = reader.readLine();
        for (int j=0; j < positions.size()-1; ++j) {
            if (nums.size() <= j) {
                nums.push_back(std::vector<std::string>{});
            }
            int size = positions[j+1] - positions[j];
            std::string num_str = line.substr(positions[j], size );
            while(num_str.size() < size){
                num_str = num_str + " ";
            }
            nums[j].push_back(num_str);
        }
        std::string last_num_str = line.substr(positions.back());
        if (nums.size() <= positions.size()-1) {
            nums.push_back(std::vector<std::string>{});
        }
        nums[positions.size()-1].push_back(last_num_str);

    }
        
}

void rearrange_numbers(std::vector<std::string>& nums) {
    std::vector<std::string> rearranged;
    int size = nums[0].size();
    for (int i = 0; i < size; ++i) {
        std::string new_num;
        for (const auto& num_str : nums) {
            if (num_str[i] != ' ') {
                new_num += num_str[i];
            }
        }
        rearranged.push_back(new_num);
    }
 
    nums = rearranged;
}

void rearrange_all_numbers(std::vector<std::vector<std::string>>& nums) {
    for (auto& vec : nums) {
        rearrange_numbers(vec);
    }
}

int get_max_size(const std::vector<std::string>& nums) {
    int max_length = 0;
    for (const auto& str : nums) {
        if (str.length() > max_length) {
            max_length = str.length();
        }
    }
    return max_length;
}


long long get_total(const std::vector<std::vector<std::string>>& nums, std::vector<std::string>& ops) {
    long long total = 0;
    for (int idx = 0; idx < nums.size(); ++idx) {
        const auto& vec = nums[idx];
        long long sub_total = 0;
        for (const auto& str : vec) {
            if (str.empty()) {
                continue;
            }
            long long num = std::stoll(str);
            if (ops[idx] == "+") {
                sub_total += num;
            } else if (ops[idx] == "*") {
                if (sub_total == 0) {
                    sub_total = 1;
                }
                sub_total *= num;
            }
        }
        total += sub_total;
    }
    return total;
}

long long process_numbers(Reader& reader, const std::vector<std::string>& ops) {
    std::vector<long long> totalVector;
    std::regex re(R"(\d+)");
    int lineCount = reader.getLineCount();
    for (int i = 0; i < lineCount -1; ++i) {
        std::string line = reader.readLine();
        std::sregex_token_iterator first{line.begin(), line.end(), re, 0}, last;
        std::vector<std::string> nums_str{first, last};
        for (int j = 0; j < nums_str.size(); ++j) {
            long long num = std::stoll(nums_str[j]);
            if (j>= totalVector.size()) {
                totalVector.push_back(num);
            } else {
                if (ops[j] == "+") {
                    totalVector[j] += num;
                } else if (ops[j] == "*") {
                    totalVector[j] *= num;
                }
            }
        }
    }
    long long finalResult = 0;
    for (const auto& val : totalVector) {
        finalResult += val;
    }
    return finalResult;

}

int main(int argc, char* argv[]) {
    std::vector<std::vector<std::string>> numbers;
    std::vector<std::string> operands;
    std::string file = argv[1];
    Reader reader(file);
    std::string content = reader.readAll();
    std::vector<int> positions = get_operands(content, operands);
    get_numbers(reader, numbers,positions);
    rearrange_all_numbers(numbers);
    for (const auto& vec : numbers) {
        for (const auto& val : vec) {
            std::cout << val << " ";
        }
        std::cout << std::endl;
    }
    long long result = get_total(numbers, operands);
    std::cout << "Final result: " << result << std::endl;

}