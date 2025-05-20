import textwrap  # Para formatar o endereço
from datetime import datetime   # Para timesta


# --- Constantes ---
AGENCIA = "0001"
LIMITE_SAQUE_VALOR = 500.0
LIMITE_SAQUES_DIARIOS = 3
MAX_TRANSACOES_DIARIAS = 10 # Novo limite de transações

# --- Classes de base (POO) ---

class Transacao:
    """
    Classe base para todas as transações bancárias.
    Define a estrutura comum de uma transação.
    """
    def __init__(self, valor):
        if valor <= 0:
            raise ValueError("O valor da transação deve ser maior do que zero.")
        self._valor = valor
        self._data_hora = datetime.now()

    @property
    def valor(self):
        return self._valor
    
    @property
    def data_hora(self):
        return self._data_hora
    
    def registrar(self, conta):
        """
        Método abstrato para ser implementado pelas subclasses.
        Realiza a lógica específica da transação na conta.
        """
        raise NotImplementedError("Método 'registrar' deve ser implementado pela subclasse.")

class Deposito(Transacao):
    """
    Representa uma operação de depósito.
    """
    def __init__(self, valor):
        super().__init__(valor)
        self._tipo = "Depósito"

    @property
    def tipo(self):
        return self._tipo
    
    def registrar(self, conta):
        """
        Implementa a lógica de depósito na conta.
        """
        conta.saldo += self.valor
        conta.historico.adicionar_transacao(self)
        conta.numero_transacoes_hoje += 1
        print(f"\nDepósito de R$ {self.valor:.2f} realizado com sucesso {conta.agencia}/{conta.numero}!")
        return True
    
class Saque(Transacao):
    """
    Representa uma operação de saque.
    """
    def __init__(self, valor):
        super().__init__(valor)
        self._tipo = "Saque"

    @property
    def tipo(self):
        return self._tipo
    
    def registrar(self, conta):
        """
        Implementa a lógica de saque na conta, aplicando os limites da conta corrente.
        """
        # Estas validações são específicas da ContaCorrente,
        # mas são colocadas aqui para simplificar a delegação da lógica de saque
        # na classe ContaCorrente.
        if self.valor > conta.saldo:
            print("\nOperação falhou! Você não tem saldo suficiente.")
            return False
        
        # O limite_saque e limite_saques_diarios são propriedades da ContaCorrente
        # Vamos assumir que 'conta' aqui é uma instância de ContaCorrente
        if hasattr(conta, 'limite_saque') and self.valor > conta.limite_saque:
            print(f"\nOperação falhou! O valor do saque (R$ {self.valor:.2f}) excede o limite de R$ {conta.limite_saque:.2f} por saque.")
            return False
        
        if hasattr(conta, 'limite_saques_diarios') and conta.numero_saques_hoje >= conta.limite_saques_diarios:
            print(f"\nOperação falhou! Número máximo de {conta.limite_saques_diarios} saques diários excedido.")
            return False
        
        if self.valor <= 0: # Caso o valor seja validado no __init__ de transação, isso pode ser redundante aqui
            print(f"\nOperação falhou! O valor informado é inválido.")
            return False

        conta.saldo -= self.valor
        conta.historico.adicionar_transacao(self)
        conta.numero_saques_hoje += 1
        conta.numero_transacoes_hoje += 1
        print(f"\nSaque de R$ {self.valor:.2f} realizado com sucesso na conta {conta.agencia}/{conta.numero}!")
        return True
    
class Historico:
    """
    Gerencia o histórico de transações de uma conta.
    """
    def __init__(self):
        self.transacoes = []


    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        """Adiciona uma transação ao histórico."""
        self._transacoes.append(transacao)

    def gerar_relatorio(self):
        """Exibe o extrato das transações."""
        if not self._transacoes:
            return "Nenhuma movimentação realizada."
        
        relatorio = []
        for transacao in self._transacoes:
            data_hora_formatada = transacao.data_hora.strftime("%d/%m/%Y %H:%M:%S")
            tipo_transacao = transacao.tipo
            valor_transacao = abs(transacao.valor) if tipo_transacao == "Saque" else transacao.valor
            relatorio.append(f"{data_hora_formatada} - {tipo_transacao}: R$ {valor_transacao:.2f}")
        
        return "\n".join(relatorio)
    
