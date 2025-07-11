# Sistema Bancário - Conta

## Estrutura da Classe Conta

A classe `Conta` é responsável por representar uma conta bancária genérica. Ela serve como base para outras classes, como `ContaCorrente`. Abaixo estão os principais atributos e métodos da classe.

### Atributos

- **agencia**: Número da agência bancária.
- **numero**: Número da conta.
- **saldo**: Saldo atual da conta.
- **cliente**: Cliente associado à conta.
- **historico**: Histórico de transações da conta.

### Métodos

#### `__init__(self, agencia, numero, cliente)`

Construtor que inicializa uma conta com os dados fornecidos.

#### `depositar(self, valor)`

Adiciona um valor ao saldo da conta e registra a transação no histórico.

#### `sacar(self, valor)`

Realiza um saque, verificando se há saldo suficiente. Registra a transação no histórico.

#### `exibir_extrato(self)`

Exibe o histórico de transações e o saldo atual.

#### `__str__(self)`

Retorna uma representação em string da conta, incluindo informações como agência, número e cliente.

---

## Estrutura da Classe ContaCorrente

A classe `ContaCorrente` herda de `Conta` e adiciona funcionalidades específicas para contas correntes.

### Atributos Adicionais

- **limite_saque**: Valor máximo permitido para um saque.
- **saques_diarios**: Número máximo de saques permitidos por dia.
- **contador_saques**: Contador de saques realizados no dia.

### Métodos Adicionais

#### `sacar(self, valor)`

Implementa a lógica de saque com validações específicas:

- Verifica se o valor do saque está dentro do limite permitido.
- Verifica se o número de saques diários não foi excedido.

#### `resetar_limites_diarios(self)`

Reseta os limites diários de saques, caso a data atual seja diferente da última transação.

---

## Exemplo de Uso

### Criar uma Conta

```python
cliente = Cliente(nome="Maria Silva", cpf="12345678900")
conta = Conta(agencia="0001", numero=1, cliente=cliente)
```
