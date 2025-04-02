#include <iostream>
#include <fstream>
#include <vector>
#include <string>
#include "./Auxiliar/dicionario.hpp"

void erro_variavel(std::string variavel)
{
    std::cout << "ERRO: variável não declarada: " << variavel << "\n";
}

int main(int argc, char *argv[])
{
    std::string nome_arquivo = argv[1];
    int dot_index = nome_arquivo.find('.');

    if (nome_arquivo[dot_index + 1] != 'e')
    {
        std::cout << "A extensão do arquivo deve ser '.ec'";
        return -1;
    }

    std::ifstream codigo;
    codigo.open(nome_arquivo);
    std::vector<std::string> codigo_tokenizado;
    std::string aux;

    while (codigo.good())
    {
        codigo >> aux;
        codigo_tokenizado.push_back(aux);
    }

    if (!(codigo_tokenizado[codigo_tokenizado.size() - 1] == "final"))
    {
        std::cout << "Está faltando a palavra-chave 'final'.";
    }

    int contador = 0;

    Dicionario memoria;

    while (true)
    {
        std::string word = codigo_tokenizado[contador];
        // std::cout << word << "\n";

        if (word == "release")
        {
            contador += 2;
            std::string arg_print = codigo_tokenizado[contador];
            std::vector<std::string> arg_list;

            while (arg_print != ">")
            {
                arg_print = codigo_tokenizado[contador];

                if (arg_print[0] == '$')
                {
                    if (!memoria.is_in_memory(arg_print))
                    {
                        erro_variavel(arg_print);
                        return -1;
                    }
                    arg_list.push_back(memoria.find(arg_print));
                }
                else
                {
                    arg_list.push_back(arg_print);
                }

                contador++;
            }

            arg_list.pop_back();

            for (std::string elemento : arg_list)
            {
                std::cout << elemento << " ";
            }
            std::cout << "\n";

            contador--;
        }

        else if (word == "capture")
        {
            contador++;
            if (codigo_tokenizado[contador][0] != 36) // 36 é o código de $
            {
                std::cout << "ERRO: está faltando o `$` em: " << codigo_tokenizado[contador] << "\n";
                return -1;
            }
            std::string var_para_input = codigo_tokenizado[contador];
            std::string input_value;
            std::cin >> input_value;
            memoria.add_key_value(var_para_input, input_value);
        }

        else if (word == "receive")
        {
            contador++;
            if (codigo_tokenizado[contador][0] != 36)
            {
                erro_variavel(codigo_tokenizado[contador]);
                return -1;
            }

            std::string var_nome = codigo_tokenizado[contador];
            contador += 2;
            if (codigo_tokenizado[contador][0] == 36)
            {
                if (memoria.is_in_memory(codigo_tokenizado[contador]))
                {
                    memoria.update_value(var_nome, codigo_tokenizado[contador]);
                }
                else
                {
                    std::cout << "ERRO: variável não declarada: " << codigo_tokenizado[contador] << "\n";
                    return -1;
                }
            }
            else
            {
                memoria.add_key_value(var_nome, codigo_tokenizado[contador]);
            }
        }

        else if (word == "decide")
        {
            int contador_antes_if = contador;
            contador++;
            std::string left_operand;
            std::string right_operand;
            bool result;

            if (codigo_tokenizado[contador][0] == 36)
            {
                if (!memoria.is_in_memory(codigo_tokenizado[contador]))
                {
                    erro_variavel(codigo_tokenizado[contador]);
                    return -1;
                }
                else
                {
                    left_operand = memoria.find(codigo_tokenizado[contador]);
                }
            }
            else
            {
                left_operand = codigo_tokenizado[contador];
            }

            contador++;
            std::string comparator = codigo_tokenizado[contador];
            contador++;

            if (codigo_tokenizado[contador][0] == 36)
            {
                if (!memoria.is_in_memory(codigo_tokenizado[contador]))
                {
                    erro_variavel(codigo_tokenizado[contador]);
                    return -1;
                }
                else
                {
                    right_operand = memoria.find(codigo_tokenizado[contador]);
                }
            }
            else
            {
                right_operand = codigo_tokenizado[contador];
            }

            int contador_words = 0;
            int contador_aux = contador;
            std::string temp;

            while (temp != "endd")
            {
                contador_aux++;
                temp = codigo_tokenizado[contador_aux];
                contador_words++;
            }

            if (comparator == "eq")
            {
                result = std::stof(left_operand) == std::stof(right_operand);
            }
            else if (comparator == "gt")
            {
                result = std::stoi(left_operand) > std::stoi(right_operand);
            }
            else if (comparator == "lt")
            {
                result = std::stoi(left_operand) < std::stoi(right_operand);
            }
            else if (comparator == "gte")
            {
                result = std::stoi(left_operand) >= std::stoi(right_operand);
            }
            else if (comparator == "lte")
            {
                result = std::stoi(left_operand) <= std::stoi(right_operand);
            }

            if (result)
            {
                codigo_tokenizado.erase(codigo_tokenizado.begin() + contador_antes_if);
                codigo_tokenizado.erase(codigo_tokenizado.begin() + contador_antes_if);
                codigo_tokenizado.erase(codigo_tokenizado.begin() + contador_antes_if);
                codigo_tokenizado.erase(codigo_tokenizado.begin() + contador_antes_if);
                codigo_tokenizado.erase(codigo_tokenizado.begin() + contador + contador_words - 4);
                contador = contador_antes_if - 1;
            }
            else
            {
                contador += contador_words - 1;
            }
        }

        else if (word == "repeat_n_times")
        {
            int contador_repeat = contador;
            contador++;
            std::string n_times;

            if (codigo_tokenizado[contador][0] == 36)
            {
                if (!memoria.is_in_memory(codigo_tokenizado[contador]))
                {
                    erro_variavel(codigo_tokenizado[contador]);
                    return -1;
                }
                n_times = memoria.find(codigo_tokenizado[contador]);
            }
            else
            {
                n_times = codigo_tokenizado[contador];
            }

            contador++;
            int contador_aux = contador;
            int contador_words = 0;
            std::string temp;
            std::vector<std::string> lista_repeat;

            while (temp != "endr")
            {
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

            for (auto i = 0; i < std::stoi(n_times) - 1; i++)
            {
                for (std::string palavra : lista_repeat)
                {
                    codigo_tokenizado.insert(codigo_tokenizado.begin() + p_index, palavra);
                    p_index++;
                }
            }
        }

        else if (word[0] == 36)
        {
            std::string var_nome = word;
            contador += 2;
            std::string novo_valor = codigo_tokenizado[contador];
            memoria.update_value(var_nome, novo_valor);
        }

        else if (word == "final")
        {
            break;
        }

        contador++;
    }

    return 0;
}
