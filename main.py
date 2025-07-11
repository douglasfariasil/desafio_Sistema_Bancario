import textwrap  # Para formatar o endereço
from datetime import datetime  # Para timesta
from pathlib import Path  # Para manipulação de caminhos de arquivos

# --- Constantes ---
AGENCIA_PADRAO = "0001"  # Agência padrão para todas as contas
LIMITE_SAQUE_VALOR = 1000.0  # Limite de saque por transação
LIMITE_SAQUES_DIARIOS = 3  # Limite de saques diários
MAX_TRANSACOES_DIARIAS = 6  # Novo limite de transações

ROOT_PATH = Path(__file__).parent  # Caminho raiz do projeto


# --- Decoradores ---
def log_transacoes(func):
    def wrapper(*args, **kwargs):
        resultado = func(*args, **kwargs)
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        nome_funcao = func.__name__
        args_str = ", ".join(repr(arg) for arg in args)
        kwargs_str = ", ".join(f"{k}={repr(v)}" for k, v in kwargs.items())

        if args_str and kwargs_str:
            argumentos = f"({args_str}, {kwargs_str})"
        elif args_str:
            argumentos = f"({args_str})"
        elif kwargs_str:
            argumentos = f"({kwargs_str})"
        else:
            argumentos = "()"

        valor_retornado = repr(resultado)
        data_hora = f"[{data_hora}] Função: {nome_funcao}{argumentos} | Retorno: {valor_retornado}\n"
        data_hora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(ROOT_PATH / "log.txt", "a") as arquivo:
            arquivo.write(f"{data_hora} - {func.__name__} executado com sucesso.\n")
        if isinstance(resultado, Conta):
            print(
                f"\nDEBUG: Transação registrada {func.__name__} na conta {resultado.numero}."
            )
        return resultado

    return wrapper


# --- Classes de Base (POO) ---
class Pessoa:
    """Classe base para representar uma pessoa."""

    def __init__(self, nome, data_nascimento, endereco):
        self._nome = nome
        self._data_nascimento = data_nascimento
        self._endereco = endereco

    @property
    def nome(self):
        return self._nome

    @property
    def data_nascimento(self):
        return self._data_nascimento

    @property
    def endereco(self):
        return self._endereco


class PessoaFisica(Pessoa):
    """Classe que representa uma pessoa física, herda de Pessoa."""

    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(nome, data_nascimento, endereco)
        if not cpf.isdigit() or len(cpf) != 11:
            raise ValueError("CPF inválido! Deve conter 11 dígitos numéricos.")
        self._cpf = cpf  # Armazena o CPF da pessoa física

    @property
    def cpf(self):
        return self._cpf  # Retorna o CPF da pessoa física


class Cliente(PessoaFisica):
    """Classe que representa um cliente do banco, herda de PessoaFisica."""

    def __init__(self, nome, data_nascimento, cpf, endereco):
        super().__init__(nome, data_nascimento, cpf, endereco)
        self._contas = []  # Lista de contas vinculadas ao cliente

    @property
    def contas(self):
        return self._contas

    def adicionar_conta(self, conta):
        self._contas.append(conta)
        print(
            f"DEBUG: Conta {conta.numero} adicionada ao cliente {self.nome}."
        )  # DEBUG

    @log_transacoes
    def realizar_transacao(self, conta, transacao_obj):
        """Realiza uma transação na conta do cliente."""
        if not isinstance(conta, Conta):
            print("\n--- Erro: O objeto fornecido não é uma conta válida. ---")
            return False
        if conta not in self.contas:
            print("\n--- Erro: Esta conta não pertence a este cliente. ---")
            return False
        return transacao_obj.registrar(
            conta
        )  # Registra a transação na conta do cliente


class Historico:
    """Classe que armazena o histórico de transações bancárias."""

    def __init__(self):
        self._transacoes = []

    @property
    def transacoes(self):
        return self._transacoes

    def adicionar_transacao(self, transacao):
        self._transacoes.append(transacao)

    def gerar_relatorio(self):
        """Exibe o extrato das transações."""
        if not self._transacoes:
            return "Nenhuma movimentação realizada."
        relatorio = []
        for transacao in self._transacoes:
            data_hora_formatada = transacao.data_hora.strftime("%d/%m/%Y %H:%M:%S")
            tipo_transacao = transacao.tipo
            valor_transacao = transacao.valor
            relatorio.append(
                f"{data_hora_formatada} - {tipo_transacao}: R$ {valor_transacao:.2f}"
            )
        return "\n".join(relatorio)  # Retorna o relatório formatado das transações