# --- Classes de Conta ---

class Conta:
    """
    Classe base para uma conta bancária.
    """
    def __init__(self, numero, cliente):
        self._agencia = AGENCIA        #_PADRAO
        self._numero = numero
        self._cliente = cliente # Objeto Cliente
        self._saldo = 0.0
        self._historico = Historico()
        self._numero_saques_hoje = 0 # Contador de saques para o limite diário
        self._numero_transacoes_hoje = 0 # Contador de transações para o limite diário

    @classmethod
    def nova_conta(cls, numero, cliente):
        """Cria uma nova instância de conta."""
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

    @saldo.setter
    def saldo(self, novo_saldo):
        self._saldo = novo_saldo

    @property
    def numero(self):
        return self._numero
    
    @property
    def agencia(self):
        return self._agencia
    
    @property
    def cliente(self):
        return self._cliente
    
    @property
    def historico(self):
        return self._historico
    
    @property
    def numero_saques_hoje(self):
        return self._numero_saques_hoje
    
    @numero_saques_hoje.setter
    def numero_saques_hoje(self, valor):
        self._numero_saques_hoje = valor

    @property
    def numero_transacoes_hoje(self):
        return self._numero_transacoes_hoje
    
    @numero_transacoes_hoje.setter
    def numero_transacoes_hoje(self, valor):
        self._numero_transacoes_hoje = valor

    def sacar(self, valor):
        """Realiza a operação de saque, a ser sobrescrito por classes filhas."""
        raise NotImplementedError("Método 'sacar' deve ser implementado pela subclasse.") 

    def depositar(self, valor):
        """Realiza a operação de depósito."""
    # Delega para a classe Deposito registrar a transação
        transacao = Deposito(valor)
        return transacao.registrar(self)  # Passa a própria conta para a transação  
    
    def __str__(self):
        """Representação da conta como string."""
        return f"Conta:\t{self.numero}\nAgência:\t\t{self.agencia}\nCliente:\t{self.cliente.nome}"

class ContaCorrente(Conta):
    """
    Representa uma conta corrente.
    """
    def __init__(self, numero, cliente, limite_saque=LIMITE_SAQUE_VALOR, limite_saques_diarios=LIMITE_SAQUES_DIARIOS):
        super().__init__(numero, cliente)
        self._limite_saque = limite_saque
        self._limite_saques_diarios = limite_saques_diarios

    @property
    def limite_saque(self):
        return self._limite_saque

    @property
    def limite_saques_diarios(self):
        return self._limite_saques_diarios

    def sacar(self, valor):
        """Realiza a operação de saque."""
        transacao = Saque(valor)  # Saque já faz a validação de valor > 0
        return transacao.registrar(self)  # Passa a própria conta para a transação

    def __str__(self):
        """Representação em string da conta corrente."""
        return textwrap.dedent(f"""\
            Agência:\t{self.agencia}
            C/C:\t\t{self.numero}
            Titular:\t{self.cliente.nome}
            Saldo:\t\tR$ {self.saldo:.2f}
        """)
    
# --- Classes de Pessoa e Cliente ---
class Pessoa:
    """
    Classe base para uma pessoa.
    """
    def __init__(self, nome, data_nascimento, cpf, endereco):
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._cpf = cpf
        self._endereco = endereco

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento

    @property
    def cpf(self):
        return self._cpf

    @property
    def endereco(self):
        return self._endereco
    
