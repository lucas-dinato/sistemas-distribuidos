#### Lucas Vieira Dinato - 117240117
#### Sistemas Distribuídos 2023.1
#### Servidor: `join-thread-srv.py`
#### Cliente: `cli.py`
Atividade 1:
1. Estilo Arquitetural: Arquitetura em camada.
2. Componentes:
    * Camada de dados: Acesso e persistência de dados.
    * Camada de Processamento: Processamento das requisições.
    * Camada de aplicação: Interface com o usuário.
    * Modo de conexão: Servidor manipula os dados do dicionario.json de acordo com as requisições do cliente, que é responsável pela interface com o usuário.

Atividade 2:
1. Componentes no Cliente: Camada de aplicação.
2. Componentes no Servidor: Camada de dados e de processamento.
3. Mensagens:
   * Não há uma ordem necessária.
   * Caso Cliente envie mensagem do tipo: "chave1" :
     * Servidor retorna a lista de valores de acordo com o dicionário (lista vazia caso a entrada
     não exista).
   * Caso Cliente envie mensagem do tipo: "chave1, valor1" :
     * Servidor retorna a lista de valores atualizado com o novo valor.
   * Caso Servidor envie mensagem do tipo: "remover chave1" :
     * A chave e todos seus valores são removidos do dicionário através do próprio servidor.
