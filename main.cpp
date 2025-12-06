#include "interpreter.hpp"

int main(int argc, char *argv[]) {
    if (argv[1] == NULL) {
        std::cerr << "Usage: eniac [file].ec\n";
        return -1;
    }
    std::string filename = argv[1];
    if (filename[0] == '.') {
        std::string aux = filename;
        std::string copy;
        for (size_t i = 2; i < aux.size(); i++) {
            copy.push_back(aux[i]);
        }

        filename = copy.c_str();
    }
    int dot_index = filename.find('.');

    if (filename[dot_index + 1] != 'e') {
        std::cerr << "File extension must be '.ec'\n";
        return -1;
    }

    std::ifstream code;
    code.open(filename);
    if (!code) {
        std::cerr << filename << " not found.\n";
        return -1;
    }
    std::vector<std::string> tokenized_code;
    std::string aux;

    while (code.good()) {
        code >> aux;
        tokenized_code.push_back(aux);
    }

    if (!(tokenized_code[tokenized_code.size() - 1] == "final")) {
        std::cerr << "ERROR: missing keyword 'final'.\n";
        return -1;
    }

    interpret(tokenized_code);

    code.close();

    return 0;
}