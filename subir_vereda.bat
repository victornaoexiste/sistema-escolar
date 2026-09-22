@echo off
REM Sobe o servidor do Vereda sem pedir nada (sem prompts, sem pause) --
REM feito pra ser chamado por uma tarefa agendada do Windows, sem ninguem
REM sentado no teclado. Pra rodar na mao, use rodar.bat em vez deste.

cd /d "%~dp0"

if not exist venv (
    exit /b 1
)

call venv\Scripts\activate.bat
python manage.py runserver 127.0.0.1:8000 >> vereda.log 2>&1
