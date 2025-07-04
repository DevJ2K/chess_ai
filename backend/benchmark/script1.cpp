#include <vector>
#include <iostream>

int main(void) {
    std::vector<int> lst;
    lst.reserve(10000000);
    for (size_t i = 0; i < 10000000; i++)
        lst.push_back(i);
}