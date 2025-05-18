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
    if valor > 0:
        saldo += valor
        agora = datetime.now()
        extrato.append({
            'tipo': 'Depósito',
            'valor': valor,
            'data_hora': agora
        })
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
        extrato.append({
            'tipo': 'Saque',
            'valor': -valor,
            'data_hora': agora
        })
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

def criar_usuario(usuarios):
    """Cadastra um novo usuário (cliente)."""
    cpf = input("Informe o CPF (somente números): ")
    usuario_existente = filtrar_usuario(cpf, usuarios)

    if usuario_existente:
        print("\n--- Erro: CPF já cadastrado! ---")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ") # Validação de data pode ser adicionada depois
    endereco = input("Informe o endereço (logradouro, numero - bairro - cidade/sigla estado): ")

    usuarios.append({"nome": nome, "data_nascimento": data_nascimento, "cpf": cpf, "endereco": endereco})
    print("\n--- Usuário cadastrado com sucesso! ---")  

def criar_conta_corrente(agencia, numero_conta_sequencial, usuarios, contas):
    """Cria uma nova conta corrente para um usuário."""
    cpf = input("Informe o CPF do usuário para vincular a conta: ")
    usuario = filtrar_usuario(cpf, usuarios)

    if not usuario:
        print("\n--- Erro: Usuário não encontrado! ---")
        return None # Retorna None se o usuário não existir

    # Cria a conta com o próximo número sequencial
    numero_conta = numero_conta_sequencial
    contas.append({
        "agencia": agencia,
        "numero_conta": numero_conta,
        "usuario": usuario, # Vincula o objeto usuário à conta
        "saldo": 0.0,
        "extrato": [],
        "numero_saques_hoje": 0,
        "numero_transacoes_hoje": 0 # Contador de transações para o limite diário por conta
    })

    print(f"\n--- Conta criada com sucesso! ---")
    print(f"\nAgência: {agencia}")
    print(f"\nConta: {numero_conta}")
    return numero_conta_sequencial + 1 # Retorna o próximo número sequencial a ser usado

def listar_contas(contas):
    """Exibe a lista de contas cadastradas."""
    if not contas:
        print("\n--- Nenhuma conta cadastrada. ---")
        return

    print("\n=========== Contas Cadastradas ===========")
    for conta in contas:
        # Usando textwrap.dedent para remover identação para exibição limpa
        linha = f"""\
            Agência:\t{conta['agencia']}
            Conta:\t\t{conta['numero_conta']}
            Titular:\t{conta['usuario']['nome']}
            Saldo:\t\tR$ {conta['saldo']:.2f}
        """
        print(textwrap.dedent(linha)) # Imprime a linha formatada
        print("-" * 30) # Separador entre contas
    print("==========================================")

def recuperar_conta(contas):
    """Solicita e busca uma conta na lista pelo número da conta e agência."""
    if not contas:
        print("\n--- Nenhuma conta cadastrada para realizar operações. ---")
        return None

    agencia_input = input("Informe a agência (padrão 0001): ") or AGENCIA # Assume 0001 se vazio
    try:
        numero_conta_input = int(input("Informe o número da conta: "))
    except ValueError:
        print("\nNúmero da conta inválido.")
        return None

    for conta in contas:
        if conta['agencia'] == agencia_input and conta['numero_conta'] == numero_conta_input:
            return conta # Retorna o dicionário da conta encontrada

    print("\n--- Erro: Conta não encontrada! ---")
    return None # Retorna None se a conta não existir

# --- Menu Principal ---
def main():
    """Função principal que executa o menu do sistema bancário."""
    usuarios = []  # Lista para armazenar usuários
    contas = []  # Lista para armazenar contas
    numero_conta_sequencial = 1  # Contador sequencial para o número da conta

# Definição do menu visualmente um pouco melhor
    menu = """
================ MENU ================
[c] Cadastrar Usuário
[cc] Cadastrar Conta Corrente
[l] Listar Contas
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
Escolha uma opção:
Pressione enter para continuar...
======================================
=> """

    print("Bem-vindo ao sistema bancário!")

    while True:
        opcao = input(menu).strip().lower()

        if opcao == 'c':
            criar_usuario(usuarios) # Passa a lista de usuários

        elif opcao == 'cc':
            # Passa a agência padrão, o contador, a lista de usuários e a lista de contas
            resultado = criar_conta_corrente(AGENCIA, numero_conta_sequencial, usuarios, contas)
            if resultado is not None: # Atualiza o contador apenas se a conta for criada
                numero_conta_sequencial = resultado

        elif opcao == 'l':
             listar_contas(contas) # Passa a lista de contas

        elif opcao in ('d', 's', 'e'):
            # Para depositar, sacar ou extrato, primeiro recupera a conta
            conta_cliente = recuperar_conta(contas)

            if conta_cliente: # Se a conta foi encontrada
                 # Verifica o limite de transações diárias para ESTA conta
                if conta_cliente['numero_transacoes_hoje'] >= MAX_TRANSACOES_DIARIAS:
                    print(f"\nLimite de {MAX_TRANSACOES_DIARIAS} transações diárias atingido para esta conta. Tente novamente amanhã.")
                    continue # Volta para o menu

                # --- Executa a operação escolhida ---
                if opcao == 'd':
                    try:
                        valor = float(input("Informe o valor do depósito: R$ "))
                        # Chama a função depositar com argumentos posicionais
                        novo_saldo, novo_extrato = depositar(conta_cliente['saldo'], valor, conta_cliente['extrato'])
                        # Atualiza a conta com os valores retornados
                        conta_cliente['saldo'] = novo_saldo
                        conta_cliente['extrato'] = novo_extrato
                        if valor > 0: # Incrementa a transação apenas se o depósito for válido
                             conta_cliente['numero_transacoes_hoje'] += 1
                    except ValueError:
                        print("\nEntrada inválida. Por favor, digite um número.")

                elif opcao == 's':
                    try:
                        valor = float(input("Informe o valor do saque: R$ "))
                         # Chama a função sacar com argumentos nomeados
                        novo_saldo, novo_extrato, novo_numero_saques = sacar(
                            saldo=conta_cliente['saldo'],
                            valor=valor,
                            extrato=conta_cliente['extrato'],
                            limite=LIMITE_SAQUE_VALOR,
                            numero_saques=conta_cliente['numero_saques_hoje'],
                            limite_saques=LIMITE_SAQUES_DIARIOS
                        )
                        # Atualiza a conta com os valores retornados
                        conta_cliente['saldo'] = novo_saldo
                        conta_cliente['extrato'] = novo_extrato
                        conta_cliente['numero_saques_hoje'] = novo_numero_saques
                        # Incrementa a transação apenas se o saque for válido (saldo, limite saque, limite saques, valor > 0)
                        if novo_numero_saques > conta_cliente['numero_saques_hoje'] - 1: # Verifica se numero_saques aumentou
                             conta_cliente['numero_transacoes_hoje'] += 1

                    except ValueError:
                         print("\nEntrada inválida. Por favor, digite um número.")

                elif opcao == 'e':
                    # Chama a função extrato com argumentos posicionais e nomeados
                    visualizar_extrato(conta_cliente['saldo'], extrato=conta_cliente['extrato'])
                    # Não incrementa numero_transacoes_hoje para extrato

        elif opcao == 'q':
            print("\nObrigado por usar nosso sistema modularizado. Até logo!")
            break

        else:
            print("\nOperação inválida. Por favor, selecione novamente a operação desejada.")

# Executa a função principal quando o script é rodado
if __name__ == "__main__":
    main()

# O código foi modularizado para facilitar a manutenção e a legibilidade.

