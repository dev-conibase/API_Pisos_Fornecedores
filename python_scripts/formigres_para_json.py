import fitz
import json
import re
import os

# Caminho base (onde este script está localizado)
base_dir = os.path.dirname(os.path.abspath(__file__))

# Caminho do PDF
pdf_path = os.path.join(base_dir, "pdfs", "Formigres.pdf")

# Caminho do JSON de saída
output_file = os.path.join(base_dir, "..", "data_formigres.json")

def process_table_data(data_list):
    """
    Processa a lista de listas (tabela) e extrai os dados dos produtos.
    """
    result = []
    
    # Regex para identificar códigos e dimensões
    code_pattern = re.compile(r"^\d{3,}[-\s]?")
    dim_pattern = re.compile(r"(\d{2,3}[xX]\d{2,3})")

    for row in data_list:
        if not row or not row[0]: # Ignora linhas vazias
            continue
        
        # O cabeçalho da tabela é a primeira linha
        if "Produto" in row[0] and "Maior Lote" in row[1]:
            continue

        # Extrai os dados das colunas
        produto_full = row[0] if len(row) > 0 and row[0] else ""
        maior_lote_str = row[1] if len(row) > 1 and row[1] else "0,00"
        saldo_a_str = row[2] if len(row) > 2 and row[2] else "0,00"
        saldo_b_str = row[3] if len(row) > 3 and row[3] else "0,00"

        # Tenta encontrar o código do produto
        code_match = code_pattern.search(produto_full)
        codigo = code_match.group(0).strip(" -") if code_match else None
        
        # Ignora linhas que não têm um código de produto válido
        if not codigo:
            continue
        
        # Extrai o nome do produto e a dimensão
        produto_name = re.sub(code_pattern, "", produto_full).strip()
        dim_match = dim_pattern.search(produto_name)
        dimensions = dim_match.group(1).replace("X", "x") if dim_match else None
        
        item = {
            "codigo": codigo,
            "produto": produto_name,
            "dimensions": dimensions,
            "maior_lote": float(maior_lote_str.replace('.', '').replace(',', '.')),
            "saldo_A": float(saldo_a_str.replace('.', '').replace(',', '.')),
            "saldo_B": float(saldo_b_str.replace('.', '').replace(',', '.')),
        }
        result.append(item)

    return result

if not os.path.isfile(pdf_path):
    print(f"? Arquivo PDF não encontrado.")
    exit()

# Abrir PDF e extrair tabelas
try:
    doc = fitz.open(pdf_path)
    all_extracted_data = []

    for page_number in range(doc.page_count):
        page = doc[page_number]
        tables = page.find_tables()
        for table in tables:
            all_extracted_data.extend(table.extract())
    
    doc.close()
    
    result = process_table_data(all_extracted_data)

    if result:
        # Salvar em JSON
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2, ensure_ascii=False)
        print(f"\n? {len(result)} produtos extraídos com sucesso.")
        print(f"?? Arquivo salvo: {output_file}")
    else:
        print("? A extração de dados não foi realizada. Nenhum produto foi encontrado.")

except Exception as e:
    print(f"? Ocorreu um erro durante a extração: {e}")