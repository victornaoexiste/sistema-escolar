# Vereda

Sistema web de gestão escolar com as seguintes funcionalidades:

- **Login com níveis de acesso**: Administrador, Secretaria, Professor e Aluno — cada um vê um painel diferente.
- **Biblioteca Virtual**: upload de livros (PDF), leitura online no navegador e download.
- **Diário Escolar Digital**: professor lança aulas e presença; aluno acompanha o histórico da própria turma.
- **Horário de aulas**: grade diária e semanal por turma.
- **Quadro de avisos**: publicação de avisos (pra toda a escola, um curso ou uma turma), enviados também por e-mail para os alunos.
- **Frequência mínima (75%)**: cálculo automático de presença por disciplina, com alerta visual pro aluno e relatório de alunos em risco pra secretaria/admin.
- **Documentos auto-atendimento**: aluno gera e baixa em PDF, na hora, a declaração de matrícula e o extrato de frequência.
- **Calendário Acadêmico**: feriados, provas, período de matrícula e outros eventos, gerais ou por turma.

Feito com **Python + Django + SQLite + Bootstrap**.

## Como rodar o projeto

### Caminho rápido (scripts prontos)

**Linux/macOS:**
```bash
./instalar.sh   # só na primeira vez (ou se mudar o requirements.txt)
./rodar.sh      # sempre que for subir o servidor
```

**Windows:** dê dois cliques em `instalar.bat` (só na primeira vez) e depois em `rodar.bat` (sempre que for subir o servidor). Se o Windows nunca teve Python instalado, baixe em https://www.python.org/downloads/windows/ e marque a opção "Add python.exe to PATH" no instalador antes de rodar o `instalar.bat`.

O instalador cria o ambiente virtual, instala as dependências, aplica as migrações e pergunta se você quer criar os usuários/dados de exemplo.

### Caminho manual

Abra um terminal dentro da pasta `sistema-escolar` e rode, na ordem:

```bash
# 1. Criar e ativar o ambiente virtual (só na primeira vez)
python3 -m venv venv
source venv/bin/activate

# 2. Instalar as dependências (só precisa na primeira vez, ou se mudar o requirements.txt)
pip install -r requirements.txt

# 3. Aplicar as migrações do banco de dados
python manage.py migrate

# 4. Criar usuários e dados de exemplo pra testar (admin, professor, aluno, curso, turma)
python manage.py seed_demo

# 5. Subir o servidor
python manage.py runserver
```

Depois abra **http://127.0.0.1:8000/** no navegador.

## Usuários de teste (criados pelo `seed_demo`)

| Papel      | Usuário       | Senha           |
|------------|---------------|-----------------|
| Admin      | `admin`       | `741852963ç`    |
| Secretaria | `secretaria1` | `741852963ç`    |
| Professor  | `professor1`  | `741852963ç`    |
| Aluno      | `aluno1`      | `741852963ç`    |

> Troque essas senhas (ou apague esses usuários) antes de apresentar/publicar o projeto de verdade — elas são só para teste local.

## Testar com alguém de fora (Tailscale Funnel)

