#!/usr/bin/env bash
# Sobe o servidor local do Vereda (Linux/macOS). Rode ./instalar.sh antes,
# se ainda não tiver feito.
set -e

cd "$(dirname "$0")"

if [ ! -d "venv" ]; then
    echo "Ambiente virtual não encontrado. Rode ./instalar.sh primeiro."
    exit 1
fi

source venv/bin/activate

echo "=== Vereda rodando em http://127.0.0.1:8000/ (Ctrl+C pra parar) ==="
python manage.py runserver
