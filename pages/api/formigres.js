const fs = require('fs');
const path = require('path');

// Defina a data customizada
const customLastUpdated = "09/06/2025";

export default function handler(req, res) {
  const { produto } = req.query;
  const filePath = path.join(process.cwd(), 'data_formigres.json');

  try {
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

    const produtoBuscado = decodeURIComponent(produto);

    const produtoEncontrado = data.estoque
      .flatMap(item => item.products)
      .find(p => p.produto === produtoBuscado);

    if (produtoEncontrado) {
      res.status(200).json({ ...produtoEncontrado, lastUpdated: customLastUpdated });
    } else {
      res.status(404).json({ error: `Produto ${produtoBuscado} não encontrado.` });
    }
  } catch (error) {
    res.status(500).json({ error: 'Erro ao processar o arquivo JSON.' });
  }
};
