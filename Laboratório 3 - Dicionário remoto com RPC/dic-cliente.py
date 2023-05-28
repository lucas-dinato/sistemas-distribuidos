# Cliente de dicionario remoto usando RPyC
import rpyc

dic = rpyc.connect('localhost', 10000)
dicionario = dic.root.carregar_dicionario()

while True:
    op = input("Digite uma funcionalidade (consulta, escrita, remoção ou 'fim' para terminar): ")
    if op == 'fim':
        dic.close()
        break

    if op == 'consulta':
        chave = input("Chave: ")
        div = dic.root.consulta(chave)
        print(div)
    elif op == 'escrita':
        chave = input("Chave: ")
        valor = input("Valor: ")
        div = dic.root.escrita(chave, valor)
        print(div)
    if op == 'remocao' or op == 'remoção':
        chave = input("Chave: ")
        div = dic.root.remocao(chave)
        print(div)
