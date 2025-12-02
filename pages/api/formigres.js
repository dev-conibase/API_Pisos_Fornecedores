const fs = require('fs');
const path = require('path');

// Data da última atualização
const customLastUpdated = "01/12/2025";

export default function handler(req, res) {
  const { produto } = req.query;
  const filePath = path.join(process.cwd(), 'data_formigres.json');

  try {
    const fileContent = fs.readFileSync(filePath, 'utf8');

    /**
     * @type {{codigo: string, produto: string, A: string, A2: string, B: string, dimensions?: string}[]}
     */
    const data = JSON.parse(fileContent);
    const produtoBuscado = decodeURIComponent(produto ?? "").trim().toLowerCase();

    // Busca EXATA por nome (produto) ou código
    const produtoEncontrado = data.find(p =>
      p.produto.toLowerCase() === produtoBuscado ||
      p.codigo === produtoBuscado
    );

    if (produtoEncontrado) {
      return res.status(200).json({
        ...produtoEncontrado,
        lastUpdated: customLastUpdated
      });
    } else {
      return res.status(404).json({
        error: `Produto não encontrado.`
      });
    }

  } catch (error) {
    console.error("Erro ao processar o arquivo JSON:", error);
    return res.status(500).json({
      error: 'Erro ao processar o arquivo JSON.'
    });
  }
};
