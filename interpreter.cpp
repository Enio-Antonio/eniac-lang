#include "interpreter.hpp"

Processor processor;
Dictionary functions;

std::string grammar[] = {"release", ">", "capture", "portal", "receive", "final", "repeat_n_times", "endr", "decide", "endd"};

void variable_error(std::string variable) {
    std::cerr << "ERROR: non declared variable: " << variable << "\n";
}

bool is_key_word(std::string word) {
    for (int i = 0; i < 10; i++) {
        if (word == grammar[i]) {
            return true;
        }
    }
    return false;
}

Error is_blocks_closed(std::vector<std::string> tokenized_code) {
    int decide_counter = 0;
    int endd_counter = 0; 
    int repeat_counter = 0; 
    int endr_counter = 0;

    for (auto word : tokenized_code) {
        if (word == "decide") {
            decide_counter++;
        } else if (word == "endd") {
            endd_counter++;
        } else if (word == "repeat_n_times") {
            repeat_counter++;
        } else if (word == "endr") {
            endr_counter++;
        }
    }

    Error e;

    if (decide_counter != endd_counter) {
        e.type = "decide";
        e.pos = decide_counter;
    } else if (repeat_counter != endr_counter) {
        e.type = "repeat";
        e.pos = repeat_counter;
    } else {
        e.type = "null";
        e.pos = 0;
    }

    return e;
}

// Somente para facilitar o std::cout
void print(std::string &arg) {
    std::cout << arg << "\n";
}

