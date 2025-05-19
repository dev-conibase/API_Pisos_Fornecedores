const fs = require('fs');
const path = require('path');

const customLastUpdated = "19/05/2025";

module.exports = function handler(req, res) {
  const { produto } = req.query;
  const filePath = path.join(process.cwd(), 'data_incopisos.json');

  try {
    const fileContent = fs.readFileSync(filePath, 'utf8');

    /**
     * @type {{Produto: string, Saldo: string, "Previsão": string}[]}
     */
    const data = JSON.parse(fileContent);

    const produtoBuscado = decodeURIComponent(produto ?? "");
    const encontrado = data.find(item => item.Produto === produtoBuscado);

    if (encontrado) {
      return res
        .status(200)
        .json({ ...encontrado, lastUpdated: customLastUpdated });
    } else {
      return res
        .status(404)
        .json({ error: `Produto ${produtoBuscado} não encontrado.` });
    }
  } catch (error) {
    console.error(error);
    return res
      .status(500)
      .json({ error: 'Erro ao processar o arquivo JSON.' });
  }
};
