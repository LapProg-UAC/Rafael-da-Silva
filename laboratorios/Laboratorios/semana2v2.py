"""Módulo de Geração de Receitas Médicas
-------------------------------------
Gera prescrições médicas sintéticas, lendo medicamentos e interações 
de um ficheiro CSV, e exportando os resultados para JSON."""

import random
import json
import csv

# 1. Estruturas de dados (Dicionário com Listas - Cumpre o Objetivo 2)
NAMES_POOL: dict = {
    "first_names": ["Ana", "João", "Maria", "Rui", "Catarina", "Pedro", "Marta", "Tiago", "Sofia", "Nuno", "Inês", "Miguel", "Beatriz", "Diogo", "Joana", "Bruno", "Diana", "Hugo", "Leonor", "Carlos"],
    "last_names": ["Silva", "Santos", "Ferreira", "Pereira", "Oliveira", "Costa", "Rodrigues", "Martins", "Jesus", "Sousa", "Fernandes", "Gomes", "Marques", "Almeida", "Ribeiro", "Pinto", "Carvalho", "Teixeira", "Moreira", "Correia"]
}

# 2. Dicionário de tradução dos critérios
INTERACTION_MAP: dict = {
    1: "Sem significado clínico",
    2: "Potencialmente grave",
    3: "Potenciador do efeito terapêutico/tóxico dos medicamentos da coluna horizontal",
    4: "Potenciador do efeito terapêutico/tóxico dos medicamentos da coluna vertical",
    5: "Diminuidor do efeito terapêutico/tóxico dos medicamentos da coluna horizontal",
    6: "Diminuidor do efeito terapêutico/tóxico dos medicamentos da coluna vertical"
}

def read_csv_data(filename: str) -> tuple:
    """Leitura Robusta de Dados do CSV
    -------------------------------
    Abre o ficheiro CSV, deteta o delimitador automaticamente e extrai 
    os medicamentos e a matriz de interações. Devolve (lista_meds, matriz)."""
    
    try:
        meds_list: list = []
        interaction_matrix: dict = {}
        
        # Abre o ficheiro e lê o texto. Se não existir, salta logo para o except!
        with open(filename, mode='r', encoding='utf-8-sig') as f:
            conteudo = f.read().strip()
            
        if not conteudo:
            return [], {}
            
        linhas_texto = conteudo.split('\n')
        
        # Deteta automaticamente se o Excel separou com ';' ou ','
        separador = ';' if ';' in linhas_texto[0] else ','
        
        # Usa o csv.reader com o separador correto
        reader = csv.reader(linhas_texto, delimiter=separador)
        linhas_csv = list(reader)
        
        if not linhas_csv:
            return [], {}
            
        # Extrai os cabeçalhos (linha 0, ignorando a primeira coluna vazia)
        cabecalho = linhas_csv[0]
        for celula in cabecalho[1:]:
            med = celula.strip()
            if med:
                meds_list.append(med)
                
        # Extrai a matriz cruzada (restantes linhas)
        for linha in linhas_csv[1:]:
            if not linha or not linha[0].strip():
                continue
                
            med_linha = linha[0].strip()
            for i, valor in enumerate(linha[1:]):
                if i + 1 < len(cabecalho):
                    med_coluna = cabecalho[i+1].strip()
                    if valor.strip().isdigit():
                        interaction_matrix[(med_linha, med_coluna)] = int(valor.strip())
                        
        return meds_list, interaction_matrix

    except FileNotFoundError:
        print(f"❌ Erro: O ficheiro '{filename}' não foi encontrado na pasta atual.")
        return [], {}
    except Exception as e:
        print(f"❌ Erro crítico ao processar o CSV: {e}")
        return [], {}

def generate_prescriptions(num_records: int, meds_list: list, matrix: dict) -> list:
    """Geração de Receitas Médicas
    ---------------------------
    Gera um número de utente único (9 dígitos), um nome e 3 medicamentos.
    Avalia as interações através de um ciclo for clássico.
    Devolve a lista de dicionários com os utentes."""
    patients_list: list = []
    used_sns: set = set() 
    
    for _ in range(num_records):
        # 1. Garante SNS único
        patient_sns = random.randint(100000000, 999999999)
        while patient_sns in used_sns:
            patient_sns = random.randint(100000000, 999999999)
        used_sns.add(patient_sns)
        
        # 2. Gera o nome
        first = random.choice(NAMES_POOL["first_names"])
        last = random.choice(NAMES_POOL["last_names"])
        full_name = f"{first} {last}"
        
        # 3. Sorteia 3 medicamentos
        patient_meds = random.sample(meds_list, 3)
        pairs = [
            (patient_meds[0], patient_meds[1]), 
            (patient_meds[0], patient_meds[2]), 
            (patient_meds[1], patient_meds[2])
        ]
        
        # 4. Avalia interações com ciclo FOR (sem funções anónimas)
        interactions_found: list = []
        for pair in pairs:
            effect_grade = matrix.get(pair, matrix.get((pair[1], pair[0]), 1))
            effect_text = INTERACTION_MAP.get(effect_grade, "Desconhecido")
            interactions_found.append(f"{pair[0]} cruzado com {pair[1]} -> Efeito {effect_grade}: {effect_text}")
        
        # 5. Guarda no dicionário
        patient_data: dict = {
            "ID": patient_sns,
            "nome": full_name,
            "medicamentos_receitados": patient_meds,
            "interacoes_detetadas": interactions_found
        }
        patients_list.append(patient_data)
        
    return patients_list

def export_to_json(data: list, filename: str) -> None:
    """Exportação para JSON
    --------------------
    Converte a lista de dicionários num ficheiro JSON estruturado."""
    try:
        with open(filename, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        print(f"✅ SUCESSO! Ficheiro '{filename}' gerado sem erros.")
    except Exception as e:
        print(f"❌ Erro ao criar ficheiro JSON: {e}")

def main() -> None:
    """Orquestrador Principal
    ----------------------
    Executa a decomposição funcional do programa."""
    nome_csv = 'Interacoes_medicamentosas.csv' 
    
    print("1️⃣ A iniciar leitura do CSV...")
    meds, matrix = read_csv_data(nome_csv)
    
    if len(meds) < 3:
        print(f"⚠️ Paragem de Segurança: Encontrei {len(meds)} medicamentos. Precisamos de pelo menos 3!")
        print("-> Verifica se guardaste bem o Excel como 'CSV UTF-8 (Delimitado por vírgulas)'.")
        return 
        
    print(f"✅ Excelentes notícias: Encontrei {len(meds)} medicamentos no teu ficheiro!")
    
    print("2️⃣ A gerar receitas médicas...")
    prescriptions = generate_prescriptions(20, meds, matrix)
    
    print("3️⃣ A exportar os dados...")
    export_to_json(prescriptions, 'receitas_medicas.json')

if __name__ == "__main__":
    main()