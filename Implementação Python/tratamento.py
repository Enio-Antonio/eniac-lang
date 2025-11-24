class Tratador:
    # def tratar_funcao(self, codigo_func: list, arg_list: list) -> list:
    #     # Substitui arg1, arg2 e etc. pelos argumentos passados na chamada
    #     controle = len(arg_list)
    #     contador = 0
    #     arg_index = 1
    #     for i in range(len(codigo_func)):
    #         if contador < controle:
    #             if codigo_func[i] == f"arg{arg_index}":
    #                 codigo_func[i] = arg_list[contador]
    #                 contador += 1
    #                 arg_index += 1

    #     return codigo_func

    def tratar_funcao(self, codigo_func: list, arg_list: list):
        # Substitui os arg's pelos argumentos passados na chamada
        for i in range(len(arg_list)):
            arg_index: int = i + 1
            for index in range(len(codigo_func)):
                if codigo_func[index] == f"arg{arg_index}":
                    codigo_func[index] = arg_list[i] 

        return codigo_func

    def calcular(self, expd: list) -> float:
        if len(expd) == 1:
            return float(expd[0])

        while '*' in expd or '/' in expd:
            for i in range(len(expd)):
                try:
                    if expd[i] == '*':
                        #print(f'valor de i aqui: {i-3}')
                        resultado = float(expd[i-1]) * float(expd[i+1])
                        expd.pop(i+1)
                        expd.pop(i)
                        expd.pop(i-1)
                        if (i-3) < 0:
                            expd.insert(0, str(resultado))
                        else:
                            expd.insert(i-1, str(resultado))
                except:
                    break
                try:
                    if expd[i] == '/':
                        resultado = float(expd[i-1]) / float(expd[i+1])
                        expd.pop(i+1)
                        expd.pop(i)
                        expd.pop(i-1)
                        if (i-1) < 0:
                            expd.insert(0, str(resultado))
                        else:
                            expd.insert(i-1, str(resultado))
                except:
                    break

        while '+' in expd or '-' in expd:
            for i in range(len(expd)):
                try:
                    if expd[i] == '+':
                        resultado = float(expd[i-1]) + float(expd[i+1])
                        expd.pop(i+1)
                        expd.pop(i)
                        expd.pop(i-1)
                        if (i-1) < 0:
                            expd.insert(0, str(resultado))
                        else:
                            expd.insert(i-1, str(resultado))
                except:
                    break
                try:
                    if expd[i] == '-':
                        resultado = float(expd[i-1]) - float(expd[i+1])
                        expd.pop(i+1)
                        expd.pop(i)
                        expd.pop(i-1)
                        if (i-1) < 0:
                            expd.insert(0, str(resultado))
                        else:
                            expd.insert(i-1, str(resultado))
                except:
                    break

        return expd[0]