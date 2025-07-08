# Sistema Bancário Simples em Python

## Descrição Geral

Este é um sistema bancário simples desenvolvido em Python, utilizando os princípios da Programação Orientada a Objetos (POO). Ele permite cadastrar clientes, criar contas correntes, realizar operações de depósito e saque, e visualizar o extrato das transações. O sistema também implementa limites diários para saques e para o número total de transações.

## Funcionalidades

Cadastro de Clientes: Permite registrar novos clientes com informações como nome, data de nascimento, CPF e endereço.

Criação de Contas Correntes: Associa uma nova conta corrente a um cliente existente.

Depósito: Realiza depósitos em contas, aumentando o saldo.

Saque: Permite saques, com validações para:

Saldo insuficiente.

Valor do saque excedendo o limite por transação (R$ 500.00).

Número máximo de saques diários (3 saques).

Extrato: Exibe o histórico de todas as transações (depósitos e saques) realizadas na conta, juntamente com o saldo atual.

Listagem de Contas: Mostra todos os clientes cadastrados e suas respectivas contas.

Controle de Transações Diárias: Limita o número total de transações (depósitos e saques) por conta por dia (10 transações).

Log de Transações: Um decorador (@log_transacoes) registra todas as operações importantes em um arquivo log.txt, incluindo data, hora, função executada, argumentos e resultado.

Estrutura do Código (POO)
O sistema é modularizado usando classes para representar as entidades do banco:

Pessoa: Classe base para informações gerais de uma pessoa.

PessoaFisica(Pessoa): Herda de Pessoa e adiciona o atributo cpf.

Cliente(PessoaFisica): Representa um cliente bancário, gerencia suas contas e o método realizar_transacao.

Historico: Gerencia o registro de todas as transações de uma conta.

Transacao: Classe abstrata base para todas as operações financeiras (depósito, saque).

Deposito(Transacao): Implementa a lógica de depósito.

Saque(Transacao): Implementa a lógica de saque, incluindo as validações de limites.

Conta: Classe base para uma conta bancária, com saldo, agência, número, cliente e histórico. Contém a lógica para resetar limites diários e incrementar contadores de transações.

ContaCorrente(Conta): Herda de Conta e define os limites específicos para saques.

Como Executar
Salve o Código: Salve o código Python fornecido em um arquivo, por exemplo, sistema_bancario.py.

Abra o Terminal/Prompt de Comando: Navegue até o diretório onde você salvou o arquivo.

Execute o Script: Digite o seguinte comando e pressione Enter:

python sistema_bancario.py

Menu de Operações
Ao executar o programa, você verá um menu de opções:

[c] Cadastrar Usuário: Para criar um novo cliente.

[cc] Criar Conta: Para vincular uma nova conta corrente a um cliente existente.

[lc] Listar Contas: Para visualizar todos os clientes e suas contas.

[d] Depositar: Para realizar um depósito em uma conta.

[s] Sacar: Para realizar um saque de uma conta.

[e] Extrato: Para visualizar o histórico de transações e o saldo de uma conta.

[q] Sair: Para encerrar o programa.

Exemplo de Uso:
Cadastrar Cliente:

=> c
Informe o CPF (somente números): 12345678900
Informe o nome completo: Maria Silva
Informe a data de nascimento (dd-mm-aaaa): 01-01-1990
Informe o endereço (logradouro, numero - bairro - cidade/sigla estado): Rua A, 123 - Centro - Cidade/SP
--- Cliente cadastrado com sucesso! ---

Criar Conta:

=> cc
Informe o CPF do cliente para vincular a conta: 12345678900
--- Conta 0001/1 criada com sucesso para Maria Silva! ---

Depositar:

=> d
Informe o CPF do cliente (somente números): 12345678900
Contas do cliente:

1. Agência: 0001, Conta: 1, Saldo: R$ 0.00
   Selecione o número da conta (ex: 1 para a primeira): 1
   Informe o valor do depósito: R$ 1000
   Depósito de R$ 1000.00 realizado com sucesso na conta 0001/1!

Exibir Extrato:

=> e
Informe o CPF do cliente (somente números): 12345678900
Contas do cliente:

1. Agência: 0001, Conta: 1, Saldo: R$ 1000.00
   Selecione o número da conta (ex: 1 para a primeira): 1
   ================ EXTRATO ================
   [Data e Hora do Depósito] - Depósito: R$ 1000.00
   Saldo atual: R$ 1000.00
   ========================================

Observações
O arquivo log.txt será criado ou atualizado no mesmo diretório do script, registrando as operações.

Os limites diários (saques e transações) são resetados automaticamente quando a data do sistema muda.
