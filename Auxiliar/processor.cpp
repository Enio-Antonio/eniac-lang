#include "processor.hpp"
#include <iostream>

Processor::Processor(){};

void Processor::process_function(std::vector<std::string> &func_code, std::vector<std::string> &arg_list) {
    int arg_index = 0;
    for (size_t i = 0; i < arg_list.size(); i++) {
       arg_index++;
       for (size_t index = 0; index < func_code.size(); index++) {
            if (func_code[index] == "arg" + std::to_string(arg_index)) {
                func_code[index] = arg_list[i];
            }
       }
    }
}

std::string Processor::calculate(std::vector<std::string> expd) {
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


    for (size_t time = 0; time < t_d_counter; time++) {
        for (size_t i = 0; i < expd.size(); i++) {
            if (expd[i] == "*") {
                float result = std::stof(expd[i-1]) * std::stof(expd[i+1]);
                expd.erase(expd.begin() + i + 1);
                expd.erase(expd.begin() + i);
                expd.erase(expd.begin() + i - 1);

                std::ostringstream fresult;
                int precision1 = post_dot_size(expd[i-1]);
                std::cout << "precisao: " << precision1 << "\n";
                int precision2 = post_dot_size(expd[i+1]);
                int final_precision = 0;

                if (precision1 > precision2) {
                    final_precision = precision1;
                } else if (precision2 > precision1) {
                    final_precision = precision1;
                } else {
                    final_precision = precision1;
                }

                fresult << std::fixed << std::setprecision(final_precision) << result;

                if (i-3) {
                    expd.insert(expd.begin(), fresult.str());
                } else {
                    expd.insert(expd.begin() + i - 1, fresult.str());
                }
            } else if (expd[i] == "/") {
                float result = std::stof(expd[i-1]) * std::stof(expd[i+1]);
                expd.erase(expd.begin() + i + 1);
                expd.erase(expd.begin() + i);
                expd.erase(expd.begin() + i - 1);

                std::ostringstream fresult;
                int precision1 = post_dot_size(expd[i-1]);
                std::cout << "precisao: " << precision1 << "\n";
                int precision2 = post_dot_size(expd[i+1]);
                int final_precision = 0;

                if (precision1 > precision2) {
                    final_precision = precision1;
                } else if (precision2 > precision1) {
                    final_precision = precision1;
                } else {
                    final_precision = precision1;
                }

                fresult << std::fixed << std::setprecision(final_precision) << result;

                if (i-3) {
                    expd.insert(expd.begin(), fresult.str());
                } else {
                    expd.insert(expd.begin() + i - 1, fresult.str());
                }
            }
        }
    }

    for (size_t time = 0; time < p_m_counter; time++) {
        for (size_t i = 0; i < expd.size(); i++) {
            if (expd[i] == "+") {
                float result = std::stof(expd[i-1]) + std::stof(expd[i+1]);
                expd.erase(expd.begin() + i + 1);
                expd.erase(expd.begin() + i);
                expd.erase(expd.begin() + i - 1);

                std::ostringstream fresult;
                int precision1 = post_dot_size(expd[i-1]);
                std::cout << "precisao: " << precision1 << "\n";
                int precision2 = post_dot_size(expd[i+1]);
                int final_precision = 0;

                if (precision1 > precision2) {
                    final_precision = precision1;
                } else if (precision2 > precision1) {
                    final_precision = precision1;
                } else {
                    final_precision = precision1;
                }

                fresult << std::fixed << std::setprecision(final_precision) << result;

                if (i-3) {
                    //expd.insert(expd.begin(), std::to_string(result));
                    expd.insert(expd.begin(), fresult.str());
                } else {
                    //expd.insert(expd.begin() + i - 1, std::to_string(result));
                    expd.insert(expd.begin() + i - 1, fresult.str());
                }
            } else if (expd[i] == "-") {
                float result = std::stof(expd[i-1]) - std::stof(expd[i+1]);
                expd.erase(expd.begin() + i + 1);
                expd.erase(expd.begin() + i);
                expd.erase(expd.begin() + i - 1);

                std::ostringstream fresult;
                int precision1 = post_dot_size(expd[i-1]);
                std::cout << "precisao: " << precision1 << "\n";
                int precision2 = post_dot_size(expd[i+1]);
                int final_precision = 0;

                if (precision1 > precision2) {
                    final_precision = precision1;
                } else if (precision2 > precision1) {
                    final_precision = precision1;
                } else {
                    final_precision = precision1;
                }

                fresult << std::fixed << std::setprecision(final_precision) << result;

                if (i-3) {
                    expd.insert(expd.begin(), fresult.str());
                } else {
                    expd.insert(expd.begin() + i - 1, fresult.str());
                }
            }
        }
    }

    return expd[0];
};

std::vector<std::string> Processor::split(std::string str, char separator) {
    std::vector<std::string> result;
    std::string current;

    for (auto c : str) {
        if (c != separator) {
            current += c;
        } else {
            if (!current.empty()) {
                result.push_back(current);
                current.clear();
            }
        }
    }

    if (!current.empty())
        result.push_back(current);

    return result;
}

int Processor::post_dot_size(std::string str) {
    bool control = false;
    for (auto e : str) {
        if (e == '.')
            control = true;
    }
    if (!control)
        return 1;

    int dot_index = str.find(".");

    int float_size = 0;

    for (size_t i = dot_index+1; i < str.size(); i++) {
        float_size += 1;
    }

    return float_size;
}