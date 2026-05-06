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

first = True
second = True

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
            print(high)
        
        if high == -1: #Foi definido por padrão como -1, se não for, achamos o maior número do intervalo
            if first_high_search:
                #O primeiro chute da busca binária será o número + 50
                first_high_search = False
                gap = 50
                print(number_from_search+gap)
                return [CHUTE_DE_NUMERO, number_from_search+gap]
            else:
                #Busca dos próximos chutes

                if last_not_right_guess == -1 or last_right_guess == -1:
                    gap //= 2
                
                if gap != 0:
                    if number_guesses[-1][2]:
                        last_right_guess = number_guesses[-1][0]
                        print(number_guesses[-1][0]+gap)
                        if last_not_right_guess != -1 and last_right_guess != -1:
                            gap = (last_not_right_guess - last_right_guess)//2
                        return [CHUTE_DE_NUMERO, number_guesses[-1][0]+gap]
                    else:
                        last_not_right_guess = number_guesses[-1][0]
                        print(number_guesses[-1][0]-gap)
                        if last_not_right_guess != -1 and last_right_guess != -1:
                            gap = (last_not_right_guess - last_right_guess)//2
                        return [CHUTE_DE_NUMERO, number_guesses[-1][0]-gap]
                
                else:
                    #Se a gap for igual a 0, o número ou vai ser o próprio número, ou o anterior
                    if number_guesses[-1][2]:
                        high = number_guesses[-1][0]
                    else:
                        high = number_guesses[-1][0]-1
                    print(high)
                    print(number_guesses[-1][0])
        
        if low == -1:
            if first_low_search:
                first_low_search = False
                gap = 100 - (high - number_from_search)
                return [CHUTE_DE_NUMERO, number_from_search-gap]
            else:
                if last_not_right_guess == -1 or last_right_guess == -1:
                    gap //= 2
                
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
                    print(low)
        
        global first, second
        if first:
            first = False
            return [CHUTE_DE_REGRA, ["int", low, high]]
        elif second:
            second = False
            return [CHUTE_DE_REGRA, ["int", low, high-2]]

        #return [CHUTE_DE_REGRA, ["int", low, high]]

    else:
        #Testar se não é o intervalo [n,n]
        global testar_intervalo_unico
        if testar_intervalo_unico:
            testar_intervalo_unico = False
            return [CHUTE_DE_REGRA, ["int", number_from_search, number_from_search]]
        