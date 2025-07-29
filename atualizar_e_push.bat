@echo off
setlocal EnableDelayedExpansion

REM Perguntar datas de cada fornecedor
set /p dataFormigres=Qual foi a data de atualização do arquivo Formigres.pdf? 
set /p dataIncopisos=Qual foi a data de atualização do arquivo Incopisos.pdf? 
set /p dataHelena=Qual foi a data de atualização do arquivo Helena.pdf? 

REM Rodar scripts Python
echo.
echo 🟡 Executando scripts Python...

python python_scripts\formigres_para_json.py
python python_scripts\incopisos_para_json.py
python python_scripts\helena_para_json.py

REM Atualizar datas com PowerShell
echo.
echo 🔄 Atualizando datas nos arquivos .js com PowerShell...

powershell -Command "(Get-Content pages/api/formigres.js) -replace 'const customLastUpdated = \".*?\";', 'const customLastUpdated = \"!dataFormigres!\";' | Set-Content pages/api/formigres.js"
powershell -Command "(Get-Content pages/api/incopisos.js) -replace 'const customLastUpdated = \".*?\";', 'const customLastUpdated = \"!dataIncopisos!\";' | Set-Content pages/api/incopisos.js"
powershell -Command "(Get-Content pages/api/helena.js) -replace 'const customLastUpdated = \".*?\";', 'const customLastUpdated = \"!dataHelena!\";' | Set-Content pages/api/helena.js"

REM Git
echo.
echo 🟢 Adicionando todas as alterações ao Git...
git add .
git commit -m "Atualizacao automatica dos JSONs e datas customLastUpdated"
git push

echo.
echo ✅ Processo finalizado com sucesso.
pause
