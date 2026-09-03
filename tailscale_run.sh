#!/bin/bash
# Sobe o sistema escolar e expõe pra internet via Tailscale Funnel,
# pra você mandar o link pra alguém testar de fora da sua rede Tailscale.
#
# Uso: ./tailscale_run.sh
# Pra parar: Ctrl+C (derruba o Django e desliga o Funnel automaticamente).
set -e
cd "$(dirname "$0")"

if ! command -v tailscale >/dev/null; then
    echo "Tailscale não encontrado. Instale em https://tailscale.com/download antes de continuar."
    exit 1
fi

source venv/bin/activate

# Descobre o hostname público desta máquina na tailnet (ex: fedora.tail16a68b.ts.net)
HOSTNAME=$(tailscale status --json | python3 -c "
import json, sys
d = json.load(sys.stdin)
self = d.get('Self', {})
print(f\"{self.get('HostName')}.{d.get('MagicDNSSuffix')}\")
")

if [ -z "$HOSTNAME" ] || [ "$HOSTNAME" = "." ]; then
    echo "Não consegui descobrir o hostname da tailnet. O Tailscale está rodando e logado (tailscale status)?"
    exit 1
fi

export DJANGO_DEBUG=False
export DJANGO_ALLOWED_HOSTS="$HOSTNAME,127.0.0.1,localhost"
export DJANGO_CSRF_TRUSTED_ORIGINS="https://$HOSTNAME"
# Chave própria pra essa sessão exposta publicamente (não é a do repositório).
export DJANGO_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(50))")

echo "Aviso: enquanto este script roda, o sistema fica acessível por qualquer pessoa que tenha o link."
echo "Troque as senhas de demonstração (admin123 etc.) antes de compartilhar de verdade."
echo

python manage.py runserver --insecure 127.0.0.1:8000 >/tmp/sistema-escolar-runserver.log 2>&1 &
DJANGO_PID=$!

cleanup() {
    echo
    echo "Encerrando..."
    kill "$DJANGO_PID" 2>/dev/null
    tailscale funnel reset >/dev/null 2>&1
}
trap cleanup EXIT INT TERM

sleep 2
if ! kill -0 "$DJANGO_PID" 2>/dev/null; then
    echo "O Django não subiu. Veja o log:"
    cat /tmp/sistema-escolar-runserver.log
    exit 1
fi

echo "Link público (envie esse link):  https://$HOSTNAME"
echo
tailscale funnel 8000
