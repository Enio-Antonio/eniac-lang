#pragma once

#include <vector>
#include <string>

class Dicionario
{
    std::vector<std::string> keys, values;

public:
    Dicionario();
    std::string find(std::string key); 
    void add_key_value(std::string key, std::string value);
    void update_value(std::string key, std::string new_value);
    bool is_in_memory(std::string key);
};