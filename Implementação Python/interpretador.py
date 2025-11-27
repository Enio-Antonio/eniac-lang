from sys import argv

from tratamento import Tratador

if len(argv) == 1:
    print("Uso: python interpretador.py <arquivo>")
    raise SystemExit

nome_arquivo: str = argv[1]

# Tratando o arquivo
try:
    _ = nome_arquivo.split(".")[1] != "ec"
except:
    print("ERRO: verifique a extensão do arquivo.")
    raise SystemExit()

if nome_arquivo.split(".")[1] != "ec":
    print("ERRO: a extensão do arquivo não é .ec")
    raise SystemExit()

codigos_e: list = ["release", ">", "capture", "portal", "receive", "final", "repeat_n_times", "endr", "decide", "endd"] # Gramática super complicada

processador = Tratador()

codigo = open(nome_arquivo, 'r')
codigo_string: str = codigo.read()
codigo_tokenizado: list = codigo_string.split()
funcoes: dict = {}

if codigo_tokenizado[-1] != "final":
    print("ERRO: está faltando a palavra-chave 'final'")
    raise SystemExit()

if "decide" in codigo_tokenizado and "endd" not in codigo_tokenizado:
    print("ERRO: está faltando a palavra-chave 'endd'")
    raise SystemExit()

if "repeat_n_times" in codigo_tokenizado and "endr" not in codigo_tokenizado:
    print("ERRO: está faltando a palavra-chave 'endr'")
    raise SystemExit()

