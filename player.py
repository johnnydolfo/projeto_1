### TODO: PREENCHA SUAS INFORMAÇÕES AQUI ###
# Nome #01 (quem entregou o código):    João Rodolfo Berger Andrade
# RA #01 (quem entregou o código):      306480
# Nome #02:                             Felipe de Lucca
# RA #02:                               312860


CHUTE_DE_NUMERO = "NUMBER"
CHUTE_DE_REGRA = "RULE"
parar_busca = False
testar_sucessor = True
testar_antecessor = False
testar_intervalo_unico = True
antecessor_testado = False
antecessor_acabou_de_ser_testado = False
sucessor_acabou_de_ser_testado = False
first_high_search = True
first_low_search = True
high = -1
low = -1
last_right_guess = -1
last_not_right_guess = -1
muito_provavelmente_intervalo = False
could_be_pot = True
pot = 1
first_mod_search = True
last_low_guess = -1
second_number = -1
firstattempt = True
secondattempt = True

def player(number_guesses, rule_guesses):
    #O primeiro chute do programa será 50_000
    if number_guesses == []:
        return [CHUTE_DE_NUMERO, 50_000]
    
    #O programa irá chegar se o chute não está contido na regra...
    global parar_busca

    global gap

    if not number_guesses[-1][2] and not parar_busca:
        #...e se não estiver, irá definir um intervalo para fazer uma busca binária

        if len(number_guesses) == 1:
            gap = 25_000
        else:
            #Divide o intervalo em dois
            gap//=2

        #Se a gap for zero, o número ou será o sucessor ou o antecessor do último chute
        if gap == 0:
            if number_guesses[-1][1] == 'menor':
                return [CHUTE_DE_NUMERO, number_guesses[-1][0]-1]
            else:
                return [CHUTE_DE_NUMERO, number_guesses[-1][0]+1]

        if number_guesses[-1][1] == 'menor':
            return [CHUTE_DE_NUMERO, number_guesses[-1][0]-gap]
        else:
            return [CHUTE_DE_NUMERO, number_guesses[-1][0]+gap]
    
    #Aqui, a busca binária foi feita e encontramos o primeiro elemento que satisfaz a regra
    else:
        if not parar_busca:
            global number_from_search
            number_from_search = number_guesses[-1][0]
        parar_busca = True
    
    #Vamos checar se a regra é de intervalos testando o sucessor do nosso primeiro elemento
    global muito_provavelmente_intervalo

    global testar_sucessor
    global sucessor_acabou_de_ser_testado
    global testar_antecessor

    if testar_sucessor:
        testar_sucessor = False
        sucessor_acabou_de_ser_testado = True
        return [CHUTE_DE_NUMERO, number_from_search+1]
    
    if sucessor_acabou_de_ser_testado and number_guesses[-1][2]:
        sucessor_acabou_de_ser_testado = False
        muito_provavelmente_intervalo = True
    elif sucessor_acabou_de_ser_testado and not number_guesses[-1][2]:
        sucessor_acabou_de_ser_testado = False
        testar_antecessor = True
    
    #Para não correr o risco de assumir que a regra não é intervalo e o número for o último do intervalo, testaremos o antecessor
    global antecessor_testado
    global antecessor_acabou_de_ser_testado

    if not number_guesses[-1][2] and testar_antecessor:
        antecessor_testado = True
        antecessor_acabou_de_ser_testado = True
        testar_antecessor = False
        return [CHUTE_DE_NUMERO, number_from_search-1]
   
    if antecessor_testado and number_guesses[-1][2] and antecessor_acabou_de_ser_testado:
        antecessor_acabou_de_ser_testado = False
        muito_provavelmente_intervalo = True
    
    elif antecessor_acabou_de_ser_testado and not number_guesses[-1][2]:
        antecessor_acabou_de_ser_testado = False
        muito_provavelmente_intervalo = False
    
    #Se o sucessor ou antecessor são parte também da regra, muito provavelmente é um intervalo (a não ser resto 0 mod 1)
    if muito_provavelmente_intervalo:
        global high
        global low
        global first_high_search
        global first_low_search
        global last_not_right_guess
        global last_right_guess

        #Note que se o antecessor foi testado, o sucessor não era parte e, assim, o último elemento do intervalo é o próprio número da busca binária
        if antecessor_testado:
            high = number_from_search
        
        if high == -1: #Foi definido por padrão como -1, se não for, achamos o maior número do intervalo
            if first_high_search:
                last_not_right_guess = number_from_search+101
                last_right_guess = number_from_search
                first_high_search = False
                gap = (last_not_right_guess - last_right_guess)//2
                return [CHUTE_DE_NUMERO, number_from_search+gap]
            
            else:
                #Busca dos próximos chutes
                if gap != 0:
                    if number_guesses[-1][2]:
                        last_right_guess = number_guesses[-1][0]
                        if last_not_right_guess != -1 and last_right_guess != -1:
                            gap = (last_not_right_guess - last_right_guess)//2
                        return [CHUTE_DE_NUMERO, number_guesses[-1][0]+gap]
                    else:
                        last_not_right_guess = number_guesses[-1][0]
                        if last_not_right_guess != -1 and last_right_guess != -1:
                            gap = (last_not_right_guess - last_right_guess)//2
                        return [CHUTE_DE_NUMERO, number_guesses[-1][0]-gap]
                
                else:
                    #Se a gap for igual a 0, o número ou vai ser o próprio número, ou o anterior
                    if number_guesses[-1][2]:
                        high = number_guesses[-1][0]
                    else:
                        high = number_guesses[-1][0]-1
        
        if low == -1:
            if first_low_search:
                last_not_right_guess = number_from_search-(100-(high-number_from_search))-1
                last_right_guess = number_from_search
                first_low_search = False
                gap = (last_right_guess - last_not_right_guess)//2
                return [CHUTE_DE_NUMERO, number_from_search-gap]
            else:
                
                if gap != 0:
                    if number_guesses[-1][2]:
                        last_right_guess = number_guesses[-1][0]
                        if last_not_right_guess != -1 and last_right_guess != -1:
                            gap = (last_right_guess - last_not_right_guess)//2
                        return [CHUTE_DE_NUMERO, number_guesses[-1][0]-gap]
                    else:
                        last_not_right_guess = number_guesses[-1][0]
                        if last_not_right_guess != -1 and last_right_guess != -1:
                            gap = (last_right_guess - last_not_right_guess)//2
                        return [CHUTE_DE_NUMERO, number_guesses[-1][0]+gap]
                else:
                    #Se a gap for igual a 0, o número ou vai ser o próprio número, ou o próximo
                    if number_guesses[-1][2]:
                        low = number_guesses[-1][0]
                    else:
                        low = number_guesses[-1][0]+1
        
        return [CHUTE_DE_REGRA, ["int", low, high]]

    else: #Aqui, não é intervalos
        #Testar se não é o intervalo [n,n]
        global testar_intervalo_unico
        if testar_intervalo_unico:
            testar_intervalo_unico = False
            return [CHUTE_DE_REGRA, ["int", number_from_search, number_from_search]]
        
        global could_be_pot
        if could_be_pot:
            global pot
            while pot < 10: #note que não é <= pq o incremento vem antes
                pot += 1

                raiz = round(number_from_search ** (1/pot))

                if raiz ** pot == number_from_search:
                    return [CHUTE_DE_REGRA, ["pot", pot, 999]]
            
            could_be_pot = False
        
        #se não é intervalo, nem potência, então é módulo
        #acharemos o próximo número com a mesma propriedade
        global first_mod_search
        global last_high_guess, last_low_guess
        global second_number
        global firstattempt, secondattempt
        global candidate
        
        if first_mod_search:
            first_mod_search = False
            last_high_guess = number_from_search
            gap = 2
            return [CHUTE_DE_NUMERO, number_from_search-gap]

        elif second_number == -1:
            if last_low_guess == -1:
                if number_guesses[-1][1] == 'menor':
                    last_low_guess = number_guesses[-1][0]
                    gap = (last_high_guess-last_low_guess)/2
                    return [CHUTE_DE_NUMERO, number_guesses[-1][0]+gap]
                elif number_guesses[-1][1] == 'maior':
                    last_high_guess = number_guesses[-1][0]
                    gap *= 2
                    return [CHUTE_DE_NUMERO, number_guesses[-1][0]-gap]
                else:
                    second_number = number_guesses[-1][0]
                    firstattempt = False
                    return [CHUTE_DE_REGRA, ["mod", number_from_search-second_number, number_from_search%(number_from_search-second_number)]]
                
            else:
                if number_guesses[-1][1] == 'menor':
                    last_low_guess = number_guesses[-1][0]
                    gap = (last_high_guess-last_low_guess)/2

                    if last_high_guess-last_low_guess == 1:
                        second_number = 2*last_low_guess - number_from_search
                    
                    else:
                        return [CHUTE_DE_NUMERO, number_guesses[-1][0]+gap]
                    
                elif number_guesses[-1][1] == 'maior':
                    last_high_guess = number_guesses[-1][0]
                    gap = (last_high_guess-last_low_guess)/2

                    if last_high_guess-last_low_guess == 1:
                        second_number = 2*last_low_guess - number_from_search

                    else:
                        return [CHUTE_DE_NUMERO, number_guesses[-1][0]-gap]

        print("found")
        if firstattempt:
            firstattempt = False
            print(number_from_search, second_number)
            return [CHUTE_DE_REGRA, ["mod", number_from_search-second_number, number_from_search%(number_from_search-second_number)]]
        elif secondattempt:
            secondattempt = False
            print(number_from_search, second_number)
            return [CHUTE_DE_REGRA, ["mod", number_from_search-second_number-1, number_from_search%(number_from_search-second_number-1)]]