int interpret(std::vector<std::string> tokenized_code) {
    auto err = is_blocks_closed(tokenized_code);
    if (err.type != "null") {
        std::cout << "ERROR: " << err.type << " block " << err.pos << " was not closed.\n";
        return -1;
    }

    int counter = 0;

    Dictionary memory;

    while (true) {
        std::string word = tokenized_code[counter];
        // std::cout << word << "\n";

        if (word == "release") {
            counter += 2;
            std::string arg_print = tokenized_code[counter];
            std::vector<std::string> arg_list;

            while (arg_print != ">") {
                arg_print = tokenized_code[counter];

                if (arg_print[0] == '$') {
                    if (!memory.is_in_memory(arg_print)) {
                        variable_error(arg_print);
                        return -1;
                    }
                    arg_list.push_back(memory.find(arg_print));
                }
                else {
                    arg_list.push_back(arg_print);
                }

                counter++;
            }

            arg_list.pop_back();

            std::string print_string;

            for (std::string &element : arg_list) {
                char *endptr;
                float val = std::strtof(element.c_str(), &endptr);
                if (*endptr == '\0') {
                    //std::cout << val << " ";
                    print_string += std::to_string(val) + " ";
                } else {
                    //std::cout << element << " ";
                    print_string += element + " ";
                }
            }

            // Adiciona o caractere '\n' verdadeiro (ASCII 10)
            std::string real;
            for (size_t i = 0; i < print_string.size(); ++i) {
                if (print_string[i] == '\\' && i + 1 < print_string.size() && print_string[i+1] == 'n') {
                    real += '\n';
                    i++; // pular o 'n'
                } else {
                    real += print_string[i];
                }
            }

            auto lines = processor.split(real, '\n');

            for (auto line : lines) {
                std::cout << line << "\n";
            }

            counter--;
        }

        else if (word == "capture") {
            counter++;
            if (tokenized_code[counter][0] != 36) { // 36 é o código de $
                std::cerr << "ERROR: missing `$` in: " << tokenized_code[counter] << "\n";
                return -1;
            }
            std::string input_var = tokenized_code[counter];
            std::string input_value;
            std::cin >> input_value;
            memory.add_key_value(input_var, input_value);
        } 

        else if (word == "decide") {
            counter++;
            std::string left_operand;
            std::string right_operand;
            bool result;

            if (tokenized_code[counter][0] == 36) {
                if (!memory.is_in_memory(tokenized_code[counter])) {
                    variable_error(tokenized_code[counter]);
                    return -1;
                } else {
                    left_operand = memory.find(tokenized_code[counter]);
                }
            } else {
                left_operand = tokenized_code[counter];
            }

            counter++;
            std::string comparator = tokenized_code[counter];
            counter++;

            if (tokenized_code[counter][0] == 36) {
                if (!memory.is_in_memory(tokenized_code[counter])) {
                    variable_error(tokenized_code[counter]);
                    return -1;
                } else {
                    right_operand = memory.find(tokenized_code[counter]);
                }
            } else {
                right_operand = tokenized_code[counter];
            }

            int counter_words = 0;
            int counter_aux = counter;
            std::string temp;

            while (temp != "endd") {
                counter_aux++;
                temp = tokenized_code[counter_aux];
                counter_words++;
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
                counter += counter_words - 1;
        }

        else if (word == "repeat_n_times") {
            int counter_repeat = counter;
            counter++;
            std::string n_times;

            if (tokenized_code[counter][0] == 36) {
                if (!memory.is_in_memory(tokenized_code[counter])) {
                    variable_error(tokenized_code[counter]);
                    return -1;
                }
                n_times = memory.find(tokenized_code[counter]);
            } else {
                n_times = tokenized_code[counter];
            }

            counter++;
            int counter_aux = counter;
            int counter_words = 0;
            std::string temp;
            std::vector<std::string> list_repeat;

            while (temp != "endr") {
                temp = tokenized_code[counter_aux];
                list_repeat.push_back(temp);
                counter_aux++;
                counter_words++;
            }

            tokenized_code.erase(tokenized_code.begin() + counter_repeat);
            tokenized_code.erase(tokenized_code.begin() + counter_repeat);
            counter -= 3;
            int p_index = counter + counter_words;
            list_repeat.pop_back();
            tokenized_code.erase(tokenized_code.begin() + counter + counter_words);

            for (auto i = 0; i < std::stoi(n_times) - 1; i++) {
                for (std::string element : list_repeat) {
                    tokenized_code.insert(tokenized_code.begin() + p_index, element);
                    p_index++;
                }
            }
        }

        else if (word[0] == 36) {
            std::string var_name = word;
            counter += 2;

            std::vector<std::string> operands_list;

            while (!is_key_word(tokenized_code[counter]) && !(tokenized_code[counter][0] == 36 && tokenized_code[counter+1] == "=")) {
                if (tokenized_code[counter][0] == 36) {
                    operands_list.push_back(memory.find(tokenized_code[counter]));
                } else { 
                    operands_list.push_back(tokenized_code[counter]);
                }
                counter++;
            }
            counter--;
            auto result = processor.calculate(operands_list); 

            if (memory.is_in_memory(var_name)) {
                memory.update_value(var_name, result);       
            } else {
                memory.add_key_value(var_name, result);
            }
        }

        else if (word == "final") {
            break;
        }

        else if (word == "portal") {
            counter++;
            std::string func_name = tokenized_code[counter];
            if (func_name[0] != 64) {
                std::cerr << "ERROR: functions names must start with `@`: " << func_name << "\n";
                return -1;
            }
            counter += 1;
            std::vector<std::string> func_code;
            
            while (tokenized_code[counter] != "endp") {
                func_code.push_back(tokenized_code[counter]);
                counter++;
            }
            func_code.push_back("final");
            functions.add_key_value(func_name, func_code);
        } 

        else if (word[0] == 64) {
            auto func_name = word;
            auto func = functions.find_portal(func_name);
            int result;
            
            counter++;

            if (tokenized_code[counter] == "|") {
                counter++;
                std::vector<std::string> list_args;
                while (tokenized_code[counter] != "|") {
                    list_args.push_back(tokenized_code[counter]);
                    counter++;
                } 
                processor.process_function(func, list_args);
                result = interpret(func);
            } else { 
                result = interpret(func);
                counter--;
            }
            if (result == -1) {
                std::cerr << "Failed in " << func_name << "\n";
                return -1;
            }
        }

        counter++;
    }

    return 0;
}