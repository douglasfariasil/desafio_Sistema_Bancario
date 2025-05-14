# Sistema Bancário Simples em Python 

## Descrição Geral

Este projeto implementa um sistema bancário básico utilizando a linguagem Python, focado na simplicidade e demonstração de conceitos fundamentais de programação. O sistema permite ao usuário interagir através de um menu no console para realizar operações de depósito, saque e visualização de extrato.

## Funcionalidades

O sistema oferece as seguintes operações:

1.  **Depositar (`d`)**:
    * Permite ao usuário adicionar fundos à sua conta.
    * **Entrada**: O valor do depósito é solicitado como um número inteiro (R$).
    * **Validação**: O sistema verifica se o valor do depósito informado é positivo.
    * **Registro**: Depósitos bem-sucedidos são registrados no extrato no formato "Depósito: R$ VALOR.00".

2.  **Sacar (`s`)**:
    * Permite ao usuário retirar fundos da conta.
    * **Entrada**: O valor do saque é solicitado como um número inteiro (R$).
    * **Validações e Regras (nesta ordem)**:
        1.  Verifica se há `saldo_conta` suficiente.
        2.  Verifica se o `valor_saque` não excede o `limite_por_saque` (R$ 500,00).
        3.  Verifica se o `numero_saques_realizados` não atingiu o `MAX_SAQUES_DIARIOS` (3 saques).
        4.  Verifica se o `valor_saque` é positivo (maior que zero).
    * **Registro**: Saques bem-sucedidos são registrados no extrato no formato "Saque: R$ VALOR.00".

3.  **Extrato (`e`)**:
    * Exibe um histórico de todas as transações (depósitos e saques) realizadas na sessão atual.
    * Ao final, mostra o saldo atual da conta, formatado com duas casas decimais (ex: "Saldo atual: R$ SALDO.00").
    * Se nenhuma transação foi realizada, informa: "Nenhuma transação realizada."

4.  **Sair (`q`)**:
    * Encerra a execução do sistema bancário com a mensagem "Saindo do sistema. Até logo!".

## Como Executar

1.  **Pré-requisito**: Certifique-se de ter o Python 3 instalado.
2.  **Salvar o Código**: Copie o código fornecido e salve-o em um arquivo com a extensão `.py` (ex: `meu_banco.py`).
3.  **Abrir o Terminal/Prompt de Comando**.
4.  **Navegar até o Diretório** onde o arquivo foi salvo.
5.  **Executar o Script**:
    ```bash
    python meu_banco.py
    ```
6.  Siga as instruções do menu interativo.

## Visão Geral da Implementação

### Estrutura Principal

* **Menu Interativo**: A variável `menu` contém o texto exibido ao usuário, solicitando a escolha de uma operação.
* **Variáveis de Estado**:
    * `saldo_conta`: (float) Armazena o saldo atual.
    * `limite_por_saque`: (float) Define o teto de R$ 500,00 para cada saque.
    * `extrato_transacoes`: (list) Lista que guarda o registro textual de cada transação.
    * `numero_saques_realizados`: (int) Contador de saques na sessão.
    * `MAX_SAQUES_DIARIOS`: (int) Constante para o limite de 3 saques diários.
* **Loop de Execução**: Um loop `while True` mantém o programa ativo, processando as opções do usuário até que 'q' seja escolhido. A entrada do usuário é normalizada com `.strip().lower()`.

### Lógica das Operações

* **Depósito**:
    * Converte a entrada do usuário para `int` com `int(input(...))`. **Atenção**: Não há tratamento para o caso do usuário digitar um texto não numérico, o que causaria um erro (`ValueError`) e encerraria o programa.
    * Valida se o valor é positivo.
    * Atualiza `saldo_conta` e adiciona ao `extrato_transacoes`.

* **Saque**:
    * Converte a entrada para `int` com `int(input(...))`. (Mesma atenção sobre `ValueError` do depósito).
    * Aplica as validações na ordem especificada na seção "Funcionalidades".
    * Se aprovado, atualiza `saldo_conta`, `numero_saques_realizados` e `extrato_transacoes`.

* **Extrato**:
    * Verifica se a lista `extrato_transacoes` está vazia e exibe a mensagem apropriada.
    * Caso contrário, percorre a lista e imprime cada transação.
    * Exibe o `saldo_conta` formatado ao final.

* **Sair**: Interrompe o loop com `break`.

### Formato dos Valores

* **Entrada**: Valores para depósito e saque são lidos como inteiros (`int`).
* **Saída/Exibição**: No extrato e na exibição do saldo, os valores são formatados com duas casas decimais usando f-strings (ex: `f"R$ {valor:.2f}"`). Isso significa que, mesmo que a entrada seja um inteiro como `100`, será exibido como `R$ 100.00`.

## Limitações da Versão Atual

* **Entrada de Valores**: O sistema aceita apenas **números inteiros** para depósitos e saques. Não há suporte para centavos na entrada de valores.
* **Tratamento de Erros de Entrada**: O código **não possui tratamento de erro** para entradas não numéricas (ex: letras ou símbolos) nos campos de valor de depósito ou saque. Se o usuário fornecer uma entrada inválida nesses campos, o programa será encerrado com um `ValueError`.
* **Usuário Único**: Não há sistema de login ou diferenciação entre contas; todas as operações são feitas em uma conta única e implícita.
* **Não Persistência de Dados**: Todos os dados (saldo, extrato, contador de saques) são armazenados em memória e **perdidos ao fechar o programa**.
* **Reset de Limites Diários**: O contador de saques diários é zerado a cada nova execução do script.

Este README visa descrever o funcionamento e as características do código fornecido.