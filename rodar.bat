@echo off
REM Sobe o servidor local do Vereda (Windows). Rode instalar.bat antes,
REM se ainda nao tiver feito.

cd /d "%~dp0"

if not exist venv (
    echo Ambiente virtual nao encontrado. Rode instalar.bat primeiro.
    pause
    exit /b 1
)

call venv\Scripts\activate.bat

echo === Vereda rodando em http://127.0.0.1:8000/ ^(Ctrl+C pra parar^) ===
python manage.py runserver

pause
