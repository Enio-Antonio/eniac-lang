#include "interpretador.hpp"

int main(int argc, char *argv[]) {
    if (argv[1] == NULL) {
        std::cerr << "Uso: eniac [arquivo].ec";
        return -1;
    }
    std::string nome_arquivo = argv[1];
    int dot_index = nome_arquivo.find('.');

    if (nome_arquivo[dot_index + 1] != 'e') {
        std::cerr << "A extensão do arquivo deve ser '.ec'";
        return -1;
    }

    std::ifstream codigo;
    codigo.open(nome_arquivo);
    if (!codigo) {
        std::cerr << nome_arquivo << " não encontrado.\n";
        return -1;
    }
    std::vector<std::string> codigo_tokenizado;
    std::string aux;

    while (codigo.good()) {
        codigo >> aux;
        codigo_tokenizado.push_back(aux);
    }

    if (!(codigo_tokenizado[codigo_tokenizado.size() - 1] == "final")) {
        std::cerr << "Está faltando a palavra-chave 'final'.";
        return -1;
    }

    interpretar(codigo_tokenizado);

    codigo.close();

    return 0;
}