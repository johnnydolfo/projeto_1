### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    João Rodolfo Berger Andrade
# RA #01 (quem entregou o código):      306480
# Nome #02:                             Felipe de Lucca
# RA #02:                               312860


# CONSTANTES DO JOGO

CHUTE_DE_NUMERO = "NUMBER"

CHUTE_DE_REGRA = "RULE"


# VARIÁVEIS GLOBAIS DE CONTROLE

# Indica se já encontramos algum número que satisfaz a regra
parar_busca = False

# Controle dos testes de vizinhança para detectar intervalos
testar_sucessor = True
testar_antecessor = False

# Controle do teste especial para intervalos unitários [n,n]
testar_intervalo_unico = True

# Flags auxiliares dos testes de antecessor/sucessor
antecessor_testado = False
antecessor_acabou_de_ser_testado = False
sucessor_acabou_de_ser_testado = False

# Controle das buscas binárias dos extremos do intervalo
first_high_search = True
first_low_search = True

# Limites do intervalo encontrados
high = -1
low = -1

# Últimos chutes corretos/incorretos utilizados na busca binária
last_right_guess = -1
last_not_right_guess = -1

# Indica se a regra parece ser um intervalo
muito_provavelmente_intervalo = False

# Controle da tentativa de identificar potências perfeitas
could_be_pot = True
pot = 1

# Controle da busca da regra modular
first_mod_search = True

# Variáveis auxiliares da busca modular
last_low_guess = -1
second_number = -1

# Controle das tentativas de chute da regra modular
firstattempt = True
secondattempt = True


