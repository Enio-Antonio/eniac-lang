#pragma once
#include <string>
#include <vector>
#include <iomanip>
#include <sstream>

class Processor {
    public:
    Processor();
    void process_function(std::vector<std::string> &func_code, std::vector<std::string> &arg_list);
    std::string calculate(std::vector<std::string> expd);
    std::vector<std::string> split(std::string str, char separator);
    int post_dot_size(std::string str);
};