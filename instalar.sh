#!/usr/bin/env bash
# Instalador do Vereda (Linux/macOS) — cria o ambiente virtual, instala as
# dependências e prepara o banco de dados. Rode uma vez só (ou de novo se
# o requirements.txt mudar).
#
# Uso: ./instalar.sh [--auto]
#   --auto  pula a pergunta do final — usado quando este script é chamado
#           por outro script, sem ninguém sentado no teclado.
set -e

AUTO=0
[ "$1" = "--auto" ] && AUTO=1

cd "$(dirname "$0")"

echo "=== Vereda — instalador (Linux/macOS) ==="

# 1. Localizar o Python 3
if command -v python3 >/dev/null 2>&1; then
    PYTHON=python3
elif command -v python >/dev/null 2>&1; then
    PYTHON=python
else
    echo "Erro: Python 3 não encontrado. Instale com o gerenciador de pacotes da sua distro"
    echo "(ex.: 'sudo apt install python3 python3-venv' no Debian/Ubuntu) e rode este script de novo."
    exit 1
fi
echo "-> Usando $($PYTHON --version)"

# 2. Criar o ambiente virtual, se ainda não existir
if [ ! -d "venv" ]; then
    echo "-> Criando ambiente virtual em ./venv"
    "$PYTHON" -m venv venv
else
    echo "-> Ambiente virtual já existe, reaproveitando"
fi

# 3. Ativar o ambiente virtual
source venv/bin/activate

# 4. Instalar as dependências
echo "-> Atualizando pip"
pip install --upgrade pip --quiet
echo "-> Instalando dependências do requirements.txt"
pip install -r requirements.txt

# 5. Aplicar as migrações do banco de dados
echo "-> Aplicando migrações do banco de dados"
python manage.py migrate

# 6. Perguntar se quer criar os usuários de teste
if [ "$AUTO" = "1" ]; then
    resposta=S
else
    read -p "Criar usuários e dados de exemplo pra testar (admin, professor1, secretaria1, aluno1)? [S/n] " resposta
fi
resposta=${resposta:-S}
if [[ "$resposta" =~ ^[Ss]$ ]]; then
    python manage.py seed_demo
fi

echo ""
echo "=== Instalação concluída! ==="
echo "Pra subir o servidor, rode: ./rodar.sh"
