#include "dictionary.hpp"
#include <iostream>


Dictionary::Dictionary(){}

void Dictionary::add_key_value(std::string key, std::string value)
{
    keys.push_back(key);
    values.push_back(value);
}

void Dictionary::add_key_value(std::string key, std::vector<std::string> value)
{
    keys.push_back(key);
    functions.push_back(value);
}

std::string Dictionary::find(std::string key)
{
    for (size_t i = 0; i < keys.size(); i++)
    {
        if (key == keys[i])
        {
            return values[i];
        }
    }

    return "Sem chave correspondente";
}

std::vector<std::string> Dictionary::find_portal(std::string key)
{
    for (size_t i = 0; i < keys.size(); i++)
    {
        if (key == keys[i])
        {
            return functions[i];
        }
    }
    std::vector<std::string> null_return;
    return null_return;
 
}

void Dictionary::update_value(std::string key, std::string new_value)
{
    for (size_t i = 0; i < keys.size(); i++)
    {
        if (key == keys[i])
        {
            values[i] = new_value;
        }
    }
}

bool Dictionary::is_in_memory(std::string key)
{
    for (size_t i = 0; i < keys.size(); i++)
    {
        if (key == keys[i])
        {
            return true;
        }
    }
    
    return false;
}