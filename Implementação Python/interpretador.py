from sys import argv

if len(argv) == 1:
    print("Uso: python interpretador.py <arquivo>")
    raise SystemExit

nome_arquivo = argv[1]

# Tratando o arquivo
try:
    nome_arquivo.split(".")[1] != "ec"
except:
    print("ERRO: verifique se você digitou a extensão do arquivo.")
    raise SystemExit()

if nome_arquivo.split(".")[1] != "ec":
    print("ERRO: a extensão do arquivo não é .ec")
    raise SystemExit()

# A keyword 'sum' não tem muito sentido se não for usada com uma variável, dado que o resultado não será salvo em nenhum lugar sem isso
codigos_e = ["release", ">", "capture", "portal", "receive", "final", "sum", "repeat_n_times", "endr", "subt", "decide", "endd", "mult", "div"] # Gramática super complicada

memoria = {} # Eu vou simplesmente deixar o Python manejar a memória

codigo = open(nome_arquivo, 'r')
codigo_string = codigo.read()
codigo_tokenizado = codigo_string.split()
sub_rotinas = {}

if codigo_tokenizado[-1] != "final":
    print("ERRO: está faltando a palavra-chave 'final'")
    raise SystemExit()

if "decide" in codigo_tokenizado and "endd" not in codigo_tokenizado:
    print("ERRO: está faltando a palavra-chave 'endd'")
    raise SystemExit()

if "repeat_n_times" in codigo_tokenizado and "endr" not in codigo_tokenizado:
    print("ERRO: está faltando a palavra-chave 'endr'")
    raise SystemExit()

contador = 0 

