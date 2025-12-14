import json
from time import sleep

def carregar_dados():
    global usuarios, livros, emprestimos
    try:
        with open('biblioteca_usuarios.json', 'r') as arquivo:
            usuarios = json.load(arquivo)
    except:
        usuarios = {}
    
    try:
        with open('biblioteca_livros.json', 'r') as arquivo:
            livros = json.load(arquivo)
    except:
        livros = {}

    try:
        with open('biblioteca_emprestimos.json', 'r') as arquivo:
            emprestimos = json.load(arquivo)
    except:
        emprestimos = {}

def salvar_dados():
    with open('biblioteca_usuarios.json', 'w') as arquivo:
        json.dump(usuarios, arquivo, indent=4)
    with open('biblioteca_livros.json', 'w') as arquivo:
        json.dump(livros, arquivo)
    with open('biblioteca_emprestimos.json', 'w') as arquivo:
        json.dump(emprestimos, arquivo)

def menu():
    print('-=' * 15)
    print('BIBLIOTECA MENU'.center(30))
    print('-=' * 15)
    print('''[1] - Ver livros disponíveis
[2] - Cadastrar novo livro
[3] - Cadastrar novo usuário
[4] - Realizar empréstimo
[5] - Devolver livro
[6] - Ver histórico de empréstimos
[7] - Sair''')
    print()

def opcao1(): # VISUALIZAÇÃO DOS LIVROS
    print('-=-=-=-=-=- LIVROS -=-=-=-=-=-')
    for i, livro in enumerate(livros.values()):
        print(f'[{i}] - {livro[0]} | STATUS: {livro[1]} ')

def opcao2(): # CADASTRO DE LIVROS
    print('-=-=-= CADASTRO DE LIVROS -=-=-=')
    while True:
        titulo_livro = input('Titulo do livro: ')
        if titulo_livro == '': 
            print('\033[31mErro! Digite um título válido.\033[m')
            continue
        else:
            while True:
                autor_livro = input('Autor do livro: ')
                if autor_livro == '':
                    print('\033[31mErro! Digite um autor válido.\033[m')
                    continue
                disponibilidade = 'DISPONÍVEL'
                livros[autor_livro] = titulo_livro, disponibilidade
                print('\033[32mLivro adicionado com sucesso!\033[m')
                salvar_dados()
                break
            break

def opcao3(): # CRIAÇÃO DE CONTAS
    print('-=-=-= CADASTRO DE USUÁRIO -=-=-=')
    while True:
        usuario = input('Nome de usuário: ').lower()
        if usuario == '':
            print('\033[31mErro! Digite um usuário válido.\033[m')
            continue

        if usuario in usuarios:
            print('\033[31mEsse usuário já existe!\033[m')
            continue
        else:
            while True:
                senha = input('Senha: ')
                if senha == '':
                    print('\033[31mErro! Digite uma senha segura.\033[m')
                    continue
                else:
                    usuarios[usuario] = {'senha' : senha}
                    print('\033[32mConta criada com sucesso!\033[m')
                    salvar_dados()
                    break
            break

