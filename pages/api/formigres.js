const fs = require('fs');
const path = require('path');
// Data da última atualização
const customLastUpdated = "24/07/2025";
export default function handler(req, res) {
  const { produto } = req.query;
  const filePath = path.join(process.cwd(), 'data_formigres.json');
  try {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));
    const produtoBuscado = decodeURIComponent(produto ?? "").trim();
    const produtoEncontrado = data.find(p =>
      p.produto.toLowerCase().includes(produtoBuscado.toLowerCase())
    );
    if (produtoEncontrado) {
      res.status(200).json({ ...produtoEncontrado, lastUpdated: customLastUpdated });
    } else {
      res.status(404).json({ error: `Produto "${produtoBuscado}" não encontrado.` });
    }
  } catch (error) {
    console.error("Erro ao processar o arquivo JSON:", error);
    res.status(500).json({ error: 'Erro ao processar o arquivo JSON.' });
  }
};
