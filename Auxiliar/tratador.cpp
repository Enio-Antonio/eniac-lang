#include "tratador.hpp"

Tratador::Tratador(){};

std::vector<std::string> Tratador::tratar_funcao(std::vector<std::string> &codigo_func, std::vector<std::string> &arg_list) {
    int arg_index = 0;
    for (size_t i = 0; i < arg_list.size(); i++) {
       arg_index++;
       for (size_t index = 0; index < codigo_func.size(); index++) {
            if (codigo_func[index] == "arg" + std::to_string(arg_index)) {
                codigo_func[index] = arg_list[i];
            }
       }
    }

    return codigo_func;
}

std::string Tratador::calcular(std::vector<std::string> expd) {
    if (expd.size() == 1)
        return expd[0];

    int t_d_counter = 0;
    int p_m_counter = 0;

    for (size_t e = 0; e < expd.size(); e++) {
        if (expd[e] == "*" || expd[e] == "/") {
            t_d_counter++;
        } else if (expd[e] == "+" || expd[e] == "-") {
            p_m_counter++;
        }
    }


    for (size_t vez = 0; vez < t_d_counter; vez++) {
        for (size_t i = 0; i < expd.size(); i++) {
            if (expd[i] == "*") {
                float resultado = std::stof(expd[i-1]) * std::stof(expd[i+1]);
                expd.erase(expd.begin() + i + 1);
                expd.erase(expd.begin() + i);
                expd.erase(expd.begin() + i - 1);
                if (i-3) {
                    expd.insert(expd.begin(), std::to_string(resultado));
                } else {
                    expd.insert(expd.begin() + i - 1, std::to_string(resultado));
                }
            } else if (expd[i] == "/") {
                float resultado = std::stof(expd[i-1]) * std::stof(expd[i+1]);
                expd.erase(expd.begin() + i + 1);
                expd.erase(expd.begin() + i);
                expd.erase(expd.begin() + i - 1);
                if (i-3) {
                    expd.insert(expd.begin(), std::to_string(resultado));
                } else {
                    expd.insert(expd.begin() + i - 1, std::to_string(resultado));
                }
            }
        }
    }

    for (size_t vez = 0; vez < p_m_counter; vez++) {
        for (size_t i = 0; i < expd.size(); i++) {
            if (expd[i] == "+") {
                float resultado = std::stof(expd[i-1]) + std::stof(expd[i+1]);
                expd.erase(expd.begin() + i + 1);
                expd.erase(expd.begin() + i);
                expd.erase(expd.begin() + i - 1);
                if (i-3) {
                    expd.insert(expd.begin(), std::to_string(resultado));
                } else {
                    expd.insert(expd.begin() + i - 1, std::to_string(resultado));
                }
            } else if (expd[i] == "-") {
                float resultado = std::stof(expd[i-1]) - std::stof(expd[i+1]);
                expd.erase(expd.begin() + i + 1);
                expd.erase(expd.begin() + i);
                expd.erase(expd.begin() + i - 1);
                if (i-3) {
                    expd.insert(expd.begin(), std::to_string(resultado));
                } else {
                    expd.insert(expd.begin() + i - 1, std::to_string(resultado));
                }
            }
        }
    }

    return expd[0];
};