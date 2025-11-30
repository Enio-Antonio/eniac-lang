class Processor:
    def process_function(self, func_code: list, arg_list: list) -> list:
        # Substitui os arg's pelos argumentos passados na chamada
        for i in range(len(arg_list)):
            arg_index: int = i + 1
            for index in range(len(func_code)):
                if func_code[index] == f"arg{arg_index}":
                    func_code[index] = arg_list[i] 

        return func_code

    def calculate(self, expd: list) -> float:
        if len(expd) == 1:
            return float(expd[0])

        while '*' in expd or '/' in expd:
            for i in range(len(expd)):
                try:
                    if expd[i] == '*':
                        #print(f'valor de i aqui: {i-3}')
                        result = float(expd[i-1]) * float(expd[i+1])
                        expd.pop(i+1)
                        expd.pop(i)
                        expd.pop(i-1)
                        if (i-3) < 0:
                            expd.insert(0, str(result))
                        else:
                            expd.insert(i-1, str(result))
                except:
                    break
                try:
                    if expd[i] == '/':
                        result = float(expd[i-1]) / float(expd[i+1])
                        expd.pop(i+1)
                        expd.pop(i)
                        expd.pop(i-1)
                        if (i-1) < 0:
                            expd.insert(0, str(result))
                        else:
                            expd.insert(i-1, str(result))
                except:
                    break

        while '+' in expd or '-' in expd:
            for i in range(len(expd)):
                try:
                    if expd[i] == '+':
                        result = float(expd[i-1]) + float(expd[i+1])
                        expd.pop(i+1)
                        expd.pop(i)
                        expd.pop(i-1)
                        if (i-1) < 0:
                            expd.insert(0, str(result))
                        else:
                            expd.insert(i-1, str(result))
                except:
                    break
                try:
                    if expd[i] == '-':
                        result = float(expd[i-1]) - float(expd[i+1])
                        expd.pop(i+1)
                        expd.pop(i)
                        expd.pop(i-1)
                        if (i-1) < 0:
                            expd.insert(0, str(result))
                        else:
                            expd.insert(i-1, str(result))
                except:
                    break

        return expd[0]