def player(number_guesses, rule_guesses):

    # PRIMEIRO CHUTE
    
    # O primeiro chute do algoritmo será sempre 50.000,
    # posicionando a busca aproximadamente no centro do domínio.

    if number_guesses == []:
        return [CHUTE_DE_NUMERO, 50_000]
    
    # BUSCA DO PRIMEIRO NÚMERO VÁLIDO
    
    # Enquanto ainda não tivermos encontrado um número pertencente à regra,
    # o algoritmo realiza uma busca binária baseada nos feedbacks
    # "maior" e "menor".
    
    global parar_busca
    global gap

    if not number_guesses[-1][2] and not parar_busca:

        # Inicialização da busca binária

        if len(number_guesses) == 1:
            gap = 25_000
        else:
            # Redução progressiva da distância dos chutes
            gap//=2

        # Caso base da busca binária
        
        # Quando gap chega em 0, testamos diretamente o sucessor ou
        # antecessor imediato.

        if gap == 0:
            if number_guesses[-1][1] == 'menor':
                return [CHUTE_DE_NUMERO, number_guesses[-1][0]-1]
            else:
                return [CHUTE_DE_NUMERO, number_guesses[-1][0]+1]

        # Ajuste do chute baseado no feedback recebido

        if number_guesses[-1][1] == 'menor':

            # Garante que o chute permaneça dentro do domínio [1,100000]
            if number_guesses[-1][0]-gap >= 1:
                return [CHUTE_DE_NUMERO, number_guesses[-1][0]-gap]
            else:
                return [CHUTE_DE_NUMERO, 1]

        else:

            # Garante que o chute permaneça dentro do domínio [1,100000]
            if number_guesses[-1][0]+gap <= 100000:
                return [CHUTE_DE_NUMERO, number_guesses[-1][0]+gap]
            else:
                return [CHUTE_DE_NUMERO, 100000]
    
    # PRIMEIRO NÚMERO VÁLIDO ENCONTRADO
    
    # Armazenamos o primeiro número encontrado que satisfaz a regra.

    else:

        if not parar_busca:

            global number_from_search
            number_from_search = number_guesses[-1][0]

        parar_busca = True
    
    # DETECÇÃO DE INTERVALOS
    
    # O algoritmo testa o sucessor e o antecessor do primeiro número válido
    # encontrado. Se algum deles também satisfizer a regra, assumimos que
    # provavelmente estamos lidando com um intervalo.

    global muito_provavelmente_intervalo

    global testar_sucessor
    global sucessor_acabou_de_ser_testado
    global testar_antecessor

    # Teste do sucessor

    if testar_sucessor:

        testar_sucessor = False
        sucessor_acabou_de_ser_testado = True

        return [CHUTE_DE_NUMERO, number_from_search+1]
    
    # Resultado do teste do sucessor

    if sucessor_acabou_de_ser_testado and number_guesses[-1][2]:

        sucessor_acabou_de_ser_testado = False
        muito_provavelmente_intervalo = True

    elif sucessor_acabou_de_ser_testado and not number_guesses[-1][2]:

        sucessor_acabou_de_ser_testado = False
        testar_antecessor = True
    
    # TESTE DO ANTECESSOR

    global antecessor_testado
    global antecessor_acabou_de_ser_testado

    if not number_guesses[-1][2] and testar_antecessor:

        antecessor_testado = True
        antecessor_acabou_de_ser_testado = True
        testar_antecessor = False

        return [CHUTE_DE_NUMERO, number_from_search-1]
   
    # Resultado do teste do antecessor

    if antecessor_testado and number_guesses[-1][2] and antecessor_acabou_de_ser_testado:

        antecessor_acabou_de_ser_testado = False
        muito_provavelmente_intervalo = True
    
    elif antecessor_acabou_de_ser_testado and not number_guesses[-1][2]:

        antecessor_acabou_de_ser_testado = False
        muito_provavelmente_intervalo = False
    
    # BUSCA DOS LIMITES DO INTERVALO

    # Caso a regra pareça ser um intervalo, o algoritmo realiza duas buscas
    # binárias:
    
    # 1. Busca do limite superior (high)
    # 2. Busca do limite inferior (low)

    if muito_provavelmente_intervalo:

        global high
        global low

        global first_high_search
        global first_low_search

        global last_not_right_guess
        global last_right_guess

        # Caso especial:
        
        # Se o antecessor foi válido e o sucessor não, então o número da busca
        # já é o limite superior.

        if antecessor_testado:
            high = number_from_search
        
        # BUSCA DO LIMITE SUPERIOR

        if high == -1:

            if first_high_search:

                last_not_right_guess = number_from_search+101
                last_right_guess = number_from_search

                first_high_search = False

                gap = (last_not_right_guess - last_right_guess)//2

                if number_from_search+gap <= 100000:
                    return [CHUTE_DE_NUMERO, number_from_search+gap]
                else:
                    return [CHUTE_DE_NUMERO, 100000]
            
            else:

                # Continuação da busca binária

                if gap != 0:

                    if number_guesses[-1][2]:

                        last_right_guess = number_guesses[-1][0]

                        if last_not_right_guess != -1 and last_right_guess != -1:
                            gap = (last_not_right_guess - last_right_guess)//2

                        if number_guesses[-1][0]+gap <= 100000:
                            return [CHUTE_DE_NUMERO, number_guesses[-1][0]+gap]
                        else:
                            return [CHUTE_DE_NUMERO, 100000]

                    else:

                        last_not_right_guess = number_guesses[-1][0]

                        if last_not_right_guess != -1 and last_right_guess != -1:
                            gap = (last_not_right_guess - last_right_guess)//2

                        if number_guesses[-1][0]-gap >= 1:
                            return [CHUTE_DE_NUMERO, number_guesses[-1][0]-gap]
                        else:
                            return [CHUTE_DE_NUMERO, 1]
                
                else:

                    # Finalização da busca do high

                    if number_guesses[-1][2]:
                        high = number_guesses[-1][0]
                    else:
                        high = number_guesses[-1][0]-1
        
        # BUSCA DO LIMITE INFERIOR

        if low == -1:

            if first_low_search:

                last_not_right_guess = number_from_search-(100-(high-number_from_search))-1
                last_right_guess = number_from_search

                first_low_search = False

                gap = (last_right_guess - last_not_right_guess)//2

                if number_from_search-gap >= 1:
                    return [CHUTE_DE_NUMERO, number_from_search-gap]
                else:
                    return [CHUTE_DE_NUMERO, 1]

            else:
                
                if gap != 0:

                    if number_guesses[-1][2]:

                        last_right_guess = number_guesses[-1][0]

                        if last_not_right_guess != -1 and last_right_guess != -1:
                            gap = (last_right_guess - last_not_right_guess)//2

                        if number_guesses[-1][0]-gap >= 1:
                            return [CHUTE_DE_NUMERO, number_guesses[-1][0]-gap]
                        else:
                            return [CHUTE_DE_NUMERO, 1]

                    else:

                        last_not_right_guess = number_guesses[-1][0]

                        if last_not_right_guess != -1 and last_right_guess != -1:
                            gap = (last_right_guess - last_not_right_guess)//2

                        if number_guesses[-1][0]+gap <= 100000:
                            return [CHUTE_DE_NUMERO, number_guesses[-1][0]+gap]
                        else:
                            return [CHUTE_DE_NUMERO, 100000]

                else:

                    # Finalização da busca do low

                    if number_guesses[-1][2]:
                        low = number_guesses[-1][0]
                    else:
                        low = number_guesses[-1][0]+1
        
        # Chute final da regra de intervalo

        return [CHUTE_DE_REGRA, ["int", low, high]]

    # CASO NÃO SEJA INTERVALO

    else:

        # Teste especial para intervalos unitários [n,n]

        global testar_intervalo_unico

        if testar_intervalo_unico:

            testar_intervalo_unico = False

            return [CHUTE_DE_REGRA, ["int", number_from_search, number_from_search]]
        
        # TESTE DE POTÊNCIAS PERFEITAS

        global could_be_pot

        if could_be_pot:

            global pot

            while pot < 10:

                pot += 1

                raiz = round(number_from_search ** (1/pot))

                # Verifica se o número é uma potência perfeita de ordem pot

                if raiz ** pot == number_from_search:
                    return [CHUTE_DE_REGRA, ["pot", pot, 999]]
            
            could_be_pot = False
        
        # BUSCA DA REGRA MODULAR
        
        # Caso a regra não seja intervalo nem potência perfeita,
        # assumimos que ela é modular.
        
        # O algoritmo tenta encontrar um segundo número válido
        # para reconstruir o módulo.

        global first_mod_search
        global last_high_guess, last_low_guess
        global second_number
        global firstattempt, secondattempt
        global candidate
        
        # Inicialização da busca modular

        if first_mod_search:

            first_mod_search = False

            last_high_guess = number_from_search
            gap = 2

            if number_guesses[-1][0]-gap >= 1:
                return [CHUTE_DE_NUMERO, number_guesses[-1][0]-gap]
            else:
                return [CHUTE_DE_NUMERO, 1]

        # PROCURA DO SEGUNDO NÚMERO VÁLIDO

        elif second_number == -1:

            # Ainda não temos limite inferior

            if last_low_guess == -1:

                if number_guesses[-1][1] == 'menor' or number_guesses[-1][1] == "igual":

                    last_low_guess = number_guesses[-1][0]

                    gap = (last_high_guess-last_low_guess)/2

                    if number_guesses[-1][0]+gap <= 100000:
                        return [CHUTE_DE_NUMERO, number_guesses[-1][0]+gap]
                    else:
                        return [CHUTE_DE_NUMERO, 100000]

                elif number_guesses[-1][1] == 'maior':

                    last_high_guess = number_guesses[-1][0]

                    # Crescimento linear da distância dos chutes
                    gap += 1

                    if number_guesses[-1][0]-gap >= 1:
                        return [CHUTE_DE_NUMERO, number_guesses[-1][0]-gap]
                    else:
                        return [CHUTE_DE_NUMERO, 1]
                
            # Já temos limite inferior

            else:

                if number_guesses[-1][1] == 'menor' or number_guesses[-1][1] == "igual":

                    last_low_guess = number_guesses[-1][0]

                    gap = (last_high_guess-last_low_guess)/2

                    # Caso os limites sejam consecutivos

                    if last_high_guess-last_low_guess == 1:

                        second_number = 2*last_low_guess - number_from_search
                    
                    else:

                        if number_guesses[-1][0]+gap <= 100000:
                            return [CHUTE_DE_NUMERO, number_guesses[-1][0]+gap]
                        else:
                            return [CHUTE_DE_NUMERO, 100000]
                    
                elif number_guesses[-1][1] == 'maior':

                    last_high_guess = number_guesses[-1][0]

                    gap = (last_high_guess-last_low_guess)/2

                    if last_high_guess-last_low_guess == 1:

                        second_number = 2*last_low_guess - number_from_search

                    else:

                        if number_guesses[-1][0]-gap >= 1:
                            return [CHUTE_DE_NUMERO, number_guesses[-1][0]-gap]
                        else:
                            return [CHUTE_DE_NUMERO, 1]

        # CHUTES FINAIS DA REGRA MODULAR

        if firstattempt:

            firstattempt = False

            return [
                CHUTE_DE_REGRA,
                [
                    "mod",
                    number_from_search-second_number,
                    number_from_search%(number_from_search-second_number)
                ]
            ]

        elif secondattempt:

            secondattempt = False

            return [
                CHUTE_DE_REGRA,
                [
                    "mod",
                    number_from_search-second_number-1,
                    number_from_search%(number_from_search-second_number-1)
                ]
            ]