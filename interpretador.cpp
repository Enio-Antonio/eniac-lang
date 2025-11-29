#include "interpretador.hpp"

Tratador processador;
Dicionario rotinas;

std::string gramatica[] = {"release", ">", "capture", "portal", "receive", "final", "repeat_n_times", "endr", "decide", "endd"};

void erro_variavel(std::string variavel) {
    std::cerr << "ERRO: variável não declarada: " << variavel << "\n";
}

bool is_key_word(std::string word) {
    for (int i = 0; i < 10; i++)
    {
        if (word == gramatica[i])
        {
            return true;
        }
    }
    return false;
}

// Somente para facilitar o std::cout
void print(std::string &coisa) {
    std::cout << coisa << "\n";
}

int interpretar(std::vector<std::string> codigo_tokenizado) {
    int contador = 0;

    Dicionario memoria;

    while (true) {
        std::string word = codigo_tokenizado[contador];
        // std::cout << word << "\n";

        if (word == "release") {
            contador += 2;
            std::string arg_print = codigo_tokenizado[contador];
            std::vector<std::string> arg_list;

            while (arg_print != ">") {
                arg_print = codigo_tokenizado[contador];

                if (arg_print[0] == '$') {
                    if (!memoria.is_in_memory(arg_print)) {
                        erro_variavel(arg_print);
                        return -1;
                    }
                    arg_list.push_back(memoria.find(arg_print));
                }
                else {
                    arg_list.push_back(arg_print);
                }

                contador++;
            }

            arg_list.pop_back();

            for (std::string &elemento : arg_list) {
                char *endptr;
                float val = std::strtof(elemento.c_str(), &endptr);
                if (*endptr == '\0') {
                    std::cout << val << " ";
                } else {
                    std::cout << elemento << " ";
                }
            }
            std::cout << "\n";

            contador--;
        }

        else if (word == "capture") {
            contador++;
            if (codigo_tokenizado[contador][0] != 36) // 36 é o código de $
            {
                std::cerr << "ERRO: está faltando o `$` em: " << codigo_tokenizado[contador] << "\n";
                return -1;
            }
            std::string var_para_input = codigo_tokenizado[contador];
            std::string input_value;
            std::cin >> input_value;
            memoria.add_key_value(var_para_input, input_value);
        }

        else if (word == "receive") {
            contador++;
            if (codigo_tokenizado[contador][0] != 36) {
                erro_variavel(codigo_tokenizado[contador]);
                return -1;
            }

            std::string var_nome = codigo_tokenizado[contador];
            contador += 2;
            if (codigo_tokenizado[contador][0] == 36) {
                if (memoria.is_in_memory(codigo_tokenizado[contador])) {
                    memoria.add_key_value(var_nome, memoria.find(codigo_tokenizado[contador]));
                }
                else {
                    std::cerr << "ERRO: variável não declarada: " << codigo_tokenizado[contador] << "\n";
                    return -1;
                }
            }
            else {
                memoria.add_key_value(var_nome, codigo_tokenizado[contador]);
            }
        }

        else if (word == "decide") {
            contador++;
            std::string left_operand;
            std::string right_operand;
            bool result;

            if (codigo_tokenizado[contador][0] == 36) {
                if (!memoria.is_in_memory(codigo_tokenizado[contador])) {
                    erro_variavel(codigo_tokenizado[contador]);
                    return -1;
                } else {
                    left_operand = memoria.find(codigo_tokenizado[contador]);
                }
            } else {
                left_operand = codigo_tokenizado[contador];
            }

            contador++;
            std::string comparator = codigo_tokenizado[contador];
            contador++;

            if (codigo_tokenizado[contador][0] == 36) {
                if (!memoria.is_in_memory(codigo_tokenizado[contador])) {
                    erro_variavel(codigo_tokenizado[contador]);
                    return -1;
                } else {
                    right_operand = memoria.find(codigo_tokenizado[contador]);
                }
            } else {
                right_operand = codigo_tokenizado[contador];
            }

            int contador_words = 0;
            int contador_aux = contador;
            std::string temp;

            while (temp != "endd") {
                contador_aux++;
                temp = codigo_tokenizado[contador_aux];
                contador_words++;
            }

            if (comparator == "eq") {
                result = std::stof(left_operand) == std::stof(right_operand);
            } else if (comparator == "gt") {
                result = std::stoi(left_operand) > std::stoi(right_operand);
            } else if (comparator == "lt") {
                result = std::stoi(left_operand) < std::stoi(right_operand);
            } else if (comparator == "gte") {
                result = std::stoi(left_operand) >= std::stoi(right_operand);
            } else if (comparator == "lte") {
                result = std::stoi(left_operand) <= std::stoi(right_operand);
            }

            if (!result)
                contador += contador_words - 1;
        }

        else if (word == "repeat_n_times") {
            int contador_repeat = contador;
            contador++;
            std::string n_times;

            if (codigo_tokenizado[contador][0] == 36) {
                if (!memoria.is_in_memory(codigo_tokenizado[contador])) {
                    erro_variavel(codigo_tokenizado[contador]);
                    return -1;
                }
                n_times = memoria.find(codigo_tokenizado[contador]);
            } else {
                n_times = codigo_tokenizado[contador];
            }

            contador++;
            int contador_aux = contador;
            int contador_words = 0;
            std::string temp;
            std::vector<std::string> lista_repeat;

            while (temp != "endr") {
                temp = codigo_tokenizado[contador_aux];
                lista_repeat.push_back(temp);
                contador_aux++;
                contador_words++;
            }

            codigo_tokenizado.erase(codigo_tokenizado.begin() + contador_repeat);
            codigo_tokenizado.erase(codigo_tokenizado.begin() + contador_repeat);
            contador -= 3;
            int p_index = contador + contador_words;
            lista_repeat.pop_back();
            codigo_tokenizado.erase(codigo_tokenizado.begin() + contador + contador_words);

            for (auto i = 0; i < std::stoi(n_times) - 1; i++) {
                for (std::string palavra : lista_repeat) {
                    codigo_tokenizado.insert(codigo_tokenizado.begin() + p_index, palavra);
                    p_index++;
                }
            }
        }

        else if (word[0] == 36) {
            std::string var_nome = word;
            contador += 2;
            std::string novo_valor = codigo_tokenizado[contador];

            std::vector<std::string> lista_operadores;

            while (!is_key_word(codigo_tokenizado[contador]) && !(codigo_tokenizado[contador][0] == 36 && codigo_tokenizado[contador+1] == "=")) {
                if (codigo_tokenizado[contador][0] == 36) {
                    lista_operadores.push_back(memoria.find(codigo_tokenizado[contador]));
                } else { 
                    lista_operadores.push_back(codigo_tokenizado[contador]);
                }
                contador++;
            }
            contador--;

            auto result = processador.calcular(lista_operadores);
            
            memoria.update_value(var_nome, result);       
        }

        else if (word == "final") {
            break;
        }

        else if (word == "portal") {
            contador++;
            std::string nome_func = codigo_tokenizado[contador];
            if (nome_func[0] != 64) {
                std::cerr << "ERRO: nomes de funções devem iniciar com `@`: " << nome_func << "\n";
                return -1;
            }
            contador += 1;
            std::vector<std::string> codigo_rotina;
            
            while (codigo_tokenizado[contador] != "endp") {
                codigo_rotina.push_back(codigo_tokenizado[contador]);
                contador++;
            }
            codigo_rotina.push_back("final");
            rotinas.add_key_value(nome_func, codigo_rotina);
        } 

        else if (word[0] == 64) {
            auto nome_func = word;
            auto rotina = rotinas.find_portal(nome_func);
            
            contador++;

            if (codigo_tokenizado[contador] == "|") {
                contador++;
                std::vector<std::string> lista_args;
                while (codigo_tokenizado[contador] != "|") {
                    lista_args.push_back(codigo_tokenizado[contador]);
                    contador++;
                } 
                auto funcao_tratada = processador.tratar_funcao(rotina, lista_args);
                interpretar(funcao_tratada);
            } else { 
                interpretar(rotina);
                contador--;
            }
        }

        contador++;
    }

    return 0;
}