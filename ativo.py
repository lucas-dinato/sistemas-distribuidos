# Exemplo basico socket (lado ativo)

import socket

HOST = 'localhost'  # maquina onde esta o par passivo
PORTA = 5000  # porta que o par passivo esta escutando

# cria socket
sock = socket.socket()  # default: socket.AF_INET, socket.SOCK_STREAM

# conecta-se com o par passivo
sock.connect((HOST, PORTA))

while True:
    # envia uma mensagem para o par conectado
    msg = input()
    if msg == 'fim':
        break
    sock.send(msg.encode())

    # espera a resposta do par conectado (chamada pode ser BLOQUEANTE)
    msg = sock.recv(1024)  # argumento indica a qtde maxima de bytes da mensagem

    # imprime a mensagem recebida
    print(str(msg, encoding='utf-8'))

# encerra a conexao
sock.close()
