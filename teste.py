programa = ['if', '10', 'eq', '10', 'print', '<', 'Dentro', 'do', 'end_print', 'endd', 'print', '<', 'Depois', 'do', 'end_print', 'end']

contador = 0

contador_antes_if = contador
contador += 1
left_operand = programa[contador]
contador += 1 
comparator = programa[contador]
contador += 1
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
    print(programa[contador_antes_if])
    programa.pop(contador_antes_if)
    print(programa[contador_antes_if])
    programa.pop(contador_antes_if)
    print(programa[contador_antes_if])
    programa.pop(contador_antes_if)
    print(programa[contador_antes_if])
    programa.pop(contador_antes_if)
else:
    contador += contador_words - 1

print(programa)