from datetime import datetime

usuarios = []
contas = []

class Conta:
    def __init__(self, cliente, saldo=0):
        self.saldo = saldo
        self.cliente = cliente
        self.historico = {}
        self.contagem = 0
        self.data_ultimo_saque = None
        self.LIMITE_SAQUES = 3

    def depositar(self, valor):
        if valor <= 0:
            print("O valor precisa ser maior que zero.")
            return
        self.saldo += valor
        data_hora = self.get_data_hora()
        self.historico[data_hora] = f"Depósito: +R$ {valor:.2f}"
        print(f"Depósito de R$ {valor:.2f} realizado com sucesso.")

    def sacar(self, valor):
        data_atual = datetime.now().date()

        if self.data_ultimo_saque and self.data_ultimo_saque.date() != data_atual:
            self.contagem = 0

        if self.contagem >= self.LIMITE_SAQUES:
            print("Limite diário de saques atingido (3 saques).")
            return

        if valor <= 0:
            print("O valor precisa ser maior que zero.")
            return
        if valor > 500:
            print("Limite de saque: R$ 500.")
            return
        if valor > self.saldo:
            print("Saldo insuficiente.")
            return

        self.saldo -= valor
        self.data_ultimo_saque = datetime.now()
        self.contagem += 1
        data_hora = self.get_data_hora()
        self.historico[data_hora] = f"Saque: -R$ {valor:.2f}"
        print(f"Saque de R$ {valor:.2f} realizado com sucesso.")

    def extrato(self):
        print(f"\n=== Extrato da Conta de {self.cliente['nome']} ===")
        if not self.historico:
            print("Nenhuma movimentação registrada.")
        else:
            for data, operacao in self.historico.items():
                print(f"{data}: {operacao}")
        print(f"Saldo atual: R$ {self.saldo:.2f}")

    def get_data_hora(self):
        return datetime.now().strftime("%d/%m/%Y %H:%M:%S")

def procurar_usuario(cpf):
    for usuario in usuarios:
        if usuario["cpf"] == cpf:
            return usuario
    return None

def criar_usuario():
    cpf = input("CPF (somente números): ")
    if procurar_usuario(cpf):
        print("Já existe usuário com esse CPF.")
        return
    nome = input("Nome completo: ")
    data_nasc = input("Data de nascimento (dd/mm/aaaa): ")
    endereco = input("Endereço (logradouro, nº - bairro - cidade/UF): ")
    usuarios.append({
        "nome": nome,
        "cpf": cpf,
        "data_nasc": data_nasc,
        "endereco": endereco
    })
    print("Usuário criado com sucesso!")

def criar_conta():
    cpf = input("Informe o CPF do usuário: ")
    usuario = procurar_usuario(cpf)
    if not usuario:
        print("Usuário não encontrado. Cadastre o usuário primeiro.")
        return
    conta = Conta(cliente=usuario)
    contas.append(conta)
    print("Conta criada com sucesso!")

def listar_contas():
    if not contas:
        print("Nenhuma conta cadastrada.")
        return
    for i, conta in enumerate(contas, start=1):
        cliente = conta.cliente
        print(f"\nConta {i}: {cliente['nome']} | CPF: {cliente['cpf']} | Saldo: R$ {conta.saldo:.2f}")

# Menu principal
menu = """
========== MENU ==========
[d] Depositar
[s] Sacar
[e] Extrato
[nc] Nova conta
[lc] Listar contas
[nu] Novo usuário
[q] Sair
> """

while True:
    opcao = input(menu).strip().lower()

    if opcao == "d":
        if not contas:
            print("Nenhuma conta disponível.")
            continue
        listar_contas()
        indice = int(input("Escolha o número da conta para depósito: ")) - 1
        valor = float(input("Valor do depósito: "))
        contas[indice].depositar(valor)

    elif opcao == "s":
        if not contas:
            print("Nenhuma conta disponível.")
            continue
        listar_contas()
        indice = int(input("Escolha o número da conta para saque: ")) - 1
        valor = float(input("Valor do saque: "))
        contas[indice].sacar(valor)

    elif opcao == "e":
        if not contas:
            print("Nenhuma conta disponível.")
            continue
        listar_contas()
        indice = int(input("Escolha o número da conta para ver extrato: ")) - 1
        contas[indice].extrato()

    elif opcao == "nu":
        criar_usuario()

    elif opcao == "nc":
        criar_conta()

    elif opcao == "lc":
        listar_contas()

    elif opcao == "q":
        print("Saindo do sistema. Obrigado!")
        break

    else:
        print("Opção inválida. Tente novamente.")
