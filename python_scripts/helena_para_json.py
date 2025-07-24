import fitz
import json
import re
import os

# Caminho base do script atual
base_dir = os.path.dirname(__file__)

# Caminho do PDF dentro da pasta /pdfs/
pdf_path = os.path.join(base_dir, "pdfs", "Helena.pdf")

# Caminho do JSON para salvar na raiz do projeto
output_file = os.path.join(base_dir, "..", "data_helena.json")

# Verifica se o PDF existe
if not os.path.isfile(pdf_path):
    print("❌ Arquivo não encontrado.")
    exit()

# Abrir o PDF
doc = fitz.open(pdf_path)

# Extrair tokens
raw_tokens = []
for page in doc:
    for line in page.get_text().splitlines():
        raw_tokens.extend(line.strip().split())

# Regex
codigo_pattern = re.compile(r"^[A-Z]{2,4}\d{6}$")
quant_pattern = re.compile(r"^Sim$|^Não$|^\d{1,4}(?:\.\d{3})*,\d{2}$")

# Palavras que indicam cabeçalho e devem ser ignoradas
cabecalhos = {"Produto", "Saldo", "Previsão"}
previsao_keywords = ["Previsão", "Lançamento", "Fora", "linha"]

# Variáveis
result = []
current_dimension = None
i = 0

while i < len(raw_tokens):
    token = raw_tokens[i]

    # Ignorar tokens de cabeçalho
    if token in cabecalhos and all(t in cabecalhos for t in raw_tokens[i:i+3]):
        i += 3
        continue

    # Detectar nova dimensão: ex: "120 x 120"
    if i + 2 < len(raw_tokens) and raw_tokens[i+1] == "x":
        current_dimension = raw_tokens[i] + "x" + raw_tokens[i+2]
        i += 3
        continue

    previsao = ""
    if token in previsao_keywords:
        previsao = token
        i += 1
        if i < len(raw_tokens) and raw_tokens[i] == "de":
            previsao += " de"
            i += 1
            if i < len(raw_tokens) and raw_tokens[i] == "linha":
                previsao += " linha"
                i += 1

    nome = []
    saldo = None

    for nome_size in range(1, 5):
        if i + nome_size + 1 < len(raw_tokens):
            codigo = raw_tokens[i + nome_size]
            qtd = raw_tokens[i + nome_size + 1]

            if codigo_pattern.match(codigo) and quant_pattern.match(qtd):
                nome = raw_tokens[i:i + nome_size + 1]
                saldo = qtd
                i += nome_size + 2
                break

    if nome and saldo:
        if all(p in cabecalhos for p in nome):  # ignora se for "Produto Saldo Previsão"
            continue

        item = {
            "dimensions": current_dimension,
            "produto": " ".join(nome),
            "saldo": saldo
        }
        if previsao:
            item["previsao"] = previsao
        result.append(item)
    else:
        i += 1

# Salvar JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n✅ {len(result)} produtos extraídos com sucesso.")
print(f"📁 Arquivo salvo: {output_file}")
