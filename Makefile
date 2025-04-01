interpretador: interpretador.cpp
	g++ interpretador.cpp ./Auxiliar/dicionario.cpp -o eniac
	.\eniac codigo.ec