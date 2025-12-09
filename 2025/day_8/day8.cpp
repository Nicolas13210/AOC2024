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



class Point {
public:
    Point() : x(0), y(0), z(0) {}
    Point(int x, int y, int z) : x(x), y(y), z(z) {}
    int x, y, z;
    bool operator<(const Point& other) const {
        if (x != other.x) return x < other.x;
        if (y != other.y) return y < other.y;
        return z < other.z;
    }
    bool operator==(const Point& other) const {
        return x == other.x && y == other.y && z == other.z;
    }
    std::string toString() const {
        return "(" + std::to_string(x) + "," + std::to_string(y) + "," + std::to_string(z) + ")";
    }
};

float get_euclidean_distance(const Point& p1, const Point& p2) {
    return std::sqrt(std::pow(p1.x - p2.x, 2) + std::pow(p1.y - p2.y, 2) + std::pow(p1.z - p2.z, 2));
}

std::vector<std::pair<Point,Point>> parse_input(Reader& reader, int max_pairs) {
    std::cout << "Parsing input points and finding closest pairs..." << std::endl;
    std::map<std::pair<Point,Point>,float> distance_map;
    std::vector<std::pair<Point,Point>> point_pairs;
    std::vector<Point> points;
    int num_lines = reader.getLineCount();
    for (int i = 0; i < num_lines; ++i) {
        std::string line = reader.readLine();
        std::vector<std::string> parts = split(line, ',');
        int x = std::stoi(parts[0]);
        int y = std::stoi(parts[1]);
        int z = std::stoi(parts[2]);
        Point p1(x, y, z);
        for (Point p2 : points) {
            float dist = get_euclidean_distance(p1, p2);
            distance_map[{p1, p2}] = dist;
        }
        points.push_back(p1);
    }
    // replace the SortedList declaration with this code to get the map sorted by value
    std::vector<std::pair<std::pair<Point,Point>, float>> entries;
    entries.reserve(distance_map.size());
    for (const auto& kv : distance_map) {
        entries.push_back(kv); // kv.first is pair<Point,Point>, kv.second is distance
    }

    // sort by the mapped value (distance)
    std::sort(entries.begin(), entries.end(),
              [](const auto& a, const auto& b){ return a.second < b.second; });

    // build result vector of pairs (optionally limit to max_pairs if > 0)
    std::vector<std::pair<Point,Point>> result;
    size_t limit =  entries.size();
    result.reserve(limit);
    for (size_t i = 0; i < limit; ++i) {
        result.push_back(entries[i].first);
    }

    // return here because the rest of the original function assumes a different helper type
    return result;
}

void merge_groups(std::vector<std::vector<Point>>& groups) {
    bool merged;
    do {
        merged = false;
        for (size_t i = 0; i < groups.size(); ++i) {
            for (size_t j = i + 1; j < groups.size(); ++j) {
                for (const auto& point : groups[i]) {
                    if (std::find(groups[j].begin(), groups[j].end(), point) != groups[j].end()) {
                        groups[i].insert(groups[i].end(), groups[j].begin(), groups[j].end());
                        groups.erase(groups.begin() + j);
                        {
                            std::map<Point,bool> seen;
                            std::vector<Point> unique_points;
                            unique_points.reserve(groups[i].size());
                            for (const auto& pt : groups[i]) {
                                if (seen.find(pt) == seen.end()) {
                                    seen[pt] = true;
                                    unique_points.push_back(pt);
                                }
                            }
                            groups[i].swap(unique_points);
                        }
                        merged = true;
                        break;
                    }
                }
                if (merged) break;
            }
            if (merged) break;
        }
    } while (merged);
}


bool add_pair_to_groups(const std::pair<Point,Point>& point_pair, std::vector<std::vector<Point>>& groups, int num_points) {
    
    
    Point p1 = point_pair.first;
    Point p2 = point_pair.second;
    bool found_group = false;
    for (auto& group : groups) {
        if (std::find(group.begin(), group.end(), p1) != group.end() ||
            std::find(group.begin(), group.end(), p2) != group.end()) {
            if (std::find(group.begin(), group.end(), p1) == group.end()) {
                group.push_back(p1);
            }
            if (std::find(group.begin(), group.end(), p2) == group.end()) {
                group.push_back(p2);
            }
            found_group = true;
            merge_groups(groups);
            if (groups.size() == 1) {
                if (groups[0].size() == num_points){
                    return true; // all points are grouped
                }
            }
            break;
        }
    }
    if (!found_group) {
        groups.push_back({p1, p2});
    }
    return false;
}

int group_points_by_closest_pair(const std::vector<std::pair<Point,Point>>& point_pairs, int num_points) {
    std::vector<std::vector<Point>> groups;
    for (const auto& pair : point_pairs) {
        bool is_merged = add_pair_to_groups(pair, groups, num_points);
        if (is_merged){
            return pair.first.x * pair.second.x;
        }
    }
    return -1;
}


int get_total_max(const std::vector<std::vector<Point>>& groups) {
    int top1 = 0, top2 = 0, top3 = 0;
    for (const auto& g : groups) {
        int sz = static_cast<int>(g.size());
        if (sz > top1) {
            top3 = top2;
            top2 = top1;
            top1 = sz;
        } else if (sz > top2) {
            top3 = top2;
            top2 = sz;
        } else if (sz > top3) {
            top3 = sz;
        }
    }
    return top1 * top2 * top3;
}
int get_total_size(const std::vector<std::vector<Point>>& groups) {
    int total_size = 0;
    for (const auto& group : groups) {
        total_size += group.size();
    }
    return total_size;
}
int main(int argc, char* argv[]) {
    std::string file = argv[1];
    int max_pairs = atoi(argv[2]);
    Reader reader = Reader(file);
    std::vector<std::pair<Point,Point>> point_pairs = parse_input(reader,max_pairs);
    // std::vector<std::vector<Point>> groups = group_points_by_closest_pair(point_pairs);
    int result = group_points_by_closest_pair(point_pairs,max_pairs);
    std::cout << "Result (first fully grouped pair product): " << result << std::endl;

    // int total_size = get_total_size(groups);
    // std::cout << "Total number of unique points: " << total_size << std::endl;
    // int max_group_size = get_total_max(groups);
    // std::cout << "Maximum group size: " << max_group_size << std::endl;

    return 0;
}