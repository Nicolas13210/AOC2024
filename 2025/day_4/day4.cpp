#include <iostream>
#include <string>
#include <utility>
#include <vector>
#include <cmath>
#include <regex>
#include <map>
#include "../utils/stringHelper.cpp"
#include "../utils/Reader.cpp"
std::vector<std::vector<int>> parse_input(Reader& reader) {
    std::vector<std::vector<int>> parsed_lines;
    int line_count = reader.getLineCount();
    for (int i = 0; i < line_count; i++) {
        std::string line = reader.readLine();
        std::vector<int> numbers;
        for (const char& token : line) {
            if (token == '.')
                numbers.push_back(0);
            else
                numbers.push_back(1);
        }
        parsed_lines.push_back(numbers);
    }

    return parsed_lines;
}

void print_grid(const std::vector<std::vector<int>>& grid) {
    for (const auto& row : grid) {
        for (const auto& cell : row) {
            std::cout << cell;
        }
        std::cout << std::endl;
    }
}

int check_neighbours(const std::vector<std::vector<int>>& grid, int row, int col) {
    if (grid[row][col] == 0)
        return -1;
    int count = 0;
    int directions[8][2] = {{-1, -1}, {-1, 0}, {-1, 1},
                            {0, -1},          {0, 1},
                            {1, -1}, {1, 0}, {1, 1}};

    for (const auto& dir : directions) {
        int new_row = row + dir[0];
        int new_col = col + dir[1];
        if (new_row >= 0 && new_row < grid.size() && new_col >= 0 && new_col < grid[0].size()) {
            count += grid[new_row][new_col];
        }
    }
    return count;
}

int check_grid(std::vector<std::vector<int>>& grid) {
    std::vector<std::vector<int>>& mutable_grid = const_cast<std::vector<std::vector<int>>&>(grid);
    
    int total = 0;
    for (int i = 0; i < grid.size(); i++) {
        for (int j = 0; j < grid[0].size(); j++) {
            int tmp_total = check_neighbours(grid, i, j);
            if (tmp_total <4 && tmp_total >=0)
{                total += 1;
                mutable_grid[i][j] = 0;
            }
        }
    }
    mutable_grid.swap(grid);
    return total;
}



int check_grid_rec(std::vector<std::vector<int>>& grid){
    int prev_total = -1;
    int total = 0;
    while (prev_total!=0) {
        // print_grid(grid);
        prev_total = check_grid(grid);
        total += prev_total;
    }
    return total;
}



int main(int argc, char* argv[]) {
    std::string file = argv[1];
    Reader reader = Reader(file);
    std::vector<std::vector<int>> grid = parse_input(reader);
    int total = check_grid_rec(grid);
    std::cout << "Total: " << total << std::endl;
    return 0;
}