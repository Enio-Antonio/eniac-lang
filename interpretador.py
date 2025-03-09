from sys import argv

nome_arquivo = argv[1]

# Tratando o arquivo
try:
    nome_arquivo.split(".")[1] != "ec"
except:
    raise Exception("Verifique se você digitou a extensão do arquivo.\n")

if nome_arquivo.split(".")[1] != "ec":
    raise Exception("A extensão do arquivo não é .ec\n")

# A keyword 'sum' não tem muito sentido se não for usada com um variável, dado que o resultado não será salva em nenhum lugar sem isso
codigos_e = ["release", ">", "capture", "portal", "receive", "final", "sum", "repeat_n_times", "endr", "subt", "decide", "end_decideb", "mult", "div"] # Gramática super complicada

memoria = {} # Eu vou simplesmente deixar o Python manejar a memória

codigo = open(nome_arquivo, 'r')
codigo_string = codigo.read()
codigo_tokenizado = codigo_string.split()

if codigo_tokenizado[-1] != "final":
    raise Exception("Está faltando a palavra-chave 'final'")

if "decide" in codigo_tokenizado and "endd" not in codigo_tokenizado:
    raise Exception("Está faltando a palavra-chave 'endd'")

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
                    print("Chegou na excessão?")
                    raise Exception(f"variável não declarada: {arg_print}\n")
            else:
                arg_list.append(arg_print)
            contador += 1

        arg_list.pop()
        print_string = " ".join(arg_list)
        print(print_string)
        contador -= 1

    elif word == "capture":
        contador += 1
        if codigo_tokenizado[contador][0] != "$":
            raise Exception("está faltando o '$'.")
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
                    raise Exception(f"variável não declarada: {var_nome}")
            elif (arg_op != '>' and arg_op != "+"):
                if "-" == arg_op or "*" == arg_op or "/" == arg_op: 
                    raise Exception(f"sinal não suportado nessa operação: \"{arg_op}\"")
                temp.append(arg_op)
            contador += 1

        if "-" in temp or "*" in temp or "/" in temp:
            raise Exception("Sinais não suportados para essa operação: '-', '*', '/'")

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
                    raise Exception(f"variável não declarada: {var_nome}")
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
                    raise Exception(f"variável não declarada: {var_nome}")
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
                    raise Exception(f"variável não declarada: {var_nome}")
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
            raise Exception("está faltando o '$'.\n")
        var_nome = codigo_tokenizado[contador]
        contador += 2
        memoria[var_nome] = codigo_tokenizado[contador]

    elif word == "decide":
        contador_antes_if = contador
        contador += 1

        if codigo_tokenizado[contador][0] == "$":
            if codigo_tokenizado[contador] not in memoria.keys():
                raise Exception(f"variável não declarada: {var_nome}")
            left_operand = memoria[codigo_tokenizado[contador]]
        else:
            left_operand = codigo_tokenizado[contador]

        contador += 1 
        comparator = codigo_tokenizado[contador]
        contador += 1

        if codigo_tokenizado[contador][0] == "$":
            if codigo_tokenizado[contador] not in memoria.keys():
                raise Exception(f"variável não declarada: {var_nome}")
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

    elif word == "final":
        break
    contador += 1

codigo.close()