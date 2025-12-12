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
    Point() : x(0), y(0) {}
    Point(int x, int y) : x(x), y(y){}
    int x, y;
    bool operator<(const Point& other) const {
        if (x != other.x) return x < other.x;
        return y < other.y;
    }
    bool operator==(const Point& other) const {
        return x == other.x && y == other.y;
    }
    std::string toString() const {
        return "(" + std::to_string(x) + "," + std::to_string(y) + ")";
    }
};

long long getAreaRectangle(const Point& p1, const Point& p2) {
    long long width = std::abs(p2.x - p1.x) + 1;
    long long height = std::abs(p2.y - p1.y) + 1;
    return width * height;
}


std::vector<Point> parse_input(Reader& reader) {
    std::vector<Point> points;
    int line_count = reader.getLineCount();
    for (int i = 0; i < line_count; ++i) {
        std::string line = reader.readLine();
        std::vector<std::string> parts = split(line, ',');
        Point p1(std::stoi(parts[0]), std::stoi(parts[1]));
        points.push_back(p1);
    }
    return points;
}

long long getMaxArea(std::vector<Point>& points) {
    long long max_area = 0;
    int n = points.size();
    for (int i = 0; i < n; ++i) {
        for (int j = i + 1; j < n; ++j) {
            long long area = getAreaRectangle(points[i], points[j]);
            if (area > max_area) {
                max_area = area;
            }
        }
    }
    return max_area;
}

int main(int argc, char* argv[]) {
    std::string file = argv[1];
    Reader reader = Reader(file);
    std::vector<Point> points = parse_input(reader);
    long long max_area = getMaxArea(points);
    std::cout << "Max Area: " << max_area << std::endl;
    return 0;
}