def interpretar(codigo_tokenizado: list) -> None:
    contador: int = 0

    memoria: dict = {} # Eu vou simplesmente deixar o Python manejar a memória

    while True:
        word: str = codigo_tokenizado[contador]

        if word == "release":
            contador += 2
            arg_print: str = codigo_tokenizado[contador]
            arg_list: list = []

            while arg_print != ">":
                arg_print = codigo_tokenizado[contador]

                if arg_print[0] == "$":
                    try:
                        arg_list.append(memoria[arg_print])
                    except:
                        print(f"ERRO: variável não declarada: {arg_print}")
                        raise SystemExit()
                else:
                    arg_list.append(arg_print)
                contador += 1

            arg_list.pop()
            print_string = " ".join(arg_list)
            for linha in print_string.split("\\n"):
                print(linha)
            contador -= 1

        elif word == "capture":
            contador += 1
            if codigo_tokenizado[contador][0] != "$":
                print(f"ERRO: está faltando o '$' em '{codigo_tokenizado[contador]}'.")
                raise SystemExit()
            var_para_input: str = codigo_tokenizado[contador]
            input_value: str = input()
            memoria[var_para_input] = input_value

        elif word[0] == '$':
            var_nome: str = word
            contador += 2
            arg_list = []
            while codigo_tokenizado[contador] not in codigos_e and not (codigo_tokenizado[contador][0] == '$' and codigo_tokenizado[contador+1] == '='): 
                if codigo_tokenizado[contador] in memoria.keys():
                    arg_list.append(memoria[codigo_tokenizado[contador]])
                else:
                    arg_list.append(codigo_tokenizado[contador])
                contador += 1
            contador -= 1

            if len(arg_list) == 1:
                memoria[var_nome] = arg_list[0]
            else:
                resultado = processador.calcular(arg_list)
                memoria[var_nome] = resultado

        elif word == "receive":
            contador += 1
            if codigo_tokenizado[contador][0] != "$":
                print(f"ERRO: está faltando o '$' em {codigo_tokenizado[contador]}.")
                raise SystemExit()
            var_nome = codigo_tokenizado[contador]
            contador += 2
            if codigo_tokenizado[contador][0] == "$":
                if codigo_tokenizado[contador] in memoria.keys():
                    memoria[var_nome] = memoria[codigo_tokenizado[contador]]
                else:
                    print(f"ERRO:: variável não declarada: {codigo_tokenizado[contador]}")
                    raise SystemExit()
            else:
                memoria[var_nome] = codigo_tokenizado[contador]

        elif word == "decide":
            contador_antes_if = contador
            contador += 1

            if codigo_tokenizado[contador][0] == "$":
                if codigo_tokenizado[contador] not in memoria.keys():
                    print(f"ERRO: variável não declarada: {codigo_tokenizado[contador]}")
                    raise SystemExit()
                left_operand = memoria[codigo_tokenizado[contador]]
            else:
                left_operand = codigo_tokenizado[contador]

            contador += 1 
            comparator = codigo_tokenizado[contador]
            contador += 1

            if codigo_tokenizado[contador][0] == "$":
                if codigo_tokenizado[contador] not in memoria.keys():
                    print(f"ERRO: variável não declarada: {codigo_tokenizado[contador]}")
                    raise SystemExit()
                right_operand = memoria[codigo_tokenizado[contador]]
            else:
                right_operand = codigo_tokenizado[contador]

            contador_words = 0
            contador_aux = contador
            temp = ""

            while temp != "endd":
                contador_aux += 1
                temp = codigo_tokenizado[contador_aux]
                contador_words += 1

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


            if result:
                codigo_tokenizado.pop(contador_antes_if)
                codigo_tokenizado.pop(contador_antes_if)
                codigo_tokenizado.pop(contador_antes_if)
                codigo_tokenizado.pop(contador_antes_if)
                codigo_tokenizado.pop(contador + contador_words - 4) # 4 é uma correção por causa dos 4 .pop's
                contador = contador_antes_if - 1 # Não lembro o pq desse contador receber -1
            else:
                contador += contador_words - 1

        elif word == "repeat_n_times":
            contador_repeat = contador
            contador += 1
            if codigo_tokenizado[contador][0] == "$":
                if codigo_tokenizado[contador] not in memoria.keys():
                    print(f"ERRO: variável não declarada: {codigo_tokenizado[contador]}")
                    raise SystemExit()
                n_times = memoria[codigo_tokenizado[contador]]
            else:
                n_times = codigo_tokenizado[contador]
            contador += 1
            contador_aux = contador
            contador_words = 0
            temp = ""
            lista_repeat = []

            while temp != "endr":
                temp = codigo_tokenizado[contador_aux]
                lista_repeat.append(temp)
                contador_aux += 1
                contador_words += 1

            codigo_tokenizado.pop(contador_repeat)
            codigo_tokenizado.pop(contador_repeat)
            contador -= 3 # Correção por causa dos .pop's
            p_index = contador + contador_words
            lista_repeat.pop()
            codigo_tokenizado.pop(contador + contador_words)

            for i in range(int(n_times) - 1):
                for palavra in lista_repeat:
                    codigo_tokenizado.insert(p_index, palavra)
                    p_index += 1 

        elif word == "portal":
            contador += 1
            func_nome: str = codigo_tokenizado[contador]
            if func_nome[0] != '@':
                print(f"ERRO: nomes de funções devem iniciar com `@`: {func_nome}")
            contador += 1
            lista_rotina = []
            while codigo_tokenizado[contador] != "endp":
                if codigo_tokenizado[contador] != "endp":
                    lista_rotina.append(codigo_tokenizado[contador])
                contador += 1
            lista_rotina.append("final")

            funcoes[func_nome] = lista_rotina
            
        elif word[0] == '@':
            nome_func = word
            contador += 1

            if codigo_tokenizado[contador] == "|":
                contador += 1
                lista_args: list = []
                while codigo_tokenizado[contador] != "|":
                    lista_args.append(codigo_tokenizado[contador])
                    contador += 1
                funcao_tratada: list = processador.tratar_funcao(funcoes[nome_func], lista_args)
                interpretar(funcao_tratada)

            else:
               print(f"ERRO: chamada de função inválida: `{nome_func} | none |` ou `{nome_func} | args... |`")
               raise SystemExit
            
        elif word == "final":
            break
        contador += 1

interpretar(codigo_tokenizado)

codigo.close()