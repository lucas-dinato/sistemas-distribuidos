# servidor de echo: lado servidor
# com finalizacao do lado do servidor
# com multithreading (usa join para esperar as threads terminarem apos digitar 'fim' no servidor)
import socket
import sys
import threading

import select
import json

# define a localizacao do servidor
HOST = ''  # vazio indica que podera receber requisicoes a partir de qq interface de rede da maquina
PORT = 10000  # porta de acesso

# define o arquivo para salvar o dicionario
DICIONARIO_FILE = 'dicionario.json'
dicionario = []

# define a lista de I/O de interesse (jah inclui a entrada padrao)
entradas = [sys.stdin]
# armazena historico de conexoes
conexoes = {}

def iniciaServidor():
    global entradas
    '''Cria um socket de servidor e o coloca em modo de espera por conexoes
	Saida: o socket criado'''
    # cria o socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)  # Internet( IPv4 + TCP)

    # vincula a localizacao do servidor
    sock.bind((HOST, PORT))

    # coloca-se em modo de espera por conexoes
    sock.listen(5)

    # configura o socket para o modo nao-bloqueante
    sock.setblocking(False)

    # inclui o socket principal na lista de entradas de interesse
    entradas.append(sock)

    return sock


def aceitaConexao(sock):
    '''Aceita o pedido de conexao de um cliente
	Entrada: o socket do servidor
	Saida: o novo socket da conexao e o endereco do cliente'''

    # estabelece conexao com o proximo cliente
    clisock, endr = sock.accept()

    # registra a nova conexao
    conexoes[clisock] = endr

    return clisock, endr


def carregarDicionario():
    '''Carrega o dicionario do arquivo JSON, ou cria um novo arquivo se ele nao existir'''
    try:
        with open(DICIONARIO_FILE, 'r') as f:
            dicionario = json.load(f)
    except FileNotFoundError:
        dicionario = []
    return dicionario


def salvarDicionario(dicionario):
    '''Atualiza o dicionario remoto no arquivo JSON'''
    with open(DICIONARIO_FILE, 'w') as f:
        json.dump(dicionario, f)

def consulta(chave):
    for chave_valores in dicionario:
        if chave in chave_valores:
            valores = chave_valores[chave]
            return chave + " -> " + str(valores)
    return chave + " -> " + str([])

def escrita(chave, valor):
    global dicionario
    for chave_valores in dicionario:
        if chave in chave_valores:
            chave_valores[chave].append(valor)
            chave_valores[chave].sort()
            salvarDicionario(dicionario)  # atualiza o dicionario com o novo valor no arquivo
            valores = chave_valores[chave]
            return chave + " -> " + str(valores)
    nova_chave = {chave: [valor]}
    dicionario.append(nova_chave)
    salvarDicionario(dicionario)  # atualiza o dicionario com o novo valor no arquivo
    return chave + " -> " + str([valor])

def remover(chave):
    for i, d in enumerate(dicionario):
        for _ in d:
            if chave in d:
                dicionario.pop(i)
                salvarDicionario(dicionario)  # atualiza o dicionario com a chave removida no arquivo
                return "Chave " + chave + " removida."
    return "Chave " + chave + " não encontrada."


def lerMensagem(mensagem):
    partes = mensagem.strip().split(',')
    if len(partes) == 1:
        return consulta(partes[0])
    if len(partes) == 2:
        return escrita(partes[0], partes[1])

def atendeRequisicoes(clisock, endr):
    '''Recebe mensagens e as envia de volta para o cliente (ate o cliente finalizar)
    Entrada: socket da conexao e endereco do cliente
    Saida: '''
    clisock.setblocking(True)
    while True:
        # verifica se o socket ainda está presente na lista de conexões
        if clisock not in conexoes:
            print(str(endr) + ' -> encerrou')
            clisock.close()  # encerra a conexao com o cliente
            return
        try:
            # recebe dados do cliente
            data = clisock.recv(1024)
            if not data:  # dados vazios: cliente encerrou
                print(str(endr) + ' -> encerrou')
                clisock.close()  # encerra a conexao com o cliente
                return
            retorno = lerMensagem(str(data, encoding='utf-8'))
            print(str(endr) + ': ' + str(data, encoding='utf-8'))
            clisock.send(retorno.encode('utf-8'))  # ecoa os dados para o cliente
        except OSError as e:
            if e.errno == 10038:
                # o socket foi fechado por outra thread
                print(str(endr) + ' -> encerrou')
                clisock.close()
                return
            else:
                raise e


def main():
    '''Inicializa e implementa o loop principal (infinito) do servidor'''
    clientes = []  # armazena as threads criadas para fazer join
    sock = iniciaServidor()
    # carrega o dicionario a partir do JSON
    global dicionario
    dicionario = carregarDicionario()
    print("Pronto para receber conexoes...")
    while True:
        # espera por qualquer entrada de interesse
        leitura, escrita, excecao = select.select(entradas, [], [])
        # tratar todas as entradas prontas
        for pronto in leitura:
            if pronto == sock:  # pedido novo de conexao
                clisock, endr = aceitaConexao(sock)
                print('Conectado com: ', endr)
                # cria nova thread para atender o cliente
                cliente = threading.Thread(target=atendeRequisicoes, args=(clisock, endr))
                cliente.start()
                clientes.append(cliente)  # armazena a referencia da thread para usar com join()
            elif pronto is sys.stdin:  # entrada padrao
                cmd = input()
                if cmd == 'fim':  # solicitacao de finalizacao do servidor
                    for c in clientes:  # aguarda todas as threads terminarem
                        c.join()
                    sock.close()
                    sys.exit()
                elif cmd == 'hist':  # outro exemplo de comando para o servidor
                    print(str(conexoes.values()))
                elif cmd.startswith('remover'):  # Verifica se o comando começa com "remover"
                    chave = cmd.split(' ')[1]  # Separa o valor da chave a ser removida
                    remover(chave)

main()
