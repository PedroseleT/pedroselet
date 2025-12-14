import json

def carregar_dados():
    global usuarios
    try:
        with open('invest_usuarios.json', 'r', encoding='utf8') as arquivo:
            usuarios = json.load(arquivo)
    except:
        usuarios = {}

def salvar_dados():
    with open('invest_usuarios.json', 'w', encoding='utf8') as arquivo:
        json.dump(usuarios, arquivo, indent=2)

def menu(usuario):
    global opcao
    print('-' * 30)
    print(f'Usuário ativo: \033[32m{usuario.capitalize()}\033[m')
    print('''[1] - Cadastrar ativo
[2] - Registrar compra
[3] - Registrar venda
[4] - Exibir carteira
[5] - Ver extrato
[0] - Sair''')
    print('-' * 30)
    opcao = int(input('Digite sua opção: '))

def login():
    print('-' * 30)
    print('TELES INVESTIMENTOS'.center(30))
    print('-' * 30)
    cont = 0
    while True:
        usuario = input('Usuário: ')

        if usuario not in usuarios:
            senha = input('Usuário novo! Basta criar sua nova senha: ')
            usuarios[usuario] = {'senha' : senha,
                                 'ativos' : [],
                                 'extrato': []
            }
            salvar_dados()
            menu(usuario)
            return usuario

        else:
            senha = input('Senha: ')
            while senha != usuarios[usuario]['senha']:
                cont += 1
                print('\033[31mSenha incorreta.\033[m')
                senha = input('Tente novamente: ')
                if cont >= 3:
                    print('\033[31mAcesso proibido por multiplas tentativas.\033[m')
                    return None
            
            if 'extrato' not in usuarios[usuario]:
                usuarios[usuario]['extrato'] = []
            if 'ativos' not in usuarios[usuario]:
                usuarios[usuario]['ativos'] = []

            salvar_dados()
            menu(usuario)
            return usuario
                    
def cadastrar_ativo(usuario):
    print('-' * 30)
    print('CADASTRAR ATIVO'.center(30))
    print('-' * 30)

    ativo_cadastro = input('Nome do ativo: ').lower()
    tipo_ativo_cadastro = input('Tipo do ativo: ').lower()

    usuarios[usuario]['ativos'].append({
        'nome': ativo_cadastro,
        'tipo': tipo_ativo_cadastro,
        'quantidade': 0,
        'preco_medio': 0
    })

    salvar_dados()
    print('\033[32mAtivo cadastrado com sucesso!\033[m\n')

def registrar_compra(usuario):
    print('-' * 30)
    print('REGISTRAR COMPRA'.center(30))
    print('-' * 30)
    # Verificar se o ativo existe na carteira
    ativo_encontrado = None
    ativo_compra = input('Nome do ativo: ').lower()
    for ativo in usuarios[usuario]['ativos']:
        if ativo_compra == ativo['nome']:
            ativo_encontrado = ativo

            if 'quantidade' not in ativo_encontrado:
                ativo_encontrado['quantidade'] = 0
            if 'preco_medio' not in ativo_encontrado:
                ativo_encontrado['preco_medio'] = 0
            break

        if ativo_encontrado is None:
            print('\033[31mEste ativo não existe na carteira.\033[m')
            return


    # Pedir quantidade
    quantidade_compra = int(input('Quantidade comprada: '))
    if quantidade_compra <= 0:
        print('\033[31mQuantidade inválida.\033[m')
        return
    
    # Pedir preço de compra
    preco_compra = float(input('Preço por unidade (R$): '))

    # Atualizar posição
    quantidade_total_antiga = ativo_encontrado['quantidade']
    valor_total_antigo = quantidade_total_antiga * ativo_encontrado['preco_medio']

    valor_compra = quantidade_compra * preco_compra

    # Novo preço médio
    novo_preco_medio = (valor_total_antigo + valor_compra) / (quantidade_total_antiga + quantidade_compra)

    # Salvar alterações
    ativo_encontrado['quantidade'] += quantidade_compra
    ativo_encontrado['preco_medio'] = novo_preco_medio

    # Registrar no extrato
    usuarios[usuario]['extrato'].append({
        'tipo': 'compra',
        'ativo': ativo_compra,
        'quantidade': quantidade_compra,
        'preco': preco_compra
    })
    salvar_dados()

    print('\033[33mCompra registrada com sucesso!\033[m')
    print()
    print(f'Novo preço médio: R$ {novo_preco_medio:.2f}')
    print(f'Quantidade total atual: {ativo_encontrado["quantidade"]}')