Se você tem [Tailscale](https://tailscale.com/) instalado e logado nesta máquina, dá pra gerar um link público temporário e mandar pra alguém testar, mesmo que a pessoa não tenha Tailscale.

**Configuração única** (só precisa rodar uma vez nesta máquina): o Tailscale exige privilégio de administrador pra ligar o Funnel. Pra não precisar de `sudo` toda vez, libere seu usuário como operador:

```bash
sudo tailscale set --operator=$USER
```

Depois disso, sempre que quiser gerar o link de teste:

```bash
./tailscale_run.sh
```

O script imprime um link tipo `https://<sua-maquina>.<seu-tailnet>.ts.net` — é só mandar esse link. Ele fica no ar enquanto o script estiver rodando; aperte `Ctrl+C` pra encerrar (derruba o servidor e desliga o Funnel automaticamente).

> Enquanto o link estiver ativo, **qualquer pessoa com o link acessa o sistema** — troque as senhas de demonstração (veja a tabela abaixo) antes de compartilhar de verdade, e derrube o túnel (`Ctrl+C`) quando terminar o teste.

> O script usa a porta 8000. Se você já tiver um `python manage.py runserver` rodando em outro terminal, pare ele antes (`Ctrl+C` naquele terminal) pra evitar conflito de porta.

## Estrutura do projeto

- `contas/` — usuário customizado (com papel/tipo, matrícula, data de nascimento e contato do responsável), login, logout, painel de cada papel e cadastro simplificado de aluno (fora do `/admin/`).
- `biblioteca/` — modelo `Livro`, upload, listagem com busca, leitura online e download.
- `diario/` — modelos `Curso`, `Turma` (curso + módulo + identificador opcional pra turmas paralelas), `Disciplina`, `Aula`, `Presenca`, `HorarioAula`; lançamento de aula, presença (junto com a aula ou avulsa, via "Marcar presença") e cadastro do horário de aulas por turma.
- `avisos/` — modelo `Aviso` (com público-alvo: toda a escola, um curso ou uma turma); quadro de avisos e envio automático por e-mail para os alunos do público-alvo.
- `calendario/` — modelo `EventoCalendario` (feriado, recesso, prova, período de matrícula ou evento; geral ou de uma turma específica); agenda agrupada por mês.
- `contas/documentos.py` — geração de PDF (declaração de matrícula e extrato de frequência) com a biblioteca `reportlab`.
- `diario/frequencia.py` — cálculo de frequência por disciplina, frequência geral e listagem de alunos abaixo do mínimo de 75%.
- `templates/` — template base (menu, mensagens) compartilhado por todas as páginas.

## Cadastrando cursos, turmas, disciplinas e usuários de sistema

Cursos técnicos, turmas, disciplinas e contas de Professor/Secretaria/Administrador são cadastrados pelo **painel de administração do Django** em `/admin/` (só o usuário Administrador tem acesso — Secretaria não entra ali). Lá dá pra:

- Criar cursos técnicos (ex: "Técnico em Informática") e disciplinas.
- Criar turmas dentro de um curso, escolhendo o módulo (normalmente 1 a 3) — se houver mais de uma turma no mesmo módulo, preencha o "Identificador" (ex: A, B) pra diferenciar.
- Criar contas de professor e secretaria.

Já o **cadastro de aluno** tem uma tela própria, bem mais simples que o `/admin/` — veja abaixo.

## Cadastrando alunos

Administrador e Secretaria têm acesso ao menu **"Alunos"**, com uma tela dedicada (fora do `/admin/`) só com o que importa pro dia a dia: nome, usuário/senha de acesso, matrícula (digitada manualmente), turma, data de nascimento e contato do responsável. Dá pra cadastrar, listar/buscar e editar os dados de qualquer aluno por ali.

## Como cada papel usa o sistema

- **Administrador**: acesso completo — cadastra professores/secretaria/cursos/turmas/disciplinas em `/admin/`, cadastra alunos, envia livros, cadastra horários e eventos do calendário, publica avisos, vê/corrige o diário de todas as turmas e acompanha a frequência (com alerta de alunos em risco no próprio painel).
- **Secretaria**: cadastra e edita alunos (nome, matrícula, turma, contato, e-mail), cadastra horários de aula e eventos do calendário, publica avisos, corrige a presença de qualquer aluno, acompanha a frequência de todas as turmas (alerta de risco no painel) e gera declaração/extrato em PDF de qualquer aluno (sem acesso ao `/admin/` nem às outras áreas do sistema).
- **Professor**: lança aulas (com conteúdo) e marca presença junto, ou usa "Marcar presença" pra uma chamada rápida sem precisar preencher conteúdo; envia livros para a biblioteca; publica avisos; consulta a frequência das turmas em que leciona.
- **Aluno**: enxerga o diário, o horário, a frequência (com alerta se estiver abaixo de 75%), os avisos e os eventos do calendário da própria turma (mais os gerais da escola); gera seus próprios documentos em PDF; pode ler e baixar livros da biblioteca, mas não enviar.

## Enviando avisos por e-mail de verdade

Por padrão, os e-mails de aviso só aparecem no terminal onde o servidor está rodando (não são enviados de verdade) — bom pra testar sem precisar de conta de e-mail. Pra ativar o envio real (recomendado: Gmail com **senha de app**, não a senha normal da conta — gere uma em https://myaccount.google.com/apppasswords), defina estas variáveis de ambiente antes de subir o servidor:

```bash
export DJANGO_EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
export DJANGO_EMAIL_HOST_USER=seuemail@gmail.com
export DJANGO_EMAIL_HOST_PASSWORD=xxxxxxxxxxxxxxxx   # senha de app do Gmail, com 16 caracteres
python manage.py runserver
```

> Cada aluno só recebe o aviso por e-mail se tiver um e-mail cadastrado (campo `email` do usuário, editável em "Alunos" ou no `/admin/`). O envio é feito em cópia oculta (BCC) — nenhum aluno vê o e-mail dos outros.

## Próximos passos possíveis

- Adicionar lançamento de notas/boletim.
- Estágio supervisionado / TCC: controle de horas e status de entrega.
- Comunicação bidirecional (aluno consegue responder/perguntar, não só receber avisos).
- Trocar SQLite por PostgreSQL se for hospedar em produção.
- Hospedar no servidor do colégio ou em um serviço como Render/Railway quando decidirem.
