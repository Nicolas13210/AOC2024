#include <iostream>
#include <string>
#include <utility>
#include <vector>
#include <cmath>
#include <regex>
#include <map>
#include "../utils/stringHelper.cpp"
#include "../utils/Reader.cpp"
#include "../utils/SortedList.cpp"

bool has_intersection(const std::pair<long long,long long>& a, const std::pair<long long,long long>& b) {
    return (a.first <= b.second && b.first <= a.second);
}
std::vector<std::string> splitString(const std::string& str, const std::string& delimiter) {
    std::vector<std::string> result;
    size_t start = 0;
    size_t end = str.find(delimiter);
    
    while (end != std::string::npos) {
        result.push_back(str.substr(start, end - start));
        start = end + delimiter.length();
        end = str.find(delimiter, start);
    }
    
    // Add the last segment
    result.push_back(str.substr(start));
    return result;
}

class SortedIntervalList {
public:
    SortedIntervalList() = default; 
    bool contains(long long value) const {
        for (const auto& interval : intervals) {
            if (value >= interval.first && value <= interval.second) {
                return true;
            }
        }
        return false;
    }

    long long get_length() const {
        long long total_length = 0;
        for (const auto& interval : intervals) {
            total_length += (interval.second - interval.first + 1);
        }
        return total_length;
    }

    void insert(const std::pair<long long,long long>& interval) {
        if (intervals.empty()) {
            intervals.push_back(interval);
            return;
        }

        auto it = intervals.begin();
        while (it != intervals.end() && it->first < interval.first) {
            ++it;
        }

        long long new_start = interval.first;
        long long new_end = interval.second;

        // Merge with previous if overlapping
        if (it != intervals.begin()) {
            auto prev = it - 1;
            if (has_intersection(*prev, interval)) {
                new_start = std::min(prev->first, new_start);
                new_end = std::max(prev->second, new_end);
                it = intervals.erase(prev); // it now points to the element after prev
            }
        }

        // Merge with subsequent overlapping intervals
        while (it != intervals.end() && has_intersection(*it, std::pair<long long,long long>{new_start, new_end})) {
            new_start = std::min(new_start, it->first);
            new_end = std::max(new_end, it->second);
            it = intervals.erase(it);
        }

        intervals.insert(it, {new_start, new_end});
    }
    void print() const {
        for (const auto& interval : intervals) {
            std::cout << "[" << interval.first << ", " << interval.second << "] ";
        }
        std::cout << std::endl;
    }
private:
    std::vector<std::pair<long long,long long>> intervals;
};


SortedIntervalList parse_interval(const std::string& content) {
    SortedIntervalList sorted_intervals;
    std::regex pattern(R"((\d+)-(\d+))");
    std::vector<std::string> lines = splitString(content, "\n");
    
    for (const auto& line : lines) {
        std::smatch match;
        if (std::regex_search(line, match, pattern)) {
            long long start = std::stoll(match[1].str());
            long long end = std::stoll(match[2].str());
            sorted_intervals.insert({start, end});
        }
    }
    return sorted_intervals;
}

SortedList parseId(const std::string& content) {
    SortedList sorted_ids;
    std::regex pattern(R"((\d+))");
    std::vector<std::string> lines = splitString(content, "\n");
    
    for (const auto& line : lines) {
        std::smatch match;
        if (std::regex_search(line, match, pattern)) {
            long long id = std::stoll(match[1].str());
            sorted_ids.insert(id);
        }
    }
    return sorted_ids;
}







void parse_input(Reader& reader, SortedIntervalList& intervals, SortedList& ids) {
    std::string input = reader.readAll();
    std::vector<std::string> lines = splitString(input, "\n\n");
    intervals = parse_interval(lines[0]);
    ids = parseId(lines[1]);
}

long long get_id_fresh(SortedIntervalList& intervals, SortedList& ids) {
    long long total_ids = 0;
    // Part 1
    // for (long long id:ids) {
    //     if (intervals.contains(id) ) {
    //         total_ids += 1;
    //     }
    // }
    //Part 2
    total_ids = intervals.get_length();
    return total_ids;
}


int main(int argc, char* argv[]) {
    SortedIntervalList intervals;
    SortedList ids;
    std::string file = argv[1];
    Reader reader = Reader(file);
    parse_input(reader, intervals, ids);
    // std::cout << "Intervals: ";
    // intervals.print();
    // std::cout << "IDs: ";
    // ids.print();
    long long total = get_id_fresh(intervals, ids);
    std::cout << "Total fresh IDs: " << total << std::endl;
    return 0;
}