class Transacao:
    """Classe base para transações bancárias."""

    def __init__(self, valor):
        if valor <= 0:
            raise ValueError("O valor da transação deve ser positivo.")
        self._valor = valor
        self._data_hora = datetime.now()
        self._tipo = "Transação"

    @property
    def valor(self):
        return self._valor

    @property
    def data_hora(self):
        return self._data_hora

    @property
    def tipo(self):
        return self._tipo

    def registrar(self, conta):
        """Registra a transação na conta, deve ser implementado por subclasses."""
        raise NotImplementedError(
            "Método 'registrar' deve ser implementado pela subclasse."
        )


class Deposito(Transacao):
    """Representa uma operação de depósito."""

    def __init__(self, valor):
        super().__init__(valor)
        self._tipo = "Depósito"

    def registrar(self, conta):
        """Registra o depósito na conta, verificando as condições necessárias."""
        if conta._incrementar_transacao_diaria():
            conta._creditar(self.valor)
            conta.historico.adicionar_transacao(self)
            print(
                f"\nDepósito de R$ {self.valor:.2f} realizado com sucesso na,"
                " conta {conta.agencia}/{conta.numero}!"
            )
            return True  # Retorna True se o depósito for registrado com sucesso
        return False


class Saque(Transacao):
    """Representa uma operação de saque."""

    def __init__(self, valor):
        super().__init__(valor)
        self._tipo = "Saque"

    def registrar(self, conta):
        """Registra o saque na conta, verificando as condições necessárias."""
        if self.valor > conta.saldo:
            print("\nOperação falhou! Você não tem saldo insuficiente.")
            return False  # Verifica se o valor do saque não excede o saldo
        if self.valor > conta.limite_saque:
            print(
                f"\nOperação falhou! O valor do saque (R$ {self.valor:.2f}),"
                "excede o limite de R$ {conta.limite_saque:.2f} por saque."
            )

            return False  # Verifica se o valor do saque não excede o limite
        if conta.numero_saques_hoje >= conta.limite_saques_diarios:
            print(
                f"\nOperação falhou! Número máximo de {conta.limite_saques_diarios} saques diários excedido."
            )
            return False  # Verifica se o limite diário de saques foi atingido
        if conta._incrementar_transacao_diaria():
            conta._debitar(self.valor)
            conta.historico.adicionar_transacao(self)
            conta._incrementar_saque_diario()
            print(
                f"\nSaque de R$ {self.valor:.2f} realizado com sucesso na conta {conta.agencia}/{conta.numero}!"
            )
            return True
        return False  # Retorna False se o limite diário de transações for atingido


class Conta:
    """Classe base que representa uma conta bancária."""

    def __init__(self, numero, cliente):
        self._agencia = AGENCIA_PADRAO
        self._numero = numero
        self._cliente = cliente
        self._saldo = 0.0
        self._historico = Historico()
        self._numero_saques_hoje = 0
        self._numero_transacoes_hoje = 0
        self._ultima_data_transacao = datetime.now().date()

    @classmethod
    def nova_conta(cls, numero, cliente):
        """Cria uma nova conta vinculada a um cliente."""
        return cls(numero, cliente)

    @property
    def saldo(self):
        return self._saldo

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
        self._resetar_limites_diarios()
        return self._numero_saques_hoje

    @property
    def numero_transacoes_hoje(self):
        self._resetar_limites_diarios()
        return self._numero_transacoes_hoje

    def _resetar_limites_diarios(self):
        """Reseta os limites diários de saques e transações se a data atual
        for diferente da última transação."""
        hoje = datetime.now().date()
        if hoje > self._ultima_data_transacao:
            self._numero_saques_hoje = 0
            self._numero_transacoes_hoje = 0
            self._ultima_data_transacao = hoje

    def _creditar(self, valor):
        self._saldo += valor

    def _debitar(self, valor):
        self._saldo -= valor

    def _incrementar_saque_diario(self):
        self._numero_saques_hoje += 1

    def _incrementar_transacao_diaria(self):
        self._resetar_limites_diarios()
        if self._numero_transacoes_hoje >= MAX_TRANSACOES_DIARIAS:
            # Verifica se o limite diário de transações foi atingido
            print(
                f"\n--- Erro: Limite de {MAX_TRANSACOES_DIARIAS} transações diárias,"
                "atingido para a conta {self.agencia}/{self.numero}. ---"
            )  # Mensagem de erro se o limite diário for atingido
            return False  # Retorna False se o limite diário de transações for atingido
        self._numero_transacoes_hoje += 1
        return True  # Retorna True se a transação for registrada com sucesso

    def sacar(self, valor):
        """Realiza um saque na conta."""
        raise NotImplementedError(
            "Método 'sacar' deve ser implementado pela subclasse."
        )

    def depositar(self, valor):
        """Realiza um depósito na conta."""
        transacao = Deposito(valor)
        return transacao.registrar(self)

    def __str__(self):
        """Representação em string da conta."""
        return f"Agência:\t{self.agencia}\nConta:\t\t{self.numero}\nCliente:\t{self.cliente.nome}"


