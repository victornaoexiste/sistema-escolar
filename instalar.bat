@echo off
REM Instalador do Vereda (Windows) -- cria o ambiente virtual, instala as
REM dependencias e prepara o banco de dados. Rode uma vez so (ou de novo se
REM o requirements.txt mudar).

cd /d "%~dp0"

echo === Vereda - instalador (Windows) ===

REM 1. Localizar o Python 3
where python >nul 2>nul
if %errorlevel%==0 (
    set PYTHON=python
) else (
    where py >nul 2>nul
    if %errorlevel%==0 (
        set PYTHON=py -3
    ) else (
        echo Erro: Python 3 nao encontrado.
        echo Instale em https://www.python.org/downloads/windows/ ^(marque "Add python.exe to PATH" no instalador^) e rode este script de novo.
        pause
        exit /b 1
    )
)
echo -^> Usando %PYTHON%

REM 2. Criar o ambiente virtual, se ainda nao existir
if not exist venv (
    echo -^> Criando ambiente virtual em .\venv
    %PYTHON% -m venv venv
    if errorlevel 1 (
        echo Erro ao criar o ambiente virtual.
        pause
        exit /b 1
    )
) else (
    echo -^> Ambiente virtual ja existe, reaproveitando
)

REM 3. Ativar o ambiente virtual
call venv\Scripts\activate.bat

REM 4. Instalar as dependencias
echo -^> Atualizando pip
python -m pip install --upgrade pip --quiet
echo -^> Instalando dependencias do requirements.txt
pip install -r requirements.txt
if errorlevel 1 (
    echo Erro ao instalar as dependencias.
    pause
    exit /b 1
)

REM 5. Aplicar as migracoes do banco de dados
echo -^> Aplicando migracoes do banco de dados
python manage.py migrate

REM 6. Perguntar se quer criar os usuarios de teste
set /p resposta="Criar usuarios e dados de exemplo pra testar (admin, professor1, secretaria1, aluno1)? [S/n] "
if "%resposta%"=="" set resposta=S
if /i "%resposta%"=="S" (
    python manage.py seed_demo
)

echo.
echo === Instalacao concluida! ===
echo Pra subir o servidor, de dois cliques em rodar.bat
pause
