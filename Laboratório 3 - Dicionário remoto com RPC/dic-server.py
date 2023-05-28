# Servidor de dicionario remoto usando RPyC
import rpyc
from rpyc.utils.server import ThreadedServer
import json

# define o arquivo para salvar o dicionario
DICIONARIO_FILE = 'dicionario.json'
dicionario = []


class DicionarioRemoto(rpyc.Service):
    print("Pronto para receber conexões...")

    def on_connect(self, conx):
        print("Conexao estabelecida.")

    def on_disconnect(self, conx):
        print("Conexao encerrada.")

    def exposed_carregar_dicionario(self):
        global dicionario
        '''Carrega o dicionario do arquivo JSON, ou cria um novo arquivo se ele nao existir'''
        try:
            with open(DICIONARIO_FILE, 'r') as f:
                dicionario = json.load(f)
        except FileNotFoundError:
            dicionario = []
        return dicionario

    def exposed_salvar_dicionario(self, dicionario_local):
        global dicionario
        dicionario = dicionario_local
        '''Atualiza o dicionario remoto no arquivo JSON'''
        with open(DICIONARIO_FILE, 'w') as f:
            json.dump(dicionario, f)

    def exposed_consulta(self, chave):
        global dicionario
        for chave_valores in dicionario:
            if chave in chave_valores:
                valores = chave_valores[chave]
                return chave + " -> " + str(valores)
        return chave + " -> " + str([])

    def exposed_escrita(self, chave, valor):
        global dicionario
        for chave_valores in dicionario:
            if chave in chave_valores:
                chave_valores[chave].append(valor)
                chave_valores[chave].sort()
                self.exposed_salvar_dicionario(dicionario)  # atualiza o dicionario com o novo valor no arquivo
                valores = chave_valores[chave]
                return chave + " -> " + str(valores)
        nova_chave = {chave: [valor]}
        dicionario.append(nova_chave)
        self.exposed_salvar_dicionario(dicionario)  # atualiza o dicionario com o novo valor no arquivo
        return chave + " -> " + str([valor])

    def exposed_remocao(self, chave):
        global dicionario
        for i, d in enumerate(dicionario):
            for _ in d:
                if chave in d:
                    dicionario.pop(i)
                    self.exposed_salvar_dicionario(dicionario)  # atualiza o dicionario com a chave removida no arquivo
                    return "Chave " + chave + " removida."
        return "Chave " + chave + " não encontrada."


dicionarioRemoto = ThreadedServer(DicionarioRemoto, port=10000)
dicionarioRemoto.start()
