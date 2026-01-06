const fs = require('fs');
const path = require('path');

const customLastUpdated = "06/01/2026";

export default function handler(req, res) {
  const { produto } = req.query;
  const filePath = path.join(process.cwd(), 'data_helena.json'); // ou 'data_formigres.json', etc

  try {
    const fileContent = fs.readFileSync(filePath, 'utf8');

    /**
     * @type {{produto: string, saldo: string, dimensions: string}[]}
     */
    const data = JSON.parse(fileContent);

    const produtoBuscado = decodeURIComponent(produto ?? "");

    // Busca exata (case-sensitive)
    const encontrado = data.find(item => item.produto === produtoBuscado);

    if (encontrado) {
      return res
        .status(200)
        .json({ ...encontrado, lastUpdated: customLastUpdated });
    } else {
      return res
        .status(404)
        .json({ error: `Produto não encontrado.` });
    }
  } catch (error) {
    console.error("Erro na API:", error);
    return res
      .status(500)
      .json({ error: 'Erro ao processar o arquivo JSON.' });
  }
};
