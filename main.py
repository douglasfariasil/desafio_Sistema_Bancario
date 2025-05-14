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

print("Bem-vindo ao sistema bancário!")

while True:
    # Processar a opção do menu de forma mais robusta
    opcao_escolhida = input(menu).strip().lower()

    if opcao_escolhida == "d":
        print("\n--- Depósito ---")
        
        valor_deposito = float(input("Informe o valor do depósito: R$ "))

        if valor_deposito > 0:
            saldo_conta += valor_deposito
            extrato_transacoes.append(f"Depósito: R$ {valor_deposito:.2f}")
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
            extrato_transacoes.append(f"Saque: R$ {valor_saque:.2f}")
            numero_saques_realizados += 1
            print(f"Saque de R$ {valor_saque:.2f} realizado com sucesso!")
            print(f"Saques restantes hoje: {MAX_SAQUES_DIARIOS - numero_saques_realizados}")

    elif opcao_escolhida == "e":
        print("\n================ EXTRATO ================")
        if not extrato_transacoes:
            print("Nenhuma transação realizada.")
        else:
            for transacao in extrato_transacoes:
                print(transacao)
        print(f"\nSaldo atual: R$ {saldo_conta:.2f}")
        print("==========================================")

    # Adicionando opção de sair do sistema
    elif opcao_escolhida == "q":
        print("Saindo do sistema. Até logo!")
        break
    else:
        print("Operação inválida. Por favor, selecione novamente a opção desejada usando as letras indicadas.")
# Fim do código
