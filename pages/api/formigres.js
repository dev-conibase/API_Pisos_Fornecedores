import fs from 'fs';
import path from 'path';

// Defina a data customizada
const customLastUpdated = "16/05/2025";

export default function handler(req, res) {
  const { produto } = req.query; // Obtém o parâmetro `produto` da query string
  const filePath = path.join(process.cwd(), 'data_formigres.json'); // Caminho para o arquivo JSON

  try {
    // Lê e faz o parse do JSON
    const data = JSON.parse(fs.readFileSync(filePath, 'utf8'));

    // Decodifica o valor da query string para lidar com espaços e caracteres especiais
    const produtoBuscado = decodeURIComponent(produto);

    // Busca o produto no JSON acessando a propriedade "estoque"
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
}
