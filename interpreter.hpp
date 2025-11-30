#pragma once
#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "./Auxiliar/dictionary.hpp"
#include "./Auxiliar/processor.hpp"

extern Processor processor;
extern Dictionary functions;
extern std::string grammar[];

void variable_error(std::string variable);

bool is_key_word(std::string word);

void print(std::string &arg);

int interpret(std::vector<std::string> tokenized_code);