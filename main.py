import textwrap  # Para formatar o endereço
from datetime import datetime   # Para timesta


# Constantes
AGENCIA = "0001"
LIMITE_SAQUE_VALOR = 500.0
LIMITE_SAQUES_DIARIOS = 3
MAX_TRANSACOES_DIARIAS = 10 # Novo limite de transações

# --- Funções de Operações Bancárias ---
def depositar(saldo, valor, extrato, /):
    """Realiza a operação de depósito."""
    if valor > o:
        saldo += valor
        agora = datetime.now()
        extrato.append({'tipo': 'Depósito', 'valor': valor, 'data_hora': agora})
        print(f"\nDepósito de R$ {valor:.2f} realizado com sucesso!")
        return saldo, extrato
    else:
        print("\nOperação falhou! O valor informado é inválido.")
        return saldo, extrato # Retorna o estado sem alteração

def sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques):
    """Realiza a operação de saque."""
    excedeu_saldo = valor > saldo
    excedeu_limite = valor > limite
    excedeu_saques = numero_saques >= limite_saques

    if excedeu_saldo:
        print("\nOperação falhou! Você não tem saldo suficiente.")
    elif excedeu_limite:
        print(f"\nOperação falhou! O valor do saque (R$ {valor:.2f}) excede o limite de R$ {limite:.2f}por saque.")
    elif excedeu_saques:
        print(f"\nOperação falhou! Número máximo de {limite_saques} saques diários atingido.")
    elif valor <= 0:
        print("\nOperação falhou! O valor informado é inválido.")
    else:
        saldo -= valor
        numero_saques += 1
        agora = datetime.now()
        extrato.append({'tipo': 'Saque', 'valor': -valor, 'data_hora': agora})
        print(f"\nSaque de R$ {valor:.2f} realizado com sucesso!")
        return saldo, extrato, numero_saques # Retorna os valores atualizados

    return saldo, extrato, numero_saques # Retorna o estado sem alteração em caso de falha   

def visualizar_extrato(saldo, *, extrato):
    """Exibe o extrato da conta."""
    print("\n================ EXTRATO ================")
    if not extrato:
        print("Não foram realizadas movimentações.")
    else:
        for transacao in extrato:
            data_hora_formatada = transacao['data_hora'].strftime("%d/%m/%Y %H:%M:%S")
            tipo_transacao = transacao['tipo']
            valor_transacao = abs(transacao['valor']) # Exibe o valor absoluto
            print(f"{data_hora_formatada} - {tipo_transacao}: R$ {valor_transacao:.2f}")

    print(f"\nSaldo: R$ {saldo:.2f}")
    print("========================================")

# --- Funções de Usuário e Conta ---  
def filtrar_usuario(cpf, usuarios):
    """Busca um usuário na lista pelo CPF."""
    # Usa list comprehension para encontrar o usuário
    usuarios_filtrados = [usuario for usuario in usuarios if usuario["cpf"] == cpf]
    return usuarios_filtrados[0] if usuarios_filtrados else None # Retorna o primeiro encontrado ou None

# Definição do menu visualmente um pouco melhor
menu = """
================ MENU ================
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
Escolha uma opção:
Pressione enter para continuar...
======================================
=> """

# Variáveis iniciais com nomes mais descritivos e tipos apropriados
saldo_conta = 0.0
limite_por_saque = 500.0
extrato_transacoes = []  # Usar uma lista para o extrato
numero_saques_realizados = 0
MAX_SAQUES_DIARIOS = 3
MAX_TRANSACOES_DIARIAS = 10
numero_transacoes_hoje = 0

print("Bem-vindo ao sistema bancário!")

while True:
    # Processar a opção do menu de forma mais robusta
    opcao_escolhida = input(menu).strip().lower()

    if numero_transacoes_hoje >= MAX_TRANSACOES_DIARIAS and opcao_escolhida in ['d', 's']:
        print(f"Limite de ({MAX_TRANSACOES_DIARIAS} transações diárias atingido. Tente novamente amanhã.)")
        continue

    if opcao_escolhida == "d":
        print("\n--- Depósito ---")
        
        valor_deposito = float(input("Informe o valor do depósito: R$ "))

        if valor_deposito > 0:
            saldo_conta += valor_deposito
            agora = datetime.now()
            extrato_transacoes.append({'tipo': 'Depósito', 'valor': valor_deposito, 'data_hora': agora})
            numero_transacoes_hoje += 1

            # Adicionando o depósito ao extrato
            print(f"Depósito de R$ {valor_deposito:.2f} realizado com sucesso!")
        else:
            print("Valor inválido para depósito.")

    elif opcao_escolhida == "s":
        print("\n--- Saque ---")
        
        valor_saque = float(input("Informe o valor do saque: R$ "))

        # Variável para o saques
        if valor_saque > saldo_conta:
            print("Saldo insuficiente para saque.")

        elif valor_saque > limite_por_saque:
            print(f"Valor acima do limite de saque de R$ {limite_por_saque:.2f}.")

        elif numero_saques_realizados >= MAX_SAQUES_DIARIOS:
            print(f"Limite diário de saques atingido ({MAX_SAQUES_DIARIOS} saques).")

        elif valor_saque <= 0:
            print("Valor inválido para saque.")

        else:
            # Se todas as validações passarem, realizar o saque
            saldo_conta -= valor_saque
            agora = datetime.now()
            extrato_transacoes.append({'tipo': 'Saque', 'valor': -valor_saque, 'data_hora': agora})
            numero_saques_realizados += 1
            numero_transacoes_hoje += 1
            print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso!")
            print(f"Saques restantes hoje: {MAX_SAQUES_DIARIOS - numero_saques_realizados}")

    elif opcao_escolhida == "e":
        print("\n================ EXTRATO ================")
        if not extrato_transacoes:
            print("Nenhuma transação realizada.")
        else:
            for transacao in extrato_transacoes:
                data_hora_formatada = transacao['data_hora'].strftime("%d/%m/%Y %H:%M:%S")
                valor_formatada = f"R$ {abs(transacao['valor']):.2f}"
                print(f"{data_hora_formatada} - {transacao['tipo']}: {valor_formatada}")
                
        print(f"\nSaldo atual: R$ {saldo_conta:.2f}")
        print("==========================================")

    # Adicionando opção de sair do sistema
    elif opcao_escolhida == "q":
        print("Saindo do sistema. Até logo!")
        break
    else:
        print("Operação inválida. Por favor, selecione novamente a opção desejada usando as letras indicadas.")
# Fim do código
