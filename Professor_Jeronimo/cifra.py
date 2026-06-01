# ---------------------------------------------------------
# Programa de Encriptação e Desencriptação por Substituição
# ---------------------------------------------------------

# Função para encriptar uma string usando uma chave simples
def encriptar(texto, chave):
    """
    Encripta um texto deslocando o valor ASCII de cada carácter.
    """
    resultado = ""

    for c in texto:
        novo_char = chr(ord(c) + chave)
        resultado += novo_char

    return resultado


# Função para desencriptar uma string usando uma chave simples
def desencriptar(texto, chave):
    """
    Desencripta um texto subtraindo a chave ao valor ASCII.
    """
    resultado = ""

    for c in texto:
        novo_char = chr(ord(c) - chave)
        resultado += novo_char

    return resultado


# ---------------------------------------------------------
# Funções com chave múltipla
# ---------------------------------------------------------

def encriptar_multi(texto, chaves):
    """
    Encripta texto usando várias chaves aplicadas ciclicamente.
    """
    resultado = ""
    i = 0

    for c in texto:
        chave = chaves[i % len(chaves)]
        resultado += chr(ord(c) + chave)
        i += 1

    return resultado


def desencriptar_multi(texto, chaves):
    """
    Desencripta texto usando várias chaves aplicadas ciclicamente.
    """
    resultado = ""
    i = 0

    for c in texto:
        chave = chaves[i % len(chaves)]
        resultado += chr(ord(c) - chave)
        i += 1

    return resultado


# ---------------------------------------------------------
# Encriptação de ficheiros completos
# ---------------------------------------------------------

def encriptar_ficheiro(entrada, saida, chave):
    """
    Lê um ficheiro de texto, encripta o conteúdo e guarda num novo ficheiro.
    """

    with open(entrada, "r") as f:
        texto = f.read()

    texto_encriptado = encriptar(texto, chave)

    with open(saida, "w") as f:
        f.write(texto_encriptado)


def desencriptar_ficheiro(entrada, saida, chave):
    """
    Desencripta um ficheiro previamente encriptado.
    """

    with open(entrada, "r") as f:
        texto = f.read()

    texto_desencriptado = desencriptar(texto, chave)

    with open(saida, "w") as f:
        f.write(texto_desencriptado)


# ---------------------------------------------------------
# Encriptação de campos delimitados num ficheiro
# ---------------------------------------------------------

def encriptar_campo(ficheiro_entrada, ficheiro_saida, chave, indice_campo):
    """
    Encripta apenas um campo específico de cada linha de um ficheiro.
    Os campos são separados por ';'.
    """

    with open(ficheiro_entrada, "r") as f:
        linhas = f.readlines()

    with open(ficheiro_saida, "w") as f:

        for linha in linhas:

            campos = linha.strip().split(";")

            if indice_campo < len(campos):
                campos[indice_campo] = encriptar(campos[indice_campo], chave)

            nova_linha = ";".join(campos)

            f.write(nova_linha + "\n")


# ---------------------------------------------------------
# Função principal para testar o programa
# ---------------------------------------------------------

def main():

    texto = "zzz123456789"
    chave = 3

    print("Texto original:", texto)

    # Encriptação simples
    texto_encriptado = encriptar(texto, chave)
    print("Texto encriptado:", texto_encriptado)

    # Desencriptação
    texto_desencriptado = desencriptar(texto_encriptado, chave)
    print("Texto desencriptado:", texto_desencriptado)

    # Teste com chave múltipla
    chaves = [1, 2, 3]

    multi_encriptado = encriptar_multi(texto, chaves)
    print("Encriptado com múltiplas chaves:", multi_encriptado)

    multi_desencriptado = desencriptar_multi(multi_encriptado, chaves)
    print("Desencriptado com múltiplas chaves:", multi_desencriptado)


# Executar programa
main()