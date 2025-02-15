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
                arg_list.append(memoria[arg_print])
            else:
                arg_list.append(arg_print)
            contador += 1
        arg_list.pop()
        print_string = " ".join(arg_list)
        print(print_string)
        contador -= 1
    elif word == "capture":
        contador += 1
        var_para_input = codigo_tokenizado[contador]
        input_value = input()
        memoria[var_para_input] = input_value
        contador += 1
    elif word == "sum":
        contador += 2
        arg_op = codigo_tokenizado[contador]
        temp = []
        while arg_op != ">": 
            arg_op = codigo_tokenizado[contador]
            if arg_op[0] == "$":
                var_nome = arg_op
            elif (arg_op != '>' and arg_op != "+"):
                temp.append(arg_op)
            contador += 1
        sum_list = []
        for i in temp:
            sum_list.append(float(i))
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
            elif (arg_op != '>' and arg_op != "-"):
                temp.append(arg_op)
            contador += 1
        subt_list = []
        for i in temp:
            subt_list.append(float(i))
        buffer = 0
        for i in subt_list:
            buffer -= i
        if buffer < 0:
            memoria[var_nome] = str( float(memoria[var_nome]) + buffer)
        else:
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
            elif (arg_op != '>' and arg_op != "*"):
                temp.append(arg_op)
            contador += 1
        mult_result = 1
        for i in temp:
            mult_result *= int(i)
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
            elif (arg_op != '>' and arg_op != "/"):
                temp.append(arg_op)
            contador += 1
        div_result = float(memoria[var_nome])
        for i in temp:
            div_result /= int(i)
        memoria[var_nome] = str(div_result)
        contador -= 1
    elif word == "receive":
        contador += 1
        var_nome = codigo_tokenizado[contador]
        contador += 2
        memoria[var_nome] = codigo_tokenizado[contador]
    elif word == "decide":
        contador_antes_if = contador
        contador += 1
        if codigo_tokenizado[contador][0] == "$":
            left_operand = memoria[codigo_tokenizado[contador]]
        else:
            left_operand = codigo_tokenizado[contador]
        contador += 1 
        comparator = codigo_tokenizado[contador]
        contador += 1
        if codigo_tokenizado[contador][0] == "$":
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
            result = int(left_operand) > int(right_operand)
        elif comparator == "lt":
            result = int(left_operand) < int(right_operand)
        elif comparator == "gte":
            result = int(left_operand) >= int(right_operand)
        else:
            result = int(left_operand) < int(right_operand)
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
        n_times_index = contador 
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
        possivel_index = contador + contador_words
        print(possivel_index)
        lista_repeat.pop()
        codigo_tokenizado.pop(contador + contador_words)
        for i in range(int(n_times) - 1):
            for palavra in lista_repeat:
                codigo_tokenizado.insert(possivel_index, palavra)
                possivel_index += 1
    elif word == "final":
        break
    contador += 1

codigo.close()