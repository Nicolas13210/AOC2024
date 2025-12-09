#include <vector>
#include <iostream>

class SortedList {
public:
    SortedList() = default;

    void insert(long long value) {
        auto it = std::lower_bound(data.begin(), data.end(), value);
        data.insert(it, value);
    }

    void print() const {
        for (long long value : data) {
            std::cout << value << " ";
        }
        std::cout << std::endl;
    }

    using iterator = std::vector<long long>::iterator;
    using const_iterator = std::vector<long long>::const_iterator;

    iterator begin() { return data.begin(); }
    iterator end() { return data.end(); }
    const_iterator begin() const { return data.begin(); }
    const_iterator end() const { return data.end(); }
    const_iterator cbegin() const { return data.cbegin(); }
    const_iterator cend() const { return data.cend(); }

private:
    std::vector<long long> data;
};
