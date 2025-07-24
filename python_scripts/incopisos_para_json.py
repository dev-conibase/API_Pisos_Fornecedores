import fitz
import json
import os
import re

# Caminho base (onde está o script)
base_dir = os.path.dirname(__file__)

# Caminho do PDF na pasta /pdfs/
pdf_path = os.path.join(base_dir, "pdfs", "Incopisos.pdf")

# Caminho do JSON de saída (na raiz do projeto)
output_file = os.path.join(base_dir, "..", "data_incopisos.json")

# Valida o arquivo
if not os.path.isfile(pdf_path):
    print("❌ Arquivo não encontrado.")
    exit()

# Abrir PDF
doc = fitz.open(pdf_path)

# Extrair tokens
raw_tokens = []
for page in doc:
    for line in page.get_text().splitlines():
        raw_tokens.extend(line.strip().split())

# Regex
dim_pattern = re.compile(r"^\d{2,3},\d{2}x\d{2,3},\d{2}$")
tipo_pattern = re.compile(r"^[A-Z]{2}$")
quant_pattern = re.compile(r"^\d{1,4}(?:\.\d{3})*,\d{2}$|^SIM$|^0,00$")
codigo_pattern = re.compile(r"^\d{3,}(?:\.\d{3})?$")

# Parsing
result = []
current_dimension = None
i = 0

while i < len(raw_tokens):
    token = raw_tokens[i]

    # Detecta dimensão (ex: 75,00x75,00)
    if dim_pattern.match(token):
        current_dimension = token
        i += 1
        continue

    # Verifica se há tokens suficientes para análise
    if i + 4 < len(raw_tokens):
        prefixo = raw_tokens[i]
        codigo = raw_tokens[i + 1]
        tipo = raw_tokens[i + 2]
        saldo = raw_tokens[i + 3]

        # Valida produto
        if prefixo.isalpha() and codigo_pattern.match(codigo) and tipo_pattern.match(tipo) and quant_pattern.match(saldo):
            produto = f"{prefixo} {codigo}"
            result.append({
                "dimensions": current_dimension,
                "produto": produto,
                "LD": tipo,
                "saldo": saldo,
                "previsao": ""
            })
            i += 4
        else:
            i += 1
    else:
        break

# Salvar JSON
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, ensure_ascii=False, indent=2)

print(f"\n✅ {len(result)} produtos extraídos com sucesso.")
print(f"📁 Arquivo salvo: {output_file}")
