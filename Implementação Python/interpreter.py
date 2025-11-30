from sys import argv

from processor import Processor

if len(argv) == 1:
    print("Usage: python interpreter.py <file>")
    raise SystemExit

filename: str = argv[1]

# Tratando o arquivo
try:
    _ = filename.split(".")[1] != "ec"
except:
    print("ERROR: see file extension.")
    raise SystemExit()

if filename.split(".")[1] != "ec":
    print("ERROR: file extension must be .ec")
    raise SystemExit()

e_code: list = ["release", ">", "capture", "portal", "receive", "final", "repeat_n_times", "endr", "decide", "endd"] # Gramática super complicada

processor = Processor()

code = open(filename, 'r')
string_code: str = code.read()
tokenized_code: list = string_code.split()
functions: dict = {}

if tokenized_code[-1] != "final":
    print("ERROR: missing keyword 'final'")
    raise SystemExit()

if "decide" in tokenized_code and "endd" not in tokenized_code:
    print("ERROR: missing keyword 'endd'")
    raise SystemExit()

if "repeat_n_times" in tokenized_code and "endr" not in tokenized_code:
    print("ERROR: missing keyword 'endr'")
    raise SystemExit()

def interpret(tokenized_code: list) -> None:
    counter: int = 0

    memory: dict = {} # Eu vou simplesmente deixar o Python manejar a memória

    while True:
        word: str = tokenized_code[counter]

        if word == "release":
            counter += 2
            arg_print: str = tokenized_code[counter]
            arg_list: list = []

            while arg_print != ">":
                arg_print = tokenized_code[counter]

                if arg_print[0] == "$":
                    try:
                        arg_list.append(memory[arg_print])
                    except:
                        print(f"ERROR: non declared variable: {arg_print}")
                        raise SystemExit()
                else:
                    arg_list.append(arg_print)
                counter += 1

            arg_list.pop()
            print_string = " ".join(arg_list)
            for line in print_string.split("\\n"):
                print(line)
            counter -= 1

        elif word == "capture":
            counter += 1
            if tokenized_code[counter][0] != "$":
                print(f"ERROR: missing '$' in '{tokenized_code[counter]}'.")
                raise SystemExit()
            input_var: str = tokenized_code[counter]
            input_value: str = input()
            memory[input_var] = input_value

        elif word[0] == '$':
            var_name: str = word
            counter += 2
            arg_list = []
            while tokenized_code[counter] not in e_code and not (tokenized_code[counter][0] == '$' and tokenized_code[counter+1] == '='): 
                if tokenized_code[counter] in memory.keys():
                    arg_list.append(memory[tokenized_code[counter]])
                else:
                    arg_list.append(tokenized_code[counter])
                counter += 1
            counter -= 1

            if len(arg_list) == 1:
                memory[var_name] = arg_list[0]
            else:
                result = processor.calculate(arg_list)
                memory[var_name] = result

        elif word == "receive":
            counter += 1
            if tokenized_code[counter][0] != "$":
                print(f"ERROR: missing '$' in {tokenized_code[counter]}.")
                raise SystemExit()
            var_name = tokenized_code[counter]
            counter += 2
            if tokenized_code[counter][0] == "$":
                if tokenized_code[counter] in memory.keys():
                    memory[var_name] = memory[tokenized_code[counter]]
                else:
                    print(f"ERROR: non declared variable: {tokenized_code[counter]}")
                    raise SystemExit()
            else:
                memory[var_name] = tokenized_code[counter]

        elif word == "decide":
            counter += 1

            if tokenized_code[counter][0] == "$":
                if tokenized_code[counter] not in memory.keys():
                    print(f"ERROR: non declared variable: {tokenized_code[counter]}")
                    raise SystemExit()
                left_operand = memory[tokenized_code[counter]]
            else:
                left_operand = tokenized_code[counter]

            counter += 1 
            comparator = tokenized_code[counter]
            counter += 1

            if tokenized_code[counter][0] == "$":
                if tokenized_code[counter] not in memory.keys():
                    print(f"ERROR: non declared variable: {tokenized_code[counter]}")
                    raise SystemExit()
                right_operand = memory[tokenized_code[counter]]
            else:
                right_operand = tokenized_code[counter]

            counter_words = 0
            counter_aux = counter
            temp = ""

            while temp != "endd":
                counter_aux += 1
                temp = tokenized_code[counter_aux]
                counter_words += 1

            if comparator == "eq":
                result = left_operand == right_operand
            elif comparator == "gt":
                try:
                    result = int(left_operand) > int(right_operand)
                except:
                    result = float(left_operand) > float(right_operand)
            elif comparator == "lt":
                try:
                    result = int(left_operand) < int(right_operand)
                except:
                    result = float(left_operand) < float(right_operand)
            elif comparator == "gte":
                try:
                    result = int(left_operand) >= int(right_operand)
                except:
                    result = float(left_operand) >= float(right_operand)
            else:
                try:
                    result = int(left_operand) < int(right_operand)
                except:
                    result = float(left_operand) < float(right_operand)


            if not result: 
                counter += counter_words - 1

        elif word == "repeat_n_times":
            counter_repeat = counter
            counter += 1
            if tokenized_code[counter][0] == "$":
                if tokenized_code[counter] not in memory.keys():
                    print(f"ERROR: non declared variable: {tokenized_code[counter]}")
                    raise SystemExit()
                n_times = memory[tokenized_code[counter]]
            else:
                n_times = tokenized_code[counter]
            counter += 1
            counter_aux = counter
            counter_words = 0
            temp = ""
            repeat_list = []

            while temp != "endr":
                temp = tokenized_code[counter_aux]
                repeat_list.append(temp)
                counter_aux += 1
                counter_words += 1

            tokenized_code.pop(counter_repeat)
            tokenized_code.pop(counter_repeat)
            counter -= 3 # Correção por causa dos .pop's
            p_index = counter + counter_words
            repeat_list.pop()
            tokenized_code.pop(counter + counter_words)

            for _ in range(int(n_times) - 1):
                for element in repeat_list:
                    tokenized_code.insert(p_index, element)
                    p_index += 1 

        elif word == "portal":
            counter += 1
            func_name: str = tokenized_code[counter]
            if func_name[0] != '@':
                print(f"ERROR: function names must start with `@`: {func_name}")
            counter += 1
            func_list = []
            while tokenized_code[counter] != "endp":
                if tokenized_code[counter] != "endp":
                    func_list.append(tokenized_code[counter])
                counter += 1
            func_list.append("final")

            functions[func_name] = func_list
            
        elif word[0] == '@':
            func_name: str = word
            counter += 1

            if tokenized_code[counter] == "|":
                counter += 1
                lista_args: list = []
                while tokenized_code[counter] != "|":
                    lista_args.append(tokenized_code[counter])
                    counter += 1
                processed_func: list = processor.process_function(functions[func_name], lista_args)
                interpret(processed_func)
            else:
                interpret(functions[func_name])
                counter -= 1

        elif word == "final":
            break
        counter += 1

interpret(tokenized_code)

code.close()