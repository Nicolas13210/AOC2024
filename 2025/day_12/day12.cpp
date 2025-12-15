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

class Shape {
    public:
    Shape() = default;
    Shape(std::vector<std::vector<bool>> cells) : cells(cells), id(-1) {}
    Shape(std::string description) {
        std::vector<std::string> parts = split(description, ':');
        id = std::stoi(parts[0]);
        std::string shape_description = parts[1];
        std::vector<std::string> rows = split(shape_description, '\n');
        for (const std::string& row : rows) {
            if (row.empty()) continue;
            std::vector<bool> cell_row;
            for (char c : row) {
                cell_row.push_back(c == '#');
            }
            cells.push_back(cell_row);
        }
    }

    Shape getRotated(int angle) const {
        switch (angle) {
            case 0:
                return *this;
            case 1:
                return rotate90();
            case 2:
                return rotate180();
            case 3:
                return rotate270();
            default:
                throw std::invalid_argument("Angle must be a multiple of 90");
        }
    }

    int getId() const {
        return id;
    }

    std::vector<std::vector<bool>> getCells() const {
        return cells;
    }

    std::string toString() const {
        return getShapeString();
    }




    private:
    std::string getShapeString() const {
        std::string shape_str;
        for (const auto& row : cells) {
            for (bool cell : row) {
                shape_str += cell ? '#' : '.';
            }
            shape_str += '\n';
        }
        return shape_str;
    } 

    Shape rotate90() const {
        size_t rows = cells.size();
        size_t cols = cells[0].size();
        std::vector<std::vector<bool>> rotated(cols, std::vector<bool>(rows, false));
        for (size_t r = 0; r < rows; ++r) {
            for (size_t c = 0; c < cols; ++c) {
                rotated[c][rows - 1 - r] = cells[r][c];
            }
        }
        return Shape(rotated);
    }

    Shape rotate180() const {
        Shape rotated = rotate90();
        return rotated.rotate90();
    }

    Shape rotate270() const {
        Shape rotated = rotate180();
        return rotated.rotate90();
    }

    std::vector<std::vector<bool>> cells;
    int id;

};

class Region {
    public:
    Region() = default;
    Region(std::string description) {
        std::vector<std::string> parts = split(description,":");
        std::vector<std::string> size_parts = split(parts[0],'x');
        size = {std::stoi(size_parts[0]), std::stoi(size_parts[1])};
        std::vector<std::string> shape_amount_parts = split(parts[1],' ');
        for (const std::string& amt_str : shape_amount_parts) {
            if (amt_str.empty()) continue;
            shape_amounts.push_back(std::stoi(amt_str));
        }
    }
    std::pair<int,int> getSize() const {
        return size;
    }
    std::vector<int> getShapeAmounts() const {
        return shape_amounts;
    }

    std::string toString() const {
        std::string region_str = "Size: " + std::to_string(size.first) + "x" + std::to_string(size.second) + "\nShapes: ";
        for (int amt : shape_amounts) {
            region_str += std::to_string(amt) + " ";
        }
        return region_str;
    }

    private:
    std::pair<int, int> size;
    std::vector<int> shape_amounts;

};

void getShapes(std::vector<std::string> shape_descriptions, std::map<int, Shape>& shapes) {
    for (const std::string& desc : shape_descriptions) {
        std::cout << "Processing shape description:\n" << desc << std::endl;
        Shape shape(desc);
        shapes[shape.getId()] = shape;
    }
}

int processRegion(const std::string& region, const std::map<int, Shape>& shapes) {
    int result = 0;
    Region reg(region);
    std::cout << "Processing region: " << reg.toString() << std::endl;
    return result;
}

long long processRegions(const std::string& regions_description, const std::map<int, Shape>& shapes) {
    long long result = 0;
    std::vector<std::string> regions = split(regions_description, "\n");
    for(std::string region : regions) {
        if (region.empty()) continue;
        result += processRegion(region, shapes);
    }
    return result;
}

long long parseInput(Reader& reader){
    long long result = 0;
    std::string content = reader.readAll();
    std::map<int, Shape> shapes;
    std::vector<std::string> descriptions = split(content, "\n\n");
    std::vector<std::string> shape_descriptions(descriptions.begin(), descriptions.end() - 1);
    getShapes(shape_descriptions, shapes);
    std::cout << "Total shapes: " << shapes.size()<< std::endl;
    std::string regions = descriptions[descriptions.size() - 1];
    result = processRegions(regions, shapes);
    return result;
}


int main(int argc, char* argv[]) {
    std::string file = argv[1];
    Reader reader = Reader(file);
    long long result = parseInput(reader);

    return 0;
}