@echo off
echo.
echo 🟡 Executando scripts Python...

python python_scripts\formigres_para_json.py
python python_scripts\incopisos_para_json.py
python python_scripts\helena_para_json.py

echo.
echo 🟢 Adicionando todas as alterações ao Git...
git add .

echo.
git commit -m "Atualização automática dos arquivos JSON e demais alterações"

echo.
git push

echo.
echo ✅ Push concluído com sucesso.
pause
