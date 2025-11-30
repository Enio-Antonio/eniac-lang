#pragma once
#include <string>
#include <vector>

class Processor {
    public:
    Processor();
    std::vector<std::string> process_function(std::vector<std::string> &func_code, std::vector<std::string> &arg_list);
    std::string calculate(std::vector<std::string> expd);
};