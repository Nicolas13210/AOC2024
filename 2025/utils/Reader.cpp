#include <fstream>
#include <iostream>
#include <string>
#include <stdexcept>

class Reader {
public:
    Reader(const std::string& filename) : filename(filename), fileStream(filename) {
        if (!fileStream.is_open()) {
            throw std::runtime_error("Could not open file: " + filename);
        }
    }

    std::string readLine() {
        std::string line;
        if (std::getline(fileStream, line)) {
            return line;
        } else {
            throw std::runtime_error("End of file reached or error reading line.");
        }
    }

    void reset() {
        fileStream.clear(); // Clear any EOF flags
        fileStream.seekg(0, std::ios::beg); // Go back to the beginning
    }

    std::string readAll() {
        std::string content;
        std::string line;
        // Ensure we start reading from the beginning
        fileStream.clear();
        fileStream.seekg(0, std::ios::beg);
        while (std::getline(fileStream, line)) {
            content += line + "\n";
        }
        fileStream.clear(); 
        fileStream.seekg(0, std::ios::beg);  // Reset back to beginninge
        return content;
    }

    int getLineCount() const {
        int lineCount = 0;
        std::string line;
        std::ifstream tempStream(filename);
        if (!tempStream.is_open()) {
            throw std::runtime_error("Could not open file to count lines: " + filename);
        }
        while (std::getline(tempStream, line)) {
            lineCount++;
        }
        return lineCount;
    }

    ~Reader() {
        if (fileStream.is_open()) {
            fileStream.close();
        }
    }

private:
    std::string filename;
    std::ifstream fileStream;
};