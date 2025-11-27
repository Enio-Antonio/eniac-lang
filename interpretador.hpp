#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "./Auxiliar/dicionario.hpp"
#include "./Auxiliar/tratador.hpp"

extern Tratador processador;
extern Dicionario rotinas;
extern std::string gramatica[];

void erro_variavel(std::string variavel);

bool is_key_word(std::string word);

void print(std::string &coisa);

int interpretar(std::vector<std::string> codigo_tokenizado);