codigos_e = ["release", ">", "capture", "portal", "receive", "final", "calc"] # Gramática super complicada
codigos_p = ["print", "end_print", "input", "def", "var", "end", "operacao"]

memoria = [] # Eu vou simplesmente deixar o Python manejar a memória

programa = []

codigo = "release < information 1 information 2 > capture thisvar calc < 1 + 2 + 3 > final"
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
    if contador_print_debug < 3:
        print(word)
    
    contador_print_debug += 1

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
    elif word == "input":
        contador += 1
        var_para_input = programa[contador]
        input_value = input()
        memoria.append({input_value: var_para_input})
        contador += 1
        print(memoria)
    elif word == "operacao":
        contador += 2
        arg_op = programa[contador]
        print(f"Esse é o arg_op: {arg_op}")
        while arg_op != "end_print":
            pass 
    elif word == "end":
        break