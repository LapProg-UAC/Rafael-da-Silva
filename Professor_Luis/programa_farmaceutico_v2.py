# 1. Importação dos módulos necessários (Objetivo 2)
import openpyxl
import random
import sys

# 2. Criação da primeira função: extrair dados do ficheiro de texto (Objetivo 1)
def read_names(filename: str) -> list:
    # Tratamento de exceções caso o ficheiro não exista (Objetivo 3)
    try:
        lista_limpa: list = [] # 1. Começamos com uma lista vazia
        
        with open(filename, 'r', encoding='utf-8') as f:
            for line in f: # 2. Lemos o ficheiro linha a linha
                
                # 3. Limpamos o lixo e os espaços invisíveis
                texto_limpo = line.replace("", "").strip()
                
                # 4. Se a linha não estiver vazia, guardamos na lista
                if texto_limpo != "":
                    lista_limpa.append(texto_limpo)
                    
        return lista_limpa # 5. Entregamos a lista final pronta a usar
        
    except Exception as e:
        print(f"Error reading file: {e}")
        sys.exit(1)
# 3. Criação da segunda função: gerar matriz de interações (Objetivo 4 e 6)
# Usa estruturas mutáveis (dict) e imutáveis (tuplos) com tipificação
def gen_matrix(meds: list) -> dict:
    matriz: dict = {} # 1. Criamos um dicionário vazio (estrutura mutável)
    
    # 2. Pegamos no medicamento da LINHA
    for x in meds:
        
        # 3. Cruzamos com o medicamento da COLUNA
        for y in meds:
            
            # 4. Verificamos se é o mesmo medicamento
            if x == y:
                matriz[(x, y)] = 0 # O efeito sobre ele próprio é 0
            else:
                matriz[(x, y)] = random.randint(1, 6) # O efeito cruzado é aleatório (1 a 6)
                
    return matriz # 5. Entregamos a matriz preenchida
# 4. Criação da terceira função: exportar dados para Excel (Objetivo 1)
def export_excel(matrix: dict, meds: list, filename: str) -> None:
    try:
        wb = openpyxl.Workbook()
        ws = wb.active
        
        header_row: list = [""] 
        
        # Adicionamos todos os nomes dos medicamentos a esta linha
        for med in meds:
            header_row.append(med)
            
        ws.append(header_row) 
        
        # ---  As Linhas de Dados  ---
        for row_med in meds:
            
            
            new_row: list = [row_med]
            
            
            for col_med in meds:
                effect = matrix[(row_med, col_med)]
                new_row.append(effect)
                
            ws.append(new_row) 
            
        # Guarda o ficheiro no disco
        wb.save(filename)
        
        
    except Exception as e:
        print(f"Erro ao guardar o Excel: {e}")
        sys.exit(1)

# 5. Função principal: estruturação por decomposição funcional (Objetivo 5)
def main() -> None:
    meds: list = read_meds('medicamentos.txt')
    matrix: dict = gen_matrix(meds)
    export_excel(matrix, meds, 'Interacoes_medicamentosas.xlsx')

# Executa o código
if __name__ == "__main__":
    main()