#include "dicionario.hpp"
#include <iostream>


Dicionario::Dicionario(){}

void Dicionario::add_key_value(std::string key, std::string value)
{
    keys.push_back(key);
    values.push_back(value);
}

void Dicionario::add_key_value(std::string key, std::vector<std::string> value)
{
    keys.push_back(key);
    rotinas.push_back(value);
}

std::string Dicionario::find(std::string key)
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

std::vector<std::string> Dicionario::find_portal(std::string key)
{
    for (size_t i = 0; i < keys.size(); i++)
    {
        if (key == keys[i])
        {
            return rotinas[i];
        }
    }
    std::vector<std::string> retorno_vazio;
    return retorno_vazio;
 
}

void Dicionario::update_value(std::string key, std::string new_value)
{
    for (size_t i = 0; i < keys.size(); i++)
    {
        if (key == keys[i])
        {
            values[i] = new_value;
        }
    }
}

bool Dicionario::is_in_memory(std::string key)
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