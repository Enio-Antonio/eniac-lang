#include "interpreter.hpp"

int main(int argc, char *argv[]) {
    if (argv[1] == NULL) {
        std::cerr << "Uso: eniac [arquivo].ec";
        return -1;
    }
    std::string filename = argv[1];
    int dot_index = filename.find('.');

    if (filename[dot_index + 1] != 'e') {
        std::cerr << "A extensão do arquivo deve ser '.ec'";
        return -1;
    }

    std::ifstream code;
    code.open(filename);
    if (!code) {
        std::cerr << filename << " não encontrado.\n";
        return -1;
    }
    std::vector<std::string> tokenized_code;
    std::string aux;

    while (code.good()) {
        code >> aux;
        tokenized_code.push_back(aux);
    }

    if (!(tokenized_code[tokenized_code.size() - 1] == "final")) {
        std::cerr << "Está faltando a palavra-chave 'final'.";
        return -1;
    }

    interpret(tokenized_code);

    code.close();

    return 0;
}