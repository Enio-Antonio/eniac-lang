# Fiz uma linguagem de programação em Python KKKKKKKKKKK
ENIAC é uma homenagem ao que, por alguns, é considerado o primeiro computador moderno já feito. No entanto, como linguagem, não possui nenhuma utilidade real e é somente um projeto feito para diversão. Isso é lógico.
Com tantas linguagens feitas por pessoas altamente capacitadas e, principalmente, com objetivos reais, por que alguém usaria esse pequeno projeto? Eu só consigo pensar em uma razão: ver como eu fiz e tentar replicar.

Caso surja a vontade de testa-la, basta executar o script e passar o arquivo com o código na linha de comando. A extensão deve ser '.ec'.

Exemplo: ``` python interpretador.py codigo.ec ```

# Exemplos:
```
release < Hello, world! >
capture $numero
release < Esse é o número: $numero >
receive $numero_2 = 0
final
```

```
receive $num1 = 10
receive $num2 = 10

decide $num1 eq $num2
    release < Os dois são iguais >
end_decideb

final
```

```
release < Não precisa pular linhas >
receive $t1 = teste1 release < $t1 > receive $t2 = teste2  release $t2 final
```

# Lista de palavras-chave:
* _release_ < [args] > | Operação de output (print).
* _receive_ $nomevar = [valor] | Declarar uma variável. O $ é obrigatório.
* _capture_ $var | Operação de input.
* _final_ | Finaliza o programa (obrigatório).
* _sum_ < $var + x + y + ... > | Faz a operação de soma com a variável.
* _subt_ < $var - x - y - ... > | Faz a operação de subtração com a variável.
* _mult_ < $var * x * y * ... > | Faz a operação de multiplicação com a variável
* _div_ < $var / x / y / ... > | Faz a operação de divisão com a variável.
* _decide_ [valor] _operador_ [valor] end_decideb | Estrutura de decisão (if).
* _eq_ | Igual.
* _gt_ | Maior que.
* _lt_ | Menor que.
* _gte_ | Maior ou igual que.
* _lte_ | Menor ou igual que.

# Lista de implementação futura:
- Implementar em C++.
- Facilitar a operação em variáveis sem o uso de palavras-chave.
- Implementar tipos.
- Quebra de linha.
- Comentários.
- Estruturas de repetição.
- Estruturas de dados (vetores serão os primeiros).
