Explicação das Mudanças e Adições:

Modularização com Funções:

As lógicas de depósito (depositar), saque (sacar) e visualização de extrato (visualizar_extrato) foram movidas para funções separadas.
Tipos de Argumentos das Funções de Operação:

depositar(saldo, valor, extrato, /): Usa / no final dos parâmetros. Isso significa que saldo, valor e extrato devem ser passados por posição (na ordem definida) ao chamar a função. Ex: depositar(conta['saldo'], 100.0, conta['extrato']).
sacar(*, saldo, valor, extrato, limite, numero_saques, limite_saques): Usa * no início dos parâmetros. Isso significa que saldo, valor, extrato, limite, numero_saques e limite_saques devem ser passados por nome (keyword arguments) ao chamar a função. Ex: sacar(saldo=conta['saldo'], valor=50.0, extrato=conta['extrato'], ...)
visualizar_extrato(saldo, *, extrato): saldo deve ser passado por posição (devido ao / implícito antes do *), e extrato deve ser passado por nome (devido ao *). Ex: visualizar_extrato(conta['saldo'], extrato=conta['extrato']).
Novas Funções de Cadastro:

criar_usuario(usuarios):
Recebe a lista usuarios como argumento.
Pede nome, data de nascimento, CPF e endereço.
Usa a função auxiliar filtrar_usuario para verificar se o CPF já existe na lista.
Se o CPF não existe, cria um dicionário representando o usuário e o adiciona à lista usuarios.
Imprime mensagens de sucesso ou erro.
criar_conta_corrente(agencia, numero_conta_sequencial, usuarios, contas):
Recebe a agência padrão, o contador sequencial de contas e as listas usuarios e contas.
Pede o CPF do usuário para quem a conta será criada.
Usa filtrar_usuario para encontrar o usuário na lista usuarios.
Se o usuário for encontrado, incrementa o contador sequencial para obter o novo número da conta.
Cria um dicionário para a conta, incluindo a agência, o novo número sequencial, o dicionário do usuario (vinculando a conta ao usuário), saldo inicial (0.0), uma lista vazia para o extrato, o contador de numero_saques_hoje (0) e o contador de numero_transacoes_hoje (0).
Adiciona o dicionário da conta à lista contas.
Imprime mensagens de sucesso com os dados da nova conta.
Retorna o próximo número sequencial a ser usado.
filtrar_usuario(cpf, usuarios): Função auxiliar simples que busca um usuário na lista usuarios pelo CPF e retorna o dicionário do usuário ou None.
recuperar_conta(contas): Função auxiliar que solicita a agência e o número da conta ao usuário e busca a conta correspondente na lista contas, retornando o dicionário da conta ou None.
Estruturas de Dados:

usuarios: Uma lista onde cada elemento é um dicionário representando um usuário ({'nome': ..., 'cpf': ..., ...}).
contas: Uma lista onde cada elemento é um dicionário representando uma conta ({'agencia': ..., 'numero_conta': ..., 'usuario': {...}, 'saldo': ..., 'extrato': [...], ...}). O dicionário da conta inclui uma referência ao dicionário do usuário.
O extrato dentro de cada conta continua sendo uma lista de dicionários para armazenar detalhes da transação, incluindo data/hora.
Lógica no main():

As listas usuarios e contas são inicializadas no início da função main().
O loop principal agora inclui opções para 'c' (cadastrar usuário) e 'cc' (cadastrar conta).
Para as operações 'd', 's' e 'e', o programa primeiro chama recuperar_conta para encontrar a conta na lista contas com base na entrada do usuário.
Se a conta for encontrada (conta_cliente é um dicionário válido), a lógica da operação específica é executada, passando os dados relevantes da conta_cliente (como saldo, extrato, numero_saques_hoje) como argumentos para as funções modulares (depositar, sacar, visualizar_extrato).
Após a chamada das funções depositar ou sacar, os valores de retorno (novo_saldo, novo_extrato, etc.) são usados para atualizar o dicionário conta_cliente na lista contas.
O limite de MAX_TRANSACOES_DIARIAS é verificado para a conta_cliente específica antes de permitir as operações de depósito ou saque. O contador numero_transacoes_hoje é incrementado dentro do main após uma operação válida (depósito ou saque) ser concluída para aquela conta.
Tratamento de Entrada de Valor (Floats):

Adicionei try-except ValueError para a conversão de entrada para float nos depósitos e saques, corrigindo a falha que existia na versão anterior.
Data e Hora no Extrato:

Mantido o uso de datetime.now() e o armazenamento da data/hora nos dicionários de transação dentro do extrato de cada conta. A exibição no extrato também formata a data/hora.
Este código é significativamente mais complexo devido à modularização, gestão de usuários e contas