def registrar_venda(usuario):
    print('-' * 30)
    print('REGISTRAR VENDA'.center(30))
    print('-' * 30)
    
    ativo_venda_encontrado = None
    ativo_venda = input('Nome do ativo: ').lower()

    # VERIFICANDO ATIVOS
    for ativo in usuarios[usuario]['ativos']:
        if ativo_venda == ativo['nome']:
            ativo_venda_encontrado = ativo
            break

    if ativo_venda_encontrado is None:
        print('\033[31mEste ativo não existe.\033[m')
        return
        
    # VENDENDO ATIVOS
    quantidade_venda = int(input('Quantidade a vender: '))

    if quantidade_venda <= 0 or quantidade_venda > ativo_venda_encontrado['quantidade']:
        print('\033[31mDigite uma quantidade válida\033[m')
        return

    preco_venda = int(input('Preço de venda (R$): '))
    custo = quantidade_venda * ativo_venda_encontrado['preco_medio']
    valor_venda = quantidade_venda * preco_venda
    resultado = valor_venda - custo

    # ATUALIZAÇÃO
    ativo_venda_encontrado['quantidade'] -= quantidade_venda

    # EXTRATO
    usuarios[usuario]['extrato'].append({
        'tipo' : 'venda',
        'ativo' : ativo_venda,
        'quantidade' : quantidade_venda,
        'preco' : preco_venda,
        'resultado' : resultado
    })

    salvar_dados()
    print('-' * 30)
    print()
    print(f'\033[32mVenda concluída!\033[m')
    print(f'Ativo: \033[33m{ativo_venda_encontrado['nome'].upper()}\033[m')
    print(f'Quantidade restante: {ativo_venda_encontrado['quantidade']}')
    print(f'Resultado da venda: R$ {resultado:.2f}')

def exibir_carteira(usuario):
    print('-' * 30)
    print('Minha Carteira'.center(30))
    print('-' * 30)
    
    if usuarios[usuario]['ativos']:
        total_ativos = 0
        total_investido = 0
        for ativo in usuarios[usuario]['ativos']:
            total_ativos += 1
            total_investido += ativo['quantidade'] * ativo['preco_medio']
            print(f'Ativo: {ativo['nome']}')
            print(f'Tipo: {ativo['tipo']}')
            print(f'Quantidade: {ativo['quantidade']}')
            print(f'Preço médio: {ativo['preco_medio']}')
            print(f'Valor investido: {ativo['quantidade'] * ativo['preco_medio']}')
            print('-' * 30)

        print('RESUMO DA CARTEIRA')
        print('Total de ativos:', total_ativos)
        print('Valor total investido:', total_investido)
    else:
        print('SEM INVESTIMENTOS'.center(30))

def ver_extrato(usuario):
    print('-' * 30)
    print('Meu Extrato'.center(30))
    print('-' * 30)
    print(*usuarios[usuario]['extrato'], sep='\n')
    
# ------------------ EXECUÇÃO PRINCIPAL ------------------
carregar_dados()
usuario_logado = login()
while True:
    if opcao == 1:
        cadastrar_ativo(usuario_logado)

    elif opcao == 2:
        registrar_compra(usuario_logado)

    elif opcao == 3:
        registrar_venda(usuario_logado)

    elif opcao == 4:
        exibir_carteira(usuario_logado)
    
    elif opcao == 5:
        ver_extrato(usuario_logado)

    elif opcao == 0:
        print("Saindo...")
        salvar_dados()
        break
    menu(usuario_logado)

