import random
import sys
import os
from datetime import datetime

# =========================================================
# FUNÇÕES
# =========================================================

def calcular_paridade_par(n):
    """Calcula o bit de paridade par."""
    return bin(n).count("1") % 2


def verificar_paridade(n, bit_paridade):
    """Verifica se o bit de paridade é válido."""
    return calcular_paridade_par(n) == bit_paridade


def gerar_numeros():
    """Gera entre 51 e 64 números aleatórios [0,127]."""
    random.seed(datetime.now().timestamp())
    k = random.randint(51, 64)
    return [random.randint(0, 127) for _ in range(k)]


def guardar_ficheiro(nome, lista):
    """Guarda lista num ficheiro."""
    with open(nome, "w") as f:
        for x in lista:
            f.write(str(x) + "\n")


def ler_ficheiro(nome):
    """Lê números de um ficheiro."""
    with open(nome, "r") as f:
        return [int(l.strip()) for l in f]


def alterar_um_bit(n):
    """Altera um único bit aleatório."""
    pos = random.randint(0, 6)
    return n ^ (1 << pos)


def ler_input_manual():
    """Lê números do utilizador."""
    entrada = input("Introduza números (0-127) separados por espaço: ")
    return [int(x) for x in entrada.split()]


def validar_numeros(lista):
    """Garante que os números estão entre 0 e 127."""
    validos = []
    for n in lista:
        if 0 <= n < 128:
            validos.append(n)
        else:
            print(f"Valor ignorado (fora do intervalo): {n}")
    return validos


def escolher_input():
    """Menu de escolha de input."""
    print("=== ESCOLHER MODO DE INPUT ===")
    print("1 - Gerar números aleatórios")
    print("2 - Introduzir números manualmente")
    print("3 - Ler números de ficheiro")

    opcao = input("Opção: ")

    if opcao == "1":
        return gerar_numeros()

    elif opcao == "2":
        return validar_numeros(ler_input_manual())

    elif opcao == "3":
        nome = input("Nome do ficheiro: ")
        return validar_numeros(ler_ficheiro(nome))

    else:
        print("Opção inválida!\n")
        return escolher_input()


# =========================================================
# PROGRAMA PRINCIPAL
# =========================================================

# Escolher origem dos dados
numeros = escolher_input()

# Guardar números originais
guardar_ficheiro("numeros.txt", numeros)

# Calcular paridades originais
paridades = [calcular_paridade_par(n) for n in numeros]
guardar_ficheiro("paridades.txt", paridades)

# Criar cópia e alterar alguns números
numeros_alterados = numeros.copy()

for i in range(len(numeros_alterados)):
    if random.random() < 0.3:  # altera ~30%
        numeros_alterados[i] = alterar_um_bit(numeros_alterados[i])

guardar_ficheiro("numeros_alterados.txt", numeros_alterados)

# Calcular novas paridades
paridades_novas = [calcular_paridade_par(n) for n in numeros_alterados]
guardar_ficheiro("paridades_novas.txt", paridades_novas)

# =========================================================
# VERIFICAÇÃO E DETEÇÃO DE ERROS
# =========================================================

erros = []

print("\n=== VERIFICAÇÃO DE PARIDADE ===\n")

for i in range(len(numeros)):
    if not verificar_paridade(numeros_alterados[i], paridades[i]):
        erros.append(i)

        print(f"[ERRO] Índice {i}:")
        print(f"  Original : {numeros[i]} ({bin(numeros[i])})")
        print(f"  Alterado : {numeros_alterados[i]} ({bin(numeros_alterados[i])})")
        print(f"  Paridade original: {paridades[i]}")
        print(f"  Paridade nova    : {paridades_novas[i]}\n")

# =========================================================
# RESULTADO FINAL
# =========================================================

print("===================================")
print(f"Total de números: {len(numeros)}")
print(f"Números com erro: {len(erros)}")
print(f"Índices com erro: {erros}")