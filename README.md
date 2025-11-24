## (LEGADO) Fiz uma linguagem de programação em Python KKKKKKKKKKK
ENIAC é uma homenagem ao que, por alguns, é considerado o primeiro computador moderno já feito. No entanto, como linguagem, não possui nenhuma utilidade real e é somente um projeto feito para diversão. Isso é lógico.
Com tantas linguagens feitas por pessoas altamente capacitadas e, principalmente, com objetivos reais, por que alguém usaria esse pequeno projeto? Eu só consigo pensar em uma razão: ver como eu fiz e tentar replicar.

Caso surja a vontade de testa-la, basta executar o script e passar o arquivo com o código na linha de comando. A extensão deve ser '.ec'.

Exemplo: ``` python interpretador.py codigo.ec ```

## Índice
* [C++](#c)
* [Exemplos](#exemplos)
* [Lista de *keywords*](#lista-de-palavras-chave)
* [Implementações futuras](#lista-de-implementação-futura)

## C++
A implementação foi feita em C++ e Python ficará como documentação de protótipo.

Portanto, agora será necessário um compilador C/C++.

Para comodidade, foi feito uma Makefile:

```bash
make
./eniac.exe codigo.ec
```

Após compilado, também é possível mover o caminho do executável para as variáveis de ambiente e não ser necessário o "./".

## Exemplos:
```
release < Hello, world! >
capture $numero
release < Esse é o número: $numero >
final
```

```
receive $num1 = 10
receive $num2 = 10

decide $num1 eq $num2
    release < Os dois são iguais >
endd

final
```

```
release < Não precisa pular linhas >
receive $t1 = teste1 release < $t1 > receive $t2 = teste2  release $t2 final
```

```
receive $times = 5
receive $i = 0

repeat_n_times $times
    $i = $i + 1
    release < $i >
endr

final
```

```
portal print_hello_5_times 
    repeat_n_times 5
        release < Hello >
    endr
endp

print_hello_5_times | none |

final
```

```
portal somar
    $result = arg1 + arg2
    release < $result >
endp

somar | 1  1 |

final
```

## Lista de palavras-chave:
* _release_ < [args] > | Operação de output (print).
* _receive_ $var = [valor] | Declarar uma variável. O \$ é obrigatório.
* _capture_ $var | Operação de input.
* _final_ | Finaliza o programa (obrigatório).
* _decide_ [valor] _operador_ [valor] ... _endd_ | Estrutura de decisão (if).
* _eq_ | Igual.
* _gt_ | Maior que.
* _lt_ | Menor que.
* _gte_ | Maior ou igual que.
* _lte_ | Menor ou igual que.
* _repeat\_n\_times_ [times] ... _endr_ | Estrutura de repetição.
* _portal_ [nome_func] | _arg1_ _arg2_ _etc.._ | ... _endp_ | Funções.

## Lista de implementação futura:
- Implementar em C++. 👍
- Facilitar a operação em variáveis sem o uso de palavras-chave. 👍
- Implementar tipos.
- Quebra de linha. 👍
- Comentários.
- Estruturas de repetição. 👍
- Estruturas de dados (listas serão as primeiras).
- Escopo para variáveis.