while True:
    word = codigo_tokenizado[contador]

    if word == "release":
        contador += 2
        arg_print = codigo_tokenizado[contador]
        arg_list = []

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
        var_para_input = codigo_tokenizado[contador]
        input_value = input()
        memoria[var_para_input] = input_value

    elif word == "sum":
        contador += 2
        arg_op = codigo_tokenizado[contador]
        temp = []

        while arg_op != ">": 
            arg_op = codigo_tokenizado[contador]

            if arg_op[0] == "$":
                var_nome = arg_op
                if var_nome not in memoria.keys():
                    print(f"ERRO: variável não declarada: {var_nome}")
                    raise SystemExit()
            elif (arg_op != '>' and arg_op != "+"):
                if "-" == arg_op or "*" == arg_op or "/" == arg_op: 
                    print(f"sinal não suportado nessa operação: \"{arg_op}\"")
                    raise SystemExit()
                temp.append(arg_op)
            contador += 1

        if "-" in temp or "*" in temp or "/" in temp:
            print("Sinais não suportados para essa operação: '-', '*', '/'")
            raise SystemExit()

        sum_list = []

        for i in temp:
            try:
                sum_list.append(int(i))
            except:
                sum_list.append(float(i))
        try:
            memoria[var_nome] = str(int(memoria[var_nome]) + sum(sum_list))
        except:
            memoria[var_nome] = str(float(memoria[var_nome]) + sum(sum_list))
        contador -= 1

    elif word == "subt":
        contador += 2
        arg_op = codigo_tokenizado[contador]
        temp = []

        while arg_op != ">":
            arg_op = codigo_tokenizado[contador]

            if arg_op[0] == "$":
                var_nome = arg_op
                if var_nome not in memoria.keys():
                    print(f"ERRO: variável não declarada: {var_nome}")
                    raise SystemExit()
            elif (arg_op != '>' and arg_op != "-"):
                temp.append(arg_op)
            contador += 1

        subt_list = []

        for i in temp:
            try:
                subt_list.append(int(i))
            except:
                subt_list.append(float(i))

        buffer = 0

        for i in subt_list:
            buffer -= i

        if buffer < 0:
            try:
                memoria[var_nome] = str( int(memoria[var_nome]) + buffer)
            except:
                memoria[var_nome] = str( float(memoria[var_nome]) + buffer)
        else:
            try:
                memoria[var_nome] = str( int(memoria[var_nome]) - buffer )
            except:
                memoria[var_nome] = str( float(memoria[var_nome]) - buffer )

        contador -= 1

    elif word == "mult":
        contador += 2
        arg_op = codigo_tokenizado[contador]
        temp = []

        while arg_op != ">": 
            arg_op = codigo_tokenizado[contador]

            if arg_op[0] == "$":
                var_nome = arg_op
                if var_nome not in memoria.keys():
                    print(f"ERRO: variável não declarada: {var_nome}")
                    raise SystemExit()
            elif (arg_op != '>' and arg_op != "*"):
                temp.append(arg_op)
            contador += 1

        mult_result = 1

        for i in temp:
            try:
                mult_result *= int(i)
            except:
                mult_result *= float(i)

        try:
            memoria[var_nome] = str(int(memoria[var_nome]) * mult_result)
        except:
            memoria[var_nome] = str(float(memoria[var_nome]) * mult_result)
        contador -= 1

    elif word == "div":
        contador += 2
        arg_op = codigo_tokenizado[contador]
        temp = []

        while arg_op != ">": 
            arg_op = codigo_tokenizado[contador]

            if arg_op[0] == "$":
                var_nome = arg_op
                if var_nome not in memoria.keys():
                    print(f"ERRO: variável não declarada: {var_nome}")
                    raise SystemExit()
            elif (arg_op != '>' and arg_op != "/"):
                temp.append(arg_op)
            contador += 1

        try:
            div_result = int(memoria[var_nome])
        except:
            div_result = float(memoria[var_nome])

        for i in temp:
            try:
                div_result //= int(i)
            except:
                div_result /= float(i)

        memoria[var_nome] = str(div_result)
        contador -= 1

    elif word == "receive":
        contador += 1
        if codigo_tokenizado[contador][0] != "$":
            print("ERRO: está faltando o '$'.\n")
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
                print(f"ERRO: variável não declarada: {var_nome}")
                raise SystemExit()
            left_operand = memoria[codigo_tokenizado[contador]]
        else:
            left_operand = codigo_tokenizado[contador]

        contador += 1 
        comparator = codigo_tokenizado[contador]
        contador += 1

        if codigo_tokenizado[contador][0] == "$":
            if codigo_tokenizado[contador] not in memoria.keys():
                print(f"ERRO: variável não declarada: {var_nome}")
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

    elif word[0] == "$":
        var_nome = word
        contador += 2
        novo_valor = codigo_tokenizado[contador]
        if novo_valor in memoria.keys():
            memoria[var_nome] = memoria[novo_valor]
        else:
            memoria[var_nome] = novo_valor

    elif word == "portal":
        contador += 1
        lista_args = []
        # Funções serão tratadas como tipos especiais de variáveis
        func_nome = codigo_tokenizado[contador]
        # Testando se a função possui argumentos
        if func_nome.split("(")[1] == ")":
            contador += 1
            lista_rotina = []
            while codigo_tokenizado[contador] != "endp":
                if codigo_tokenizado[contador] != "endp":
                    lista_rotina.append(codigo_tokenizado[contador])
                contador += 1
        else:
            lista_args = []
            primeiro_arg = codigo_tokenizado[contador].split("(")[1]
            lista_args.append(primeiro_arg[0:len(primeiro_arg) - 1])
            contador += 1
            lista_args.append(codigo_tokenizado[contador][0:len(codigo_tokenizado[contador]) - 1])
            while codigo_tokenizado[contador][-1] != ")":
                contador += 1
                lista_args.append(codigo_tokenizado[contador][0:len(codigo_tokenizado[contador]) - 1])
            lista_rotina = []
            while codigo_tokenizado[contador] != "endp":
                if codigo_tokenizado[contador] != "endp":
                    lista_rotina.append(codigo_tokenizado[contador])
                contador += 1

            lista_rotina.pop(0)

        if len(lista_args) == 0:
            sub_rotinas[func_nome] = lista_rotina
        else: 
            sub_rotinas[func_nome.split("(")[0]] = [lista_rotina, lista_args]

    elif word in sub_rotinas.keys():
        func_codigo = sub_rotinas[word] 
        contador_aux = contador + 1
        for palavra in func_codigo:
            codigo_tokenizado.insert(contador_aux, palavra)
            contador_aux += 1

    elif word == "final":
        break
    contador += 1

codigo.close()