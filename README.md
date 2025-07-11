# Sistema Bancário Simples em Python

## Descrição Geral

Este é um sistema bancário simples desenvolvido em Python, utilizando os princípios da Programação Orientada a Objetos (POO). Ele permite:

- **Cadastrar clientes** com informações como nome, data de nascimento, CPF e endereço.
- **Criar contas correntes** associadas a clientes existentes.
- **Realizar depósitos** e **saques**, com validações de limites.
- **Exibir extratos** detalhados das transações realizadas.
- **Listar contas** e clientes cadastrados.
- **Registrar transações** em um arquivo de log (`log.txt`).

## Funcionalidades

### Operações Disponíveis

- **Cadastro de Clientes**: Registra novos clientes.
- **Criação de Contas Correntes**: Vincula contas a clientes existentes.
- **Depósito**: Adiciona saldo à conta.
- **Saque**: Permite saques com validações de:
  - Saldo insuficiente.
  - Limite por transação (R$ 500.00).
  - Número máximo de saques diários (3 saques).
- **Extrato**: Exibe o histórico de transações e o saldo atual.
- **Listagem de Contas**: Mostra todos os clientes e suas contas.
- **Controle de Transações Diárias**: Limita o número total de transações por dia (10 transações).
- **Log de Transações**: Registra todas as operações importantes em `log.txt`.

### Estrutura do Código

O sistema é modularizado usando classes para representar as entidades do banco:

- **Pessoa**: Classe base para informações gerais de uma pessoa.
- **PessoaFisica**: Herda de `Pessoa` e adiciona o atributo `cpf`.
- **Cliente**: Representa um cliente bancário e gerencia suas contas.
- **Historico**: Gerencia o registro de todas as transações de uma conta.
- **Transacao**: Classe abstrata base para operações financeiras.
  - **Deposito**: Implementa a lógica de depósito.
  - **Saque**: Implementa a lógica de saque, incluindo validações.
- **Conta**: Classe base para contas bancárias.
  - **ContaCorrente**: Herda de `Conta` e define limites específicos para saques.

## Como Executar

1. **Salve o Código**: Salve o código Python em um arquivo, por exemplo, `sistema_bancario.py`.
2. **Abra o Terminal**: Navegue até o diretório onde o arquivo foi salvo.
3. **Execute o Script**: Digite o comando abaixo e pressione Enter:
   ```sh
   python sistema_bancario.py
   ```
