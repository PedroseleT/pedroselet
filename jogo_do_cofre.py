from random import sample

primeiro_digito = sample(['1', '2', '3', '4', '5', '6', '7', '8', '9'], 1)
restantes = sample([d for d in '0123456789' if d not in primeiro_digito], 3)
senha = primeiro_digito + restantes

tentativas = 0

print('=== JOGO DO COFRE ===')
print('Tente adivinhar um número de 4 dígitos, todos diferentes.')

while True:

    tentativas += 1
    chute_usuario = input(f'\nTentativa {tentativas}: ')

    # VALIDAÇÃO
    if len(chute_usuario) > 4 or not chute_usuario.isdigit():
        print('\033[31mDigite apenas 4 dígitos.\033[m')
        continue

    if len(set(chute_usuario)) != 4:
        print('\033[31mOs dígitos não podem se repetir.\033[m')
        continue

    chute_usuario = list(chute_usuario)


    # CONTAGEM POSIÇÃO CORRETA
    senha_restante = []
    chute_restante = []
    posicao_certa = []
    posicao_errada = []

    for i in range(4):
        if chute_usuario[i] == senha[i]:
            posicao_certa.append(chute_usuario[i])
        else:
            senha_restante.append(senha[i])
            chute_restante.append(chute_usuario[i])

    # CONTAGEM DE POSIÇÃO ERRADA
    for num in chute_restante:
        if num in senha_restante:
            posicao_errada.append(num)
            senha_restante.remove(num)  # evita contagem duplicada
    
    # EXIBIR RESULTADOS
    print(f'Números na posição certa {posicao_certa}')
    print(f'Números na posição errada {posicao_errada}')

    if len(posicao_certa) == 4:
        print(f'\n🎉 Parabéns! Você abriu o cofre {senha} em {tentativas} tentativas!')
        break