class Cliente(Pessoa):
    """
    Representa um cliente do banco, herdando de Pessoa.
    """
    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(nome, data_nascimento, cpf, endereco)
        # if not cpf.isdigit() or len(cpf) != 11: # Exemplo de validação de CPF (apenas números, 11 dígitos)
        #     raise ValueError("CPF inválido! Deve conter 11 dígitos numéricos.")
        self._cpf = cpf
        self._contas = []  # Lista de contas associadas ao cliente

    @property
    def cpf(self):
        return self._cpf

    @property
    def contas(self):
        return self._contas

    def adicionar_conta(self, conta):
        """Adiciona uma conta à lista de contas do cliente."""
        self._contas.append(conta)

    # O método 'realizar_transacao' pode ser na conta ou no cliente,
    # neste modelo, a transação já tem o método 'registrar' que recebe a conta.
    # Assim, o cliente apenas "instancia" a transação e pede para ela se registrar na conta.
    def realizar_transacao(self, conta, transacao_obj):
        """
        Um cliente pode realizar uma transação em uma de suas contas.
        A transação é um objeto Saque ou Deposito.
        """
        if conta not in self.contas:
            print("\n--- Erro: Esta conta não pertence a este cliente. ---")
            return False

        if conta.numero_transacoes_hoje >= MAX_TRANSACOES_DIARIAS:
            print(f"\n--- Erro: Limite de {MAX_TRANSACOES_DIARIAS} transações diárias atingido para a conta {conta.agencia}/{conta.numero}. ---")
            return False

        # Chama o método registrar da transação, passando a conta.
        # As validações específicas de saque/depósito estão dentro de seus métodos registrar.
        return transacao_obj.registrar(conta)
    

# --- Funções Auxiliares do Sistema (fora das classes para orquestração) ---

def buscar_cliente(cpf, clientes):
    """Busca um cliente na lista pelo CPF."""
    # Usa list comprehension para encontrar o cliente
    clientes_filtrados = [cliente for cliente in clientes if cliente.cpf == cpf]
    return clientes_filtrados[0] if clientes_filtrados else None # Retorna o primeiro encontrado ou None

def buscar_conta(numero_conta, contas):
    """Busca uma conta na lista pelo número da conta."""
    # Usa list comprehension para encontrar a conta
    contas_filtradas = [conta for conta in contas if conta.numero == numero_conta]
    return contas_filtradas[0] if contas_filtradas else None # Retorna o primeiro encontrado ou None

def recuperar_conta_cliente(clientes):
    """
    Auxiliar para solicitar CPF e número da conta ao usuário,
    e retornar o objeto conta e o objeto cliente.
    """
    cpf = input("Informe o CPF do cliente (somente números): ")
    cliente = buscar_cliente(cpf, clientes)

    if not cliente:
        print("\n--- Erro: Cliente não encontrado! ---")
        return None, None

    if not cliente.contas:
        print("\n--- Cliente não possui contas cadastradas! ---")
        return None, None

    print("\nContas do cliente:")
    for i, conta in enumerate(cliente.contas):
        print(f"  {i+1}. Agência: {conta.agencia}, Conta: {conta.numero}, Saldo: R$ {conta.saldo:.2f}")

    try:
        idx_conta = int(input("Selecione o número da conta (ex: 1 para a primeira): ")) - 1
        if 0 <= idx_conta < len(cliente.contas):
            conta = cliente.contas[idx_conta]
            return cliente, conta
        else:
            print("\n--- Erro: Índice de conta inválido. ---")
            return None, None
    except ValueError:
        print("\n--- Erro: Entrada inválida. Digite um número. ---")
        return None, None
    

# --- Funções para Opções do Menu ---

def cadastrar_cliente(clientes):
    """Função para cadastrar um novo cliente."""
    cpf = input("Informe o CPF (somente números): ")
    if buscar_cliente(cpf, clientes):
        print("\n--- Erro: Já existe cliente com este CPF! ---")
        return

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input("Informe o endereço (logradouro, numero - bairro - cidade/sigla estado): ")

    try:
        novo_cliente = Cliente(nome, data_nascimento, endereco, cpf)
        clientes.append(novo_cliente)
        print("\n--- Cliente cadastrado com sucesso! ---")
    except ValueError as e:
        print(f"\n--- Erro ao cadastrar cliente: {e} ---")


def criar_conta_corrente(numero_conta, clientes, contas):
    """Função para criar uma nova conta corrente e vinculá-la a um cliente."""
    cpf = input("Informe o CPF do cliente para vincular a conta: ")
    cliente = buscar_cliente(cpf, clientes)

    if not cliente:
        print("\n--- Erro: Cliente não encontrado! ---")
        return None

    # Cria a conta corrente
    nova_conta = ContaCorrente.nova_conta(numero_conta, cliente)
    
    # Adiciona a conta à lista de contas globais e ao cliente
    contas.append(nova_conta)
    cliente.adicionar_conta(nova_conta) # Adiciona a conta à lista de contas do cliente

    print(f"\n--- Conta {AGENCIA}/{nova_conta.numero} criada com sucesso para {cliente.nome}! ---") # PARA alterar {AGENCIA_PADRAO}
    return numero_conta + 1 # Retorna o próximo número de conta sequencial


