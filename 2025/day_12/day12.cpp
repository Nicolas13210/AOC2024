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
    Shape(std::vector<std::vector<bool>> cells) : cells(cells), id(-1) {
        area = 0;
        for (const auto& row : cells) {
            for (bool cell : row) {
                if (cell) area++;
            }
        }
    }
    Shape(std::string description) {
        area = 0;
        std::vector<std::string> parts = split(description, ':');
        id = std::stoi(parts[0]);
        std::string shape_description = parts[1];
        std::vector<std::string> rows = split(shape_description, '\n');
        for (const std::string& row : rows) {
            if (row.empty()) continue;
            std::vector<bool> cell_row;
            for (char c : row) {
                if (c == '#'){
                    area++;
                    cell_row.push_back(true);
                } else {
                    cell_row.push_back(false);
                }
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

    int getArea() const {
        return area;
    }

    int getHeight() const {
        return cells.size();
    }
    int getWidth() const {
        return cells[0].size();
    }

    std::vector<Shape> getAllUniqueOrientations() const {
        std::vector<Shape> orientations;
        std::map<std::string, bool> seen;
        for (int flip = 0; flip <= 1; ++flip) {
            Shape current = (flip == 0) ? *this : flipHorizontal();
            for (int rot = 0; rot < 4; ++rot) {
                Shape rotated = current.getRotated(rot);
                std::string shape_str = rotated.getShapeString();
                if (seen.find(shape_str) == seen.end()) {
                    orientations.push_back(rotated);
                    seen[shape_str] = true;
                }
            }
        }
        return orientations;
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

    Shape flipHorizontal() const {
        size_t rows = cells.size();
        size_t cols = cells[0].size();
        std::vector<std::vector<bool>> flipped(rows, std::vector<bool>(cols, false));
        for (size_t r = 0; r < rows; ++r) {
            for (size_t c = 0; c < cols; ++c) {
                flipped[r][cols - 1 - c] = cells[r][c];
            }
        }
        return Shape(flipped);
    }

    Shape flipVertical() const {
        size_t rows = cells.size();
        size_t cols = cells[0].size();
        std::vector<std::vector<bool>> flipped(rows, std::vector<bool>(cols, false));
        for (size_t r = 0; r < rows; ++r) {
            for (size_t c = 0; c < cols; ++c) {
                flipped[rows - 1 - r][c] = cells[r][c];
            }
        }
        return Shape(flipped);
    }

    std::vector<std::vector<bool>> cells;
    int id;
    int area;

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
        std::vector<std::vector<bool>> region_cells(size.second, std::vector<bool>(size.first, false));
        region = Shape(region_cells);
    }
    std::pair<int,int> getSize() const {
        return size;
    }
    std::vector<int> getShapeAmounts() const {
        return shape_amounts;
    }

    bool canFit(Shape shape, int x, int y) const {
        std::vector<std::vector<bool>> shape_cells = shape.getCells();
        int shape_rows = shape_cells.size();
        int shape_cols = shape_cells[0].size();
        if (x + shape_cols > size.first || y + shape_rows > size.second) {
            return false;
        }
        for (int r = 0; r < shape_rows; ++r) {
            for (int c = 0; c < shape_cols; ++c) {
                if (shape_cells[r][c] && region.getCells()[y + r][x + c]) {
                    return false;
                }
            }
        }
        return true;
    }
    bool shouldStop() const{
        for (int amt : shape_amounts) {
            if (amt > 0) {
                return false;
            }
        }
        return true;
    }

    bool canFitAllShapes(const std::map<int, Shape>& shapes) const {
        if (shouldStop()) {
            return true;
        }

        int minAreaNeeded = 0;
        // int maxWidthNeeded = 0;
        // int maxHeightNeeded = 0;
        for (size_t i = 0; i < shape_amounts.size(); i++) {
            minAreaNeeded += shape_amounts[i] * shapes.at(i).getArea();
            // maxWidthNeeded += shape_amounts[i] * shapes.at(i).getWidth();
            // maxHeightNeeded += shape_amounts[i] * shapes.at(i).getHeight(); 
        }
        // if ((maxWidthNeeded < size.first && maxHeightNeeded < size.second) || (maxHeightNeeded < size.first && maxWidthNeeded < size.second)) {
        //     return true;
        // }

        if (minAreaNeeded > size.first * size.second) {
            return false;
        }

        return true;
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
    Shape region;

};

void getShapes(std::vector<std::string> shape_descriptions, std::map<int, Shape>& shapes) {
    for (const std::string& desc : shape_descriptions) {
        Shape shape(desc);
        std::vector<Shape> orientations = shape.getAllUniqueOrientations();
        shapes[shape.getId()] = shape;
    }
}

int processRegion(const std::string& region, const std::map<int, Shape>& shapes) {
    int result = 0;
    Region reg(region);
    if (reg.canFitAllShapes(shapes)) {
        result = 1;
    }
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
    std::cout << "Result: " << result << std::endl;

    return 0;
}