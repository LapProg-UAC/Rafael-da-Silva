import random
import csv
import json


def convert_txt_list(filename: str) -> list:
    """
    Lê um ficheiro .txt contendo medicamentos (um por linha)
    e devolve uma lista com os nomes já limpos de espaços e \n.
    """
    with open(filename, 'r', encoding='utf-8') as f:
        # strip() remove quebras de linha e espaços extra
        return [linha.strip() for linha in f.readlines()]


def generate_intercection_matriz(medicines: list) -> list:
    """
    Gera uma matriz quadrada simétrica com valores aleatórios entre 0 e 6.
    Cada valor representa o nível de interação entre dois medicamentos.

    0  -> sem interação
    6  -> interação muito grave
    """
    size = len(medicines)

    # Criação de uma matriz quadrada inicializada a 0
    matriz = [[0] * size for _ in range(size)]

    # Preenche apenas metade da matriz e copia para manter simetria
    for i in range(size):
        for j in range(i + 1, size):
            valor = random.randint(0, 6)
            matriz[i][j] = valor
            matriz[j][i] = valor  # garante simetria

    return matriz


def guardar_interacoes_json(filename: str, medicines: list, matriz: list) -> None:
    """
    Guarda os medicamentos e respetiva matriz de interações
    num ficheiro JSON.
    """
    dados = {
        "medicines": medicines,
        "matriz": matriz
    }

    with open(filename, "w", encoding="utf-8") as f:
        json.dump(dados, f, indent=4, ensure_ascii=False)


def gerar_pessoa() -> tuple:
    """
    Gera uma pessoa aleatória:
    - Nome completo (nome + apelido)
    - Número de Segurança Social (11 dígitos)

    Retorna um tuplo (imutável).
    """

    # Estruturas mutáveis (listas)
    nomes = ["Ana", "Bruno", "Carla", "Daniel", "Eva", "Fábio", "Gabriela"]
    apelidos = ["Silva", "Costa", "Mendes", "Oliveira", "Santos", "Ferreira"]

    # Escolha aleatória usando o módulo random
    nome = random.choice(nomes) + " " + random.choice(apelidos)

    # Geração de número aleatório de 11 dígitos
    nss = random.randint(10000000000, 99999999999)

    return (nome, nss)  # tuplo (estrutura imutável)


def guardar_pessoas_csv(filename: str, quantidade: int) -> None:
    """
    Gera 'quantidade' pessoas aleatórias e guarda num ficheiro CSV.
    O CSV terá duas colunas: nome e nss.
    """

    with open(filename, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)

        # Escrita do cabeçalho
        writer.writerow(["nome", "nss"])

        # Escrita das pessoas geradas aleatoriamente
        for _ in range(quantidade):
            writer.writerow(gerar_pessoa())


def ler_pessoas_csv(filename: str) -> list:
    """
    Lê o ficheiro CSV e devolve uma lista de tuplos (nome, nss).
    Utiliza csv.DictReader para aceder às colunas pelo nome.
    """
    pessoas = []

    with open(filename, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            pessoas.append((row["nome"], row["nss"]))

    return pessoas


def creat_prescription(medicines: list) -> list:
    """
    Cria uma prescrição médica aleatória com 1 a 5 medicamentos.
    Utiliza random.sample para evitar repetição de medicamentos.
    """
    nummedicine = random.randint(1, 5)
    return random.sample(medicines, nummedicine)


def danger_avaliation(prescription: list, medicines: list, matriz: list) -> tuple:
    """
    Analisa as interações entre os medicamentos da prescrição.

    Retorna:
    - valor máximo de perigo encontrado
    - lista com todas as interações (med1, med2, nível)
    """

    max_danger = 0
    interacoes = []

    # Percorre todas as combinações possíveis dentro da prescrição
    for i in range(len(prescription)):
        for j in range(i + 1, len(prescription)):

            # Encontra a posição real dos medicamentos na lista original
            idx1 = medicines.index(prescription[i])
            idx2 = medicines.index(prescription[j])

            valor = matriz[idx1][idx2]

            # Guarda apenas se existir interação (>0)
            if valor > 0:
                interacoes.append((prescription[i], prescription[j], valor))

            # Atualiza valor máximo
            if valor > max_danger:
                max_danger = valor

    return max_danger, interacoes


def interacoes_graves(interacoes: list) -> list:
    """
    Filtra apenas interações com nível >= 4.
    Usa função anónima (lambda) e função de ordem superior (filter).
    """
    return list(filter(lambda x: x[2] >= 4, interacoes))


def classificar_perigo(valor: int) -> str:
    """
    Classifica o nível máximo de perigo.
    """
    if valor == 0:
        return "Sem perigo"
    elif valor <= 2:
        return "Baixo"
    elif valor <= 4:
        return "Médio"
    else:
        return "Alto"


# ======================================================
# BLOCO PRINCIPAL
# ======================================================

if __name__ == "__main__":

    # 1 Ler medicamentos do ficheiro txt
    medicines = convert_txt_list("medicines.txt")

    # 2 Gerar matriz de interações aleatória
    matriz = generate_intercection_matriz(medicines)

    # 3 Guardar interações em ficheiro JSON
    guardar_interacoes_json("interacoes.json", medicines, matriz)

    # 4 Gerar ficheiro CSV com 5 pessoas aleatórias
    guardar_pessoas_csv("pessoas.csv", 5)

    # 5 Ler novamente o CSV
    pessoas = ler_pessoas_csv("pessoas.csv")

    # 6 Para cada pessoa, gerar prescrição e avaliar risco
    for nome, nss in pessoas:

        prescription = creat_prescription(medicines)

        perigo, interacoes = danger_avaliation(
            prescription, medicines, matriz
        )

        graves = interacoes_graves(interacoes)

        print("\n==============================")
        print(f"Nome: {nome}")
        print(f"NSS: {nss}")
        print("Prescrição:", prescription)

        if graves:
            print("Medicamentos que reagem (nível >= 4):")
            for m1, m2, val in graves:
                print(f"{m1} - {m2} -> Nível {val}")
        else:
            print("Sem interações graves.")

        print("Nível máximo de perigo:", perigo)
        print("Classificação:", classificar_perigo(perigo))