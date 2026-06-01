
# TRABALHO: Criptografia - Hashing por Folding


def folding_hash(texto, tamanho_hash=5):

    # Converter cada carácter do texto para o respetivo código ASCII
    ascii_vals = [ord(c) for c in texto]

    # Garantir que o número de elementos é múltiplo do tamanho do hash
    # Caso contrário, adiciona-se o valor do tamanho do hash
    while len(ascii_vals) % tamanho_hash != 0:
        ascii_vals.append(tamanho_hash)

    # Lista que vai guardar os blocos de números
    blocos = []

    # Criar blocos do tamanho definido
    for i in range(0, len(ascii_vals), tamanho_hash):

        # Guardar cada bloco
        blocos.append(ascii_vals[i:i+tamanho_hash])

    # Criar lista para armazenar a soma das colunas
    soma_colunas = [0] * tamanho_hash

    # Percorrer todos os blocos
    for bloco in blocos:

        # Somar os valores de cada coluna
        for i in range(tamanho_hash):
            soma_colunas[i] += bloco[i]

    # Aplicar módulo 256 a cada valor
    hash_vals = [valor % 256 for valor in soma_colunas]

    # Converter cada valor para hexadecimal
    hash_hex = [format(v, "02X") for v in hash_vals]

    # Devolver o hash
    return hash_hex


def verificar_integridade(texto, hash_original):

    # Calcular novamente o hash do texto
    novo_hash = folding_hash(texto)

    # Comparar os dois hashes
    if novo_hash == hash_original:

        # Se forem iguais, o texto não foi alterado
        return True

    else:

        # Caso contrário houve alteração
        return False



def keyed_hash(texto, chave, tamanho_hash=5):

    # Calcular primeiro o hash normal
    hash_base = folding_hash(texto, tamanho_hash)

    # Converter valores hexadecimais para inteiros
    hash_int = [int(h, 16) for h in hash_base]

    # Lista para guardar a assinatura final
    assinatura = []

    # Percorrer cada posição do hash
    for i in range(tamanho_hash):

        # Somar a chave e aplicar módulo 256
        valor = (hash_int[i] + chave[i]) % 256

        # Converter para hexadecimal
        assinatura.append(format(valor, "02X"))

    # Devolver a assinatura
    return assinatura



def verificar_autenticidade(texto, chave, assinatura_recebida):

    # Calcular nova assinatura
    nova_assinatura = keyed_hash(texto, chave)

    # Comparar assinaturas
    if nova_assinatura == assinatura_recebida:

        # Se forem iguais a autoria é válida
        return True

    else:

        # Caso contrário não é válida
        return False


def hash_ficheiro(nome_ficheiro):

    try:

        # Abrir ficheiro em modo leitura
        with open(nome_ficheiro, "r", encoding="utf-8") as f:

            # Ler todo o conteúdo do ficheiro
            conteudo = f.read()

        # Calcular o hash do conteúdo
        return folding_hash(conteudo)

    except:

        # Caso o ficheiro não exista
        print("Erro ao abrir o ficheiro.")
        return None



def menu():

    while True:

        print("\n---- MENU ----")
        print("1 - Calcular hash de texto")
        print("2 - Verificar integridade")
        print("3 - Criar keyed hash")
        print("4 - Verificar autenticidade")
        print("5 - Hash de ficheiro")
        print("0 - Sair")

        opcao = input("Escolha uma opção: ")

        if opcao == "1":

            texto = input("Introduza o texto: ")

            resultado = folding_hash(texto)

            print("Hash:", " ".join(resultado))


        elif opcao == "2":

            texto = input("Introduza o texto: ")

            hash_original = input("Introduza o hash original (separado por espaço): ").split()

            if verificar_integridade(texto, hash_original):

                print("Integridade verificada.")

            else:

                print("O texto foi alterado.")


        elif opcao == "3":

            texto = input("Introduza o texto: ")

            chave = input("Introduza a chave (5 números separados por espaço): ").split()

            chave = [int(x) for x in chave]

            assinatura = keyed_hash(texto, chave)

            print("Assinatura:", " ".join(assinatura))


        elif opcao == "4":

            texto = input("Introduza o texto: ")

            chave = input("Introduza a chave (5 números separados por espaço): ").split()

            chave = [int(x) for x in chave]

            assinatura = input("Introduza a assinatura: ").split()

            if verificar_autenticidade(texto, chave, assinatura):

                print("Autenticidade confirmada.")

            else:

                print("Autenticidade inválida.")


        elif opcao == "5":

            nome = input("Nome do ficheiro: ")

            resultado = hash_ficheiro(nome)

            if resultado:

                print("Hash:", " ".join(resultado))


        elif opcao == "0":

            print("Programa terminado.")
            break

        else:

            print("Opção inválida.")


menu()