from sys import argv

nome_arquivo = argv[1]

# Tratando o arquivo
try:
    nome_arquivo.split(".")[1] != "ec"
except:
    raise Exception("Verifique se o arquivo.\n")

if nome_arquivo.split(".")[1] != "ec":
    raise Exception("A extensão do arquivo não é .ec\n")

# A keyword 'sum' não tem muito sentido se não for usada com um variável, dado que o resultado não será salva em nenhum lugar sem isso
codigos_e = ["release", ">", "capture", "portal", "receive", "final", "sum", "repeat_n_times"] # Gramática super complicada
codigos_p = ["print", "end_print", "input", "def", "var", "end", "somar", "loop"]

memoria = {} # Eu vou simplesmente deixar o Python manejar a memória

programa = []

codigo = open(nome_arquivo, 'r').read()
codigo_tokenizado = codigo.split()

for i in range(len(codigo_tokenizado)):
    if codigo_tokenizado[i] in codigos_e:
        for c in range(len(codigos_e)):
            if codigo_tokenizado[i] == codigos_e[c]:
                programa.append(codigos_p[c])
    else:
        programa.append(codigo_tokenizado[i])

print(programa)

contador = 0 
contador_print_debug = 0

while True:
    word = programa[contador]
    #print(f"Essa é a keyword: {word}")

    if word == "print":
        contador += 2
        arg_print = programa[contador]
        arg_list = []
        while arg_print != "end_print":
            arg_print = programa[contador]
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
        #print(f"Esse é o arg_op: {arg_op}")
        temp = []
        while arg_op != "end_print": 
            arg_op = programa[contador]
            if (arg_op != 'end_print' and arg_op != "+"):
                temp.append(arg_op)
            contador += 1
        print(f"Lista de numeros para somar: {temp}")
        contador -= 1
    elif word == "var":
        contador += 1
        var_nome = programa[contador]
        contador += 2
        memoria[var_nome] = programa[contador]
        contador += 1
        print(f"Esse é o nome da variável: {var_nome}")
        print(f"Esse é o valor da variável: {memoria[var_nome]}")
    elif word == "end":
        break
    contador += 1