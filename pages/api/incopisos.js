const fs = require('fs');
const path = require('path');

const customLastUpdated = "28/01/2026";

export default function handler(req, res) {
  const { produto } = req.query;
  const filePath = path.join(process.cwd(), 'data_incopisos.json');

  try {
    const fileContent = fs.readFileSync(filePath, 'utf8');

    /**
     * @type {{produto: string, saldo: string, LD: string, dimensions: string, previsao: string}[]}
     */
    const data = JSON.parse(fileContent);
    const produtoBuscado = decodeURIComponent(produto ?? "").trim().toLowerCase();

    // Busca EXATA e case-insensitive
    const produtoEncontrado = data.find(p =>
      p.produto.toLowerCase() === produtoBuscado
    );

    if (produtoEncontrado) {
      return res
        .status(200)
        .json({ ...produtoEncontrado, lastUpdated: customLastUpdated });
    } else {
      return res
        .status(404)
        .json({ error: `Produto não encontrado.` });
    }

  } catch (error) {
    console.error("Erro ao processar o arquivo JSON:", error);
    res.status(500).json({ error: 'Erro ao processar o arquivo JSON.' });
  }
};
