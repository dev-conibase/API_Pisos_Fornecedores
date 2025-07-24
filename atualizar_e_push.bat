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

REM Atualizar data no formigres.js
echo.
echo 🔄 Atualizando data em pages/api/formigres.js...
(for /f "delims=" %%a in ('type pages\api\formigres.js') do (
    set "line=%%a"
    echo !line:const customLastUpdated =^=! | findstr /c:"const customLastUpdated =" >nul
    if !errorlevel! == 0 (
        echo const customLastUpdated = "!dataFormigres!";
    ) else (
        echo !line!
    )
)) > temp_formigres.js
move /y temp_formigres.js pages\api\formigres.js >nul

REM Atualizar data no incopisos.js
echo.
echo 🔄 Atualizando data em pages/api/incopisos.js...
(for /f "delims=" %%a in ('type pages\api\incopisos.js') do (
    set "line=%%a"
    echo !line:const customLastUpdated =^=! | findstr /c:"const customLastUpdated =" >nul
    if !errorlevel! == 0 (
        echo const customLastUpdated = "!dataIncopisos!";
    ) else (
        echo !line!
    )
)) > temp_incopisos.js
move /y temp_incopisos.js pages\api\incopisos.js >nul

REM Atualizar data no helena.js
echo.
echo 🔄 Atualizando data em pages\api\helena.js...
(for /f "delims=" %%a in ('type pages\api\helena.js') do (
    set "line=%%a"
    echo !line:const customLastUpdated =^=! | findstr /c:"const customLastUpdated =" >nul
    if !errorlevel! == 0 (
        echo const customLastUpdated = "!dataHelena!";
    ) else (
        echo !line!
    )
)) > temp_helena.js
move /y temp_helena.js pages\api\helena.js >nul

REM Git
echo.
echo 🟢 Adicionando todas as alterações ao Git...
git add .
git commit -m "Atualização automática dos JSONs e datas customLastUpdated"
git push

echo.
echo ✅ Processo finalizado com sucesso.
pause
