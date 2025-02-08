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
codigos_e = ["release", ">", "capture", "portal", "receive", "final", "sum", "repeat_n_times", "subt", "decide", "end_decideb", "mult", "div"] # Gramática super complicada
codigos_p = ["print", "end_print", "input", "def", "var", "end", "somar", "loop", "subtrair", "if", "endd", "multiplicar", "dividir"]

memoria = {} # Eu vou simplesmente deixar o Python manejar a memória

programa = []

codigo = open(nome_arquivo, 'r')
codigo_string = codigo.read()
codigo_tokenizado = codigo_string.split()

for i in range(len(codigo_tokenizado)):
    if codigo_tokenizado[i] in codigos_e:
        for c in range(len(codigos_e)):
            if codigo_tokenizado[i] == codigos_e[c]:
                programa.append(codigos_p[c])
    else:
        programa.append(codigo_tokenizado[i])

if programa[-1] != "end":
    raise Exception("Está faltando a palavra-chave 'final'")

if "if" in programa and "endd" not in programa:
    raise Exception("Está faltando a palavra-chave 'end_decideb'")

contador = 0 

while True:
    word = programa[contador]

    if word == "print":
        contador += 2
        arg_print = programa[contador]
        arg_list = []
        while arg_print != "end_print":
            arg_print = programa[contador]
            if arg_print[0] == "$":
                arg_list.append(memoria[arg_print])
            else:
                arg_list.append(arg_print)
            contador += 1
        arg_list.pop()
        print_string = " ".join(arg_list)
        print(print_string)
        contador -= 1
    elif word == "input":
        contador += 1
        var_para_input = programa[contador]
        input_value = input()
        memoria[var_para_input] = input_value
        contador += 1
    elif word == "somar":
        contador += 2
        arg_op = programa[contador]
        temp = []
        while arg_op != "end_print": 
            arg_op = programa[contador]
            if arg_op[0] == "$":
                var_nome = arg_op
            elif (arg_op != 'end_print' and arg_op != "+"):
                temp.append(arg_op)
            contador += 1
        sum_list = []
        for i in temp:
            sum_list.append(float(i))
        memoria[var_nome] = str(float(memoria[var_nome]) + sum(sum_list))
        contador -= 1
    elif word == "subtrair":
        contador += 2
        arg_op = programa[contador]
        temp = []
        while arg_op != "end_print":
            arg_op = programa[contador]
            if arg_op[0] == "$":
                var_nome = arg_op
            elif (arg_op != 'end_print' and arg_op != "-"):
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
    elif word == "multiplicar":
        contador += 2
        arg_op = programa[contador]
        temp = []
        while arg_op != "end_print": 
            arg_op = programa[contador]
            if arg_op[0] == "$":
                var_nome = arg_op
            elif (arg_op != 'end_print' and arg_op != "*"):
                temp.append(arg_op)
            contador += 1
        mult_result = 1
        for i in temp:
            mult_result *= int(i)
        memoria[var_nome] = str(float(memoria[var_nome]) * mult_result)
        contador -= 1
    elif word == "dividir":
        contador += 2
        arg_op = programa[contador]
        temp = []
        while arg_op != "end_print": 
            arg_op = programa[contador]
            if arg_op[0] == "$":
                var_nome = arg_op
            elif (arg_op != 'end_print' and arg_op != "/"):
                temp.append(arg_op)
            contador += 1
        div_result = float(memoria[var_nome])
        for i in temp:
            div_result /= int(i)
        memoria[var_nome] = str(div_result)
        contador -= 1
    elif word == "var":
        contador += 1
        var_nome = programa[contador]
        contador += 2
        memoria[var_nome] = programa[contador]
    elif word == "if":
        contador_antes_if = contador
        contador += 1
        if programa[contador][0] == "$":
            left_operand = memoria[programa[contador]]
        else:
            left_operand = programa[contador]
        contador += 1 
        comparator = programa[contador]
        contador += 1
        if programa[contador][0] == "$":
            right_operand = memoria[programa[contador]]
        else:
            right_operand = programa[contador]
        contador_words = 0
        contador_aux = contador
        temp = ""
        while temp != "endd":
            contador_aux += 1
            temp = programa[contador_aux]
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
            programa.pop(contador_antes_if)
            programa.pop(contador_antes_if)
            programa.pop(contador_antes_if)
            programa.pop(contador_antes_if)
            programa.pop(contador + contador_words - 4) # 4 é uma correção por causa dos 4 .pop's
            # contador -= 1 Não lembro o pq desse contador receber -1
            contador = contador_antes_if - 1
        else:
            contador += contador_words - 1
    elif word == "end":
        break
    contador += 1

codigo.close()