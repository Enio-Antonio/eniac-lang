#include <string>
#include <vector>

class Tratador {
    public:
    Tratador();
    std::vector<std::string> tratar_funcao(std::vector<std::string> &codigo_func, std::vector<std::string> &arg_list);
    std::string calcular(std::vector<std::string> expd);
};