const fs = require('fs');
const path = require('path');

const customLastUpdated = "20/05/2025";

export default function handler(req, res) {
  const { produto } = req.query;
  const filePath = path.join(process.cwd(), 'data_helena.json');

  try {
    const fileContent = fs.readFileSync(filePath, 'utf8');

    /**
     * @type {{Produto: string, Saldo: string, "Previsão": string}[]}
     */
    const data = JSON.parse(fileContent);

    const produtoBuscado = decodeURIComponent(produto ?? "");

    // Corrigido para buscar pela chave "Produto" com correspondência exata
    const encontrado = data.find(item => item.Produto === produtoBuscado);

    if (encontrado) {
      return res
        .status(200)
        .json({ ...encontrado, lastUpdated: customLastUpdated });
    } else {
      return res
        .status(404)
        .json({ error: `Produto "${produtoBuscado}" não encontrado.` });
    }
  } catch (error) {
    console.error("Erro na API /api/incopisos:", error);
    return res
      .status(500)
      .json({ error: 'Erro ao processar o arquivo JSON.' });
  }
};