def realizar_deposito(clientes):
    """Função para realizar um depósito."""
    cliente, conta = recuperar_conta_cliente(clientes)
    if not (cliente and conta):
        return

    try:
        valor = float(input("Informe o valor do depósito: R$ "))
        if valor <= 0:
            print("\n--- Erro: Valor de depósito inválido. ---")
            return

        transacao_obj = Deposito(valor) # Cria o objeto Deposito
        cliente.realizar_transacao(conta, transacao_obj) # Cliente delega a transação
        
    except ValueError as e:
        print(f"\n--- Erro: Entrada inválida. {e} ---")


def realizar_saque(clientes):
    """Função para realizar um saque."""
    cliente, conta = recuperar_conta_cliente(clientes)
    if not (cliente and conta):
        return

    try:
        valor = float(input("Informe o valor do saque: R$ "))
        if valor <= 0:
            print("\n--- Erro: Valor de saque inválido. ---")
            return

        transacao_obj = Saque(valor) # Cria o objeto Saque
        cliente.realizar_transacao(conta, transacao_obj) # Cliente delega a transação

    except ValueError as e:
        print(f"\n--- Erro: Entrada inválida. {e} ---")


def exibir_extrato(clientes):
    """Função para exibir o extrato."""
    print("\n================ EXTRATO ================")
    cliente, conta = recuperar_conta_cliente(clientes)
    if not (cliente and conta):
        return

    print(conta.historico.gerar_relatorio())
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")


def listar_clientes_contas(clientes):
    """Exibe todos os clientes e suas respectivas contas."""
    if not clientes:
        print("\n--- Não há clientes cadastrados. ---")
        return

    print("\n========== Clientes e Contas ==========")
    for cliente in clientes:
        print(f"Nome: {cliente.nome} | CPF: {cliente.cpf}")
        if cliente.contas:
            print("  Contas:")
            for conta in cliente.contas:
                print(f"    - Agência: {conta.agencia} | Conta: {conta.numero} | Saldo: R$ {conta.saldo:.2f}")
        else:
            print("  - Nenhuma conta vinculada.")
        print("-" * 30)
    print("========================================")


# --- Menu Principal ---

def main():
    """Função principal que executa o menu do sistema bancário."""
    clientes = []  # Lista para armazenar Clientes
    contas = []  # Lista para armazenar contas (ou ContasCorrente)
    numero_conta_sequencial = 1  # Contador sequencial para o número da conta

# Definição do menu visualmente um pouco melhor
    menu = """
================ MENU ================
[c] Cadastrar Usuário
[cc] Criar Conta Corrente
[lc] Listar Clientes e Contas
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
Escolha uma opção:
Pressione enter para continuar...
======================================
=> """

    print("Bem-vindo ao sistema bancário POO!")

    while True:
        opcao = input(menu).strip().lower()

        if opcao == 'c':
            cadastrar_cliente(clientes) # Passa a lista de usuários

        elif opcao == 'cc':
            # Passa a lista de clientes para buscar, e a lista de contas para adicionar
            resultado = criar_conta_corrente(numero_conta_sequencial, clientes, contas)
            if resultado is not None: 
                numero_conta_sequencial = resultado  # Atualiza o contador apenas sequencial

        elif opcao == 'l' or opcao == 'lc':  # Adicionei 'l' como atalho, e 'lc' para ser mais descritivo
             listar_clientes_contas(clientes) 

        elif opcao in ('d'):
            realizar_deposito(clientes)

        elif opcao == 's':
            realizar_saque(clientes) 

        elif opcao == 'e':
            exibir_extrato(clientes)          

        elif opcao == 'q':
            print("\nObrigado por usar nosso sistema modularizado. Até logo!")
            break

        else:
            print("\nOperação inválida. Por favor, selecione novamente a operação desejada.")

# Executa a função principal quando o script é rodado
if __name__ == "__main__":
    main()

# O código foi modularizado para facilitar a manutenção e a legibilidade.

