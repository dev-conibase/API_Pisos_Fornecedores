import fitz  # PyMuPDF
import json
import os
import re

# Caminho base (onde este script está localizado)
base_dir = os.path.dirname(__file__)

# Caminho do PDF
pdf_path = os.path.join(base_dir, "pdfs", "Formigres.pdf")

# Caminho do JSON de saída
output_file = os.path.join(base_dir, "data_formigres.json")

# Valida se o arquivo existe
if not os.path.isfile(pdf_path):
    print("❌ Arquivo PDF não encontrado.")
    exit()

# Abrir PDF
doc = fitz.open(pdf_path)

# Extrair todas as linhas do PDF
lines = []
for page in doc:
    lines.extend(page.get_text().splitlines())

# Variáveis de controle
result = []
codigo_pattern = re.compile(r"^\d{4,6}$")
quantidade_pattern = re.compile(r"^\d{1,3}(?:\.\d{3})*,\d{2}$")

i = 0
while i < len(lines):
    linha = lines[i].strip()

    # Verifica se a linha atual é um código de produto
    if codigo_pattern.match(linha) and i + 4 < len(lines):
        codigo = linha
        produto = lines[i + 1].strip()
        q1 = lines[i + 2].strip()
        q2 = lines[i + 3].strip()
        q3 = lines[i + 4].strip()

        if all(quantidade_pattern.match(q) for q in [q1, q2, q3]):
            item = {
                "codigo": codigo,
                "produto": produto,
                "A": q1,
                "A2": q2,
                "B": q3
            }

            # Tenta detectar dimensão dentro do nome
            match = re.search(r"\d{2,3}[xX]\d{2,3}", produto)
            if match:
                item["dimensions"] = match.group().replace("X", "x")

            result.append(item)
            i += 5
        else:
            i += 1  # Caso falhe nos padrões de quantidade
    else:
        i += 1

# Salvar em JSON
output_file = os.path.join(base_dir, "..", "data_formigres.json")
with open(output_file, "w", encoding="utf-8") as f:
    json.dump(result, f, indent=2, ensure_ascii=False)

print(f"\n✅ {len(result)} produtos extraídos com sucesso.")
print(f"📁 Arquivo salvo: {output_file}")