class ContaCorrente(Conta):
    """Classe que representa uma conta corrente, herda de Conta."""

    def __init__(
        self,
        numero,
        cliente,
        limite_saque=LIMITE_SAQUE_VALOR,
        limite_saques_diarios=LIMITE_SAQUES_DIARIOS,
    ):
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
        try:
            transacao = Saque(valor)  # Cria o objeto de transação de saque
            return transacao.registrar(self)
        except ValueError as e:
            print(f"\nOperação falhou! {e}")
            return False

    def __str__(self):
        return textwrap.dedent(
            f"""\
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
        if not cpf.isdigit() or len(cpf) != 11: # Exemplo de validação de CPF (apenas números, 11 dígitos)
            raise ValueError("CPF inválido! Deve conter 11 dígitos numéricos.")
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
    

# --- Funções Auxiliares do Sistema ---
def buscar_cliente(cpf, clientes):
    """Busca um cliente na lista de clientes pelo CPF."""
    print(f"DEBUG: Tentando buscar cliente com CPF: {cpf}")  # DEBUG
    for cliente in clientes:
        print(
            f"DEBUG: Comparando com CPF do cliente existente: {cliente.nome} com CPF {cliente.cpf}"
        )  # DEBUG
        if cliente.cpf == cpf:
            print(f"DEBUG: Cliente encontrado: {cliente.nome}")  # DEBUG
            return cliente
    print("DEBUG: Cliente não encontrado na lista de clientes.")  # DEBUG
    return None  # Retorna None se o cliente não for encontrado


def recuperar_conta_cliente(clientes):
    """Recupera o cliente e a conta do cliente a partir do CPF informado."""
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
        print(
            f"  {i + 1}. Agência: {conta.agencia}, Conta: {conta.numero}, Saldo: R$ {conta.saldo:.2f}"
        )  # Exibe as contas do cliente

    try:
        idx_conta = (
            int(input("Selecione o número da conta (ex: 1 para a primeira): ")) - 1
        )
        if 0 <= idx_conta < len(cliente.contas):
            conta = cliente.contas[idx_conta]
            return cliente, conta
        else:
            print("\n--- Erro: Índice de conta inválido. ---")
            return None, None
    except ValueError:
        print("\n--- Erro: Entrada inválida. Digite um número. ---")
        return (
            None,
            None,
        )  # Retorna None se a conta não for encontrada ou se a entrada for inválida


# --- Funções para Opções do Menu ---
@log_transacoes
def cadastrar_cliente(clientes):
    """Cadastra um novo cliente no sistema."""
    cpf = input("Informe o CPF (somente números): ")
    if buscar_cliente(cpf, clientes):
        print("\n--- Erro: Já existe cliente com este CPF! ---")
        return False

    nome = input("Informe o nome completo: ")
    data_nascimento = input("Informe a data de nascimento (dd-mm-aaaa): ")
    endereco = input(
        "Informe o endereço (logradouro, numero - bairro - cidade/sigla estado): "
    )

    try:
        novo_cliente = Cliente(nome, data_nascimento, cpf, endereco)
        clientes.append(novo_cliente)
        print("\n--- Cliente cadastrado com sucesso! ---")
        print(
            f"DEBUG: Cliente '{novo_cliente.nome}' (CPF: {novo_cliente.cpf}) CADASTRADO, "
            " e adicionado à lista de clientes."
        )  # DEBUG
        return True
    except ValueError as e:
        print(f"\n--- Erro ao cadastrar cliente: {e} ---")
        return False  # Retorna False se o cadastro falhar


@log_transacoes
def criar_conta_corrente(numero_conta, clientes, contas):
    """Cria uma nova conta corrente vinculada a um cliente existente."""
    cpf = input("Informe o CPF do cliente para vincular a conta: ")
    cliente = buscar_cliente(cpf, clientes)

    if not cliente:
        print("\n--- Erro: Cliente não encontrado! ---")
        print("DEBUG: Falha ao encontrar cliente para criar conta.")  # DEBUG
        return None

    print(
        f"DEBUG: Cliente '{cliente.nome}' (CPF: {cliente.cpf}) ENCONTRADO para criar conta."
    )  # DEBUG
    # Verifica se o cliente já possui uma conta com o mesmo número
    nova_conta = ContaCorrente.nova_conta(numero_conta, cliente)
    contas.append(nova_conta)
    cliente.adicionar_conta(nova_conta)  # Adiciona a nova conta ao cliente

    print(
        f"\n--- Conta {AGENCIA_PADRAO}/{nova_conta.numero} criada com sucesso para {cliente.nome}! ---"
    )
    return numero_conta + 1  # Retorna o próximo número de conta sequencial


@log_transacoes
def realizar_deposito(clientes):
    """Realiza um depósito na conta do cliente."""
    cliente, conta = recuperar_conta_cliente(clientes)
    if not (cliente and conta):
        return False
    try:
        valor = float(input("Informe o valor do depósito: R$ "))
        transacao_obj = Deposito(valor)  # Cria o objeto de transação de depósito
        return cliente.realizar_transacao(conta, transacao_obj)
    except ValueError as e:
        print(f"\n--- Erro: Entrada inválida. {e} ---")
        return False  # Retorna False se a transação falhar ou for cancelada


@log_transacoes
def realizar_saque(clientes):
    """Realiza um saque na conta do cliente."""
    cliente, conta = recuperar_conta_cliente(clientes)
    if not (cliente and conta):
        return False
    try:
        valor = float(input("Informe o valor do saque: R$ "))
        transacao_obj = Saque(valor)  # Cria o objeto de transação de saque
        return cliente.realizar_transacao(conta, transacao_obj)
    except ValueError as e:
        print(f"\n--- Erro: Entrada inválida. {e} ---")
        return False  # Retorna False se a transação falhar ou for cancelada


@log_transacoes
def exibir_extrato(clientes):
    """Exibe o extrato da conta do cliente."""
    print("\n================ EXTRATO ================")
    cliente, conta = recuperar_conta_cliente(clientes)
    if not (cliente and conta):
        return "Operação de extrato falhou ou cancelada."
    relatorio = conta.historico.gerar_relatorio()
    print(relatorio)
    print(f"\nSaldo atual: R$ {conta.saldo:.2f}")
    print("========================================")
    return f"\nExtrato gerado para conta {conta.agencia}/{conta.numero}. Saldo: R$ {conta.saldo:.2f}"


@log_transacoes
def listar_contas(clientes):
    """Lista todos os clientes e suas contas cadastradas."""
    if not clientes:
        print("\n--- Não há clientes cadastrados. ---")
        return "Nenhum cliente cadastrado."

    print("\n========== Clientes e Contas ==========")
    log_output = []
    for cliente in clientes:
        log_output.append(f"Cliente: {cliente.nome} | CPF: {cliente.cpf}")
        print(f"Nome: {cliente.nome} | CPF: {cliente.cpf}")
        if cliente.contas:
            print("  Contas:")
            for conta in cliente.contas:
                log_output.append(
                    f"    - Agência: {conta.agencia} | Conta: {conta.numero},"
                    " | Saldo: R$ {conta.saldo:.2f}"
                )
                print(
                    f"    - Agência: {conta.agencia} | Conta: {conta.numero},"
                    " | Saldo: R$ {conta.saldo:.2f}"
                )
        else:
            log_output.append("  - Nenhuma conta vinculada.")
            print("  - Nenhuma conta vinculada.")
        print("-" * 30)
    print("========================================")
    return "\n".join(log_output)  # Log de contas e clientes listados


# --- Menu Principal ---
def main():
    """Função principal que executa o menu do sistema bancário."""
    clientes = []  # Lista de clientes
    contas = []  # Lista de contas
    numero_conta_sequencial = 1

    menu = """
================ MENU ================
Escolha uma opção:
[c] Cadastrar Usuário
[cc] Criar Conta
[lc] Listar Contas
[d] Depositar
[s] Sacar
[e] Extrato
[q] Sair
Pressione enter para continuar...
======================================
=> """

    print("Bem-vindo ao sistema bancário POO!")

    while True:
        opcao = input(menu).strip().lower()

        if opcao == "c":  # Cadastrar usuário
            cadastrar_cliente(clientes)

        elif opcao == "cc":  # Criar conta corrente
            resultado = criar_conta_corrente(numero_conta_sequencial, clientes, contas)
            if resultado is not None:
                numero_conta_sequencial = (
                    resultado  # Atualiza o número da conta sequencial
                )

        elif opcao == "lc":  # Listar contas
            listar_contas(clientes)

        elif opcao == "d":  # Realizar depósito
            realizar_deposito(clientes)

        elif opcao == "s":  # Realizar saque
            realizar_saque(clientes)

        elif opcao == "e":  # Exibir extrato
            exibir_extrato(clientes)

        elif opcao == "q":  # Sair do sistema
            print("\nObrigado por usar nosso sistema modularizado. Até logo!")
            break

        else:
            print(
                "\nOperação inválida. Por favor, selecione novamente a operação desejada."
            )


if __name__ == "__main__":
    main()