def opcao4(): # REALIZAÇÃO DE EMPRÉSTIMOS
    print('-=-=-= EMPRÉSTIMO DE LIVROS -=-=-=')
    usuario_emprestimo = input('Usuario: ').lower()
    if usuario_emprestimo not in usuarios:
        print('\033[31mUsuário não encontrado!\033[m')
        return
    senha_emprestimo = input('Senha: ')
    if usuarios[usuario_emprestimo]['senha'] != senha_emprestimo:
        print('\033[31mSenha incorreta!\033[m')
        return

    livros_disponiveis = {}
    print('\nLivros Disponiveis:')
    i = 0
    for autor, dados_livro in livros.items():
        titulo, status = dados_livro
        if status == 'DISPONÍVEL':
            print(f'[{i}] - {titulo} | Autor: {autor}')
            livros_disponiveis[i] = autor
            i += 1
    try:
        escolha_indice = int(input('Qual o número [índice] do livro que deseja pegar emprestado?: '))
    except ValueError:
        print('\033[31mOpção inválida. Digite um número.\033[m')
        return
    
    if escolha_indice not in livros_disponiveis:
        print('\033[31mÍndice de livro inválido.\033[m')
        return
    
    autor_escolhido = livros_disponiveis[escolha_indice]
    titulo_escolhido, _ = livros[autor_escolhido]

    livros[autor_escolhido] = (titulo_escolhido, 'EMPRESTADO')
    if not livros_disponiveis:
        print('\033[33mNenhum livro disponível para empréstimo.\033[m')
        return

    if autor_escolhido not in emprestimos:
        emprestimos[autor_escolhido] = []

    emprestimos[autor_escolhido].append({
        'usuario' : usuario_emprestimo,
        'titulo' : titulo_escolhido,
        'status' : 'EMPRESTADO'
        
    })
    print(f'\033[32mLIVRO EMPRESTADO PARA "{usuario_emprestimo }" COM SUCESSO !\033[m')
    salvar_dados()

def opcao5(): # DEVOLUÇÃO DE LIVROS
    print('-=-=-= DEVOLUÇÃO DE LIVROS -=-=-=')
    usuario_emprestimo = input('Usuario: ')
    if usuario_emprestimo not in usuarios:
        print('\033[31mUsuário não encontrado!\033[m')
        return
    senha_emprestimo = input('Senha: ')
    if usuarios[usuario_emprestimo]['senha'] != senha_emprestimo:
        print('\033[31mSenha incorreta!\033[m')
        return
    
    livros_emprestados = {}
    print('\nLivros Emprestados: ')
    i = 0
    for autor, dados_livro in livros.items():
        titulo, status = dados_livro
        if status == 'EMPRESTADO':
            print(f'[{i}] - {titulo} | Autor {autor}')
            livros_emprestados[i] = autor
            i += 1
    devolver_livro = int(input('Qual livro você deseja devolver?: '))
    
    autor_escolhido = livros_emprestados[devolver_livro]
    titulo_escolhido, _ = livros[autor_escolhido]

    livros[autor_escolhido] = (titulo_escolhido, 'DISPONÍVEL')
    if autor_escolhido in emprestimos:
        emprestimos[autor_escolhido].append({
            'usuario': usuario_emprestimo,
            'titulo': titulo_escolhido,
            'status': 'DEVOLVIDO' # Status alterado para DEVOLVIDO no histórico
        })

    print(f'\033[32mLIVRO "{titulo_escolhido}" DEVOLVIDO COM SUCESSO!\033[m')
    salvar_dados()

def opcao6():
    print('-=-=-= HISTÓRICO DE EMPRÉSTIMOS -=-=-=')
    if not emprestimos:
        print('SEM REGISTROS DE EMPRÉSTIMOS')
    else:
        for autor, historico in emprestimos.items():
            print(f'\nAutor: {autor}')

            for registro in historico:
                print(f'Usuario: {registro['usuario']}\nLivro emprestado: {registro['titulo']}\nStatus: {registro['status']}')

carregar_dados()

# LOOP PRINCIPAl
while True:
    menu()
    try:
        op = int(input('Digite sua opção: '))
    except:
        print('\033[31mErro! Digite um número válido.\033[m')
        continue
    if op == 1:
        opcao1()
    elif op == 2:
        opcao2()
    elif op == 3:
        opcao3()
    elif op == 4:
        opcao4()
    elif op == 5:
        opcao5()
    elif op == 6:
        opcao6()
    elif op == 7:
            print('-' * 30)
            print('     SAINDO DO SISTEMA', end='', flush=True)
            for l in range(3):  
                sleep(0.5)  
                print('.', end='', flush=True)
            print(f'\n{'-' * 30}')
            break
    elif op > 7:
        print('\033[31mErro! Digite um número válido.\033[m')
        continue
    op2 = str(input('Digite "sair" para voltar ao menu: ')).lower()
    if op2 == 'sair':
        continue
