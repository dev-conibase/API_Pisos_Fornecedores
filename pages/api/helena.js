const fs = require('fs');
const path = require('path');
const customLastUpdated = "24/07/2025";
export default function handler(req, res) {
  const { produto } = req.query;
  const filePath = path.join(process.cwd(), 'data_incopisos.json');
  try {
    const fileContent = fs.readFileSync(filePath, 'utf8');
    /**
     * @type {{produto: string, saldo: string, LD: string, dimensions: string, previsao: string}[]}
     */
    const data = JSON.parse(fileContent);
    const produtoBuscado = decodeURIComponent(produto ?? "").trim();
    // Busca parcial, case-insensitive e segura
    const encontrado = data.find(item =>
      item.produto.toLowerCase().includes(produtoBuscado.toLowerCase())
    );
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
