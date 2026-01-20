#include <iostream>
#include <vector>
#include <string>
#include <algorithm>

// This function will eventually be called by Python to sort sentences by length or importance
extern "C" {
    void sort_sentences(const char** input, int count, int* indices) {
        std::vector<std::pair<int, int>> sentence_data;

        // Store length and original index
        for (int i = 0; i < count; ++i) {
            std::string s = input[i];
            sentence_data.push_back({(int)s.length(), i});
        }

        // Sort by length (descending) to find the most "substantial" sentences
        std::sort(sentence_data.begin(), sentence_data.end(), std::greater<std::pair<int, int>>());

        // Fill the indices array with the new order
        for (int i = 0; i < count; ++i) {
            indices[i] = sentence_data[i].second;
        }
    }
}