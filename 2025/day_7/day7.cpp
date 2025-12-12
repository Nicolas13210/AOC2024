#include <iostream>
#include <string>
#include <utility>
#include <vector>
#include <cmath>
#include <regex>
#include <map>
#include <algorithm>
#include "../utils/stringHelper.cpp"
#include "../utils/Reader.cpp"
#include <unordered_set>

std::string get_nth_line(const std::string& content, int n) {
    std::istringstream stream(content);
    std::string line;
    for (int i = 0; i <= n; ++i) {
        if (!std::getline(stream, line)) {
            return "";
        }
    }
    return line;
}

void print_vector(const std::vector<int>& vec) {
    for (const auto& val : vec) {
        std::cout << val << " ";
    }
    std::cout << std::endl;
}

void print_set(const std::unordered_set<int>& vec) {
    for (const auto& val : vec) {
        std::cout << val << " ";
    }
    std::cout << std::endl;
}

void get_beam_start(const std::string& line, std::unordered_set<int>& beam_position) {
    for (size_t i = 0; i < line.size(); ++i) {
        if (line[i] == 'S') {
            beam_position.insert(static_cast<int>(i));
        }
    }
}

long long process_line(const std::string& line, std::unordered_set<int>& beam_position) {
    long long score = 0;
    // std::cout << "Processing line: " << line << std::endl;
    // std::cout << "Current beam positions: ";
    // print_set(beam_position);
    // std::cout << std::endl;
    // Avoid modifying the vector while iterating. Copy current positions,
    // then rebuild beam_position from the copy.
    std::unordered_set<int> current = beam_position;
    for (int pos : current) {
        if (pos < 0 || pos >= static_cast<int>(line.size())) {
            continue;
        }
        if (line[pos] == '^') {
            if (pos - 1 >= 0){
                beam_position.insert(pos - 1);
            }
            if (pos + 1 < static_cast<int>(line.size())) {
                beam_position.insert(pos + 1);
            }
            beam_position.erase(pos);
            score++;
        }
    }
    return score;
}

long long process_input(Reader& reader) {
    long long total_score = 0;
    std::unordered_set<int> beam_position;
    int lineCount = reader.getLineCount();
    std::string first_line = reader.readLine();
    get_beam_start(first_line, beam_position);
    for (int i = 1; i < lineCount; ++i) {
        std::string line = reader.readLine();
        total_score += process_line(line, beam_position);
    }
    return total_score;
}

// Use pre-split lines and a long long cache value to avoid copying and overflow.
long long get_rec_path(const std::vector<std::string>& lines, int beam_position, int line_idx,
                       std::map<std::pair<int,int>, long long>& cache) {
    std::pair<int,int> key = {beam_position, line_idx};
    auto it = cache.find(key);
    if (it != cache.end()) {
        return it->second;
    }

    // If we've gone past the last line, there's one successful path
    if (line_idx >= static_cast<int>(lines.size())) {
        return 1;
    }

    const std::string& line = lines[line_idx];
    long long total_paths = 0;
    if (beam_position >= 0 && beam_position < static_cast<int>(line.size()) && line[beam_position] == '^') {
        if (beam_position - 1 >= 0) {
            total_paths += get_rec_path(lines, beam_position - 1, line_idx + 1, cache);
        }
        if (beam_position + 1 < static_cast<int>(line.size())) {
            total_paths += get_rec_path(lines, beam_position + 1, line_idx + 1, cache);
        }
    } else {
        total_paths = get_rec_path(lines, beam_position, line_idx + 1, cache);
    }

    cache[key] = total_paths;
    return total_paths;
}

long long process_input_part_2(Reader& reader) {
    std::map<std::pair<int,int>, long long> cache_key;
    long long total_score = 0;
    std::unordered_set<int> beam_position;
    int lineCount = reader.getLineCount();
    std::string first_line = reader.readLine();
    get_beam_start(first_line, beam_position);
    int start_beam = *(beam_position.begin());
    std::string content = reader.readAll();
    // Pre-split content into lines so recursive calls don't reparse/copy the whole string
    std::istringstream iss(content);
    std::vector<std::string> lines;
    std::string l;
    while (std::getline(iss, l)) lines.push_back(l);

    total_score = get_rec_path(lines, start_beam, 1, cache_key);

    return total_score;
}

int main(int argc, char* argv[]) {

    std::string file = argv[1];
    Reader reader(file);
    long long result = process_input_part_2(reader);
    std::cout << "Final result: " << result << std::endl;

}