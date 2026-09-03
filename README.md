# Sistema Web de Gestão Escolar

Sistema web para gestão escolar com três funcionalidades principais:

- **Login com níveis de acesso**: Administrador, Professor e Aluno — cada um vê um painel diferente.
- **Biblioteca Virtual**: upload de livros (PDF), leitura online no navegador e download.
- **Diário Escolar Digital**: professor lança aulas e presença; aluno acompanha o histórico da própria turma.

Feito com **Python + Django + SQLite + Bootstrap**.

## Como rodar o projeto

Abra um terminal dentro da pasta `sistema-escolar` e rode, na ordem:

```bash
# 1. Ativar o ambiente virtual (já vem criado)
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

| Papel      | Usuário     | Senha         |
|------------|-------------|---------------|
| Admin      | `admin`      | `admin123`     |
| Professor  | `professor1` | `professor123` |
| Aluno      | `aluno1`     | `aluno123`     |

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

O script imprime um link tipo `https://fedora.tail16a68b.ts.net` — é só mandar esse link. Ele fica no ar enquanto o script estiver rodando; aperte `Ctrl+C` pra encerrar (derruba o servidor e desliga o Funnel automaticamente).

> Enquanto o link estiver ativo, **qualquer pessoa com o link acessa o sistema** — troque as senhas de demonstração (veja a tabela abaixo) antes de compartilhar de verdade, e derrube o túnel (`Ctrl+C`) quando terminar o teste.

> O script usa a porta 8000. Se você já tiver um `python manage.py runserver` rodando em outro terminal, pare ele antes (`Ctrl+C` naquele terminal) pra evitar conflito de porta.

## Estrutura do projeto

- `contas/` — usuário customizado (com papel/tipo), login, logout e painel de cada papel.
- `biblioteca/` — modelo `Livro`, upload, listagem com busca, leitura online e download.
- `diario/` — modelos `Curso`, `Turma` (curso + módulo + identificador opcional pra turmas paralelas), `Disciplina`, `Aula`, `Presenca`; lançamento de aula, presença (junto com a aula ou avulsa, via "Marcar presença").
- `templates/` — template base (menu, mensagens) compartilhado por todas as páginas.

## Cadastrando cursos, turmas, disciplinas e usuários

Use o **painel de administração do Django** em `/admin/` (só o usuário Administrador tem acesso). Lá dá pra:

- Criar cursos técnicos (ex: "Técnico em Informática") e disciplinas.
- Criar turmas dentro de um curso, escolhendo o módulo (normalmente 1 a 3) — se houver mais de uma turma no mesmo módulo, preencha o "Identificador" (ex: A, B) pra diferenciar.
- Criar professores e alunos, e definir o "tipo" de cada um.
- Matricular um aluno numa turma (campo "Turma" no cadastro do usuário).

Não é necessário escrever telas novas pra isso — o Django já gera esse painel automaticamente a partir dos modelos.

## Como cada papel usa o sistema

- **Administrador**: cadastra usuários/cursos/turmas/disciplinas em `/admin/`, e também pode enviar livros e ver todos os diários.
- **Professor**: lança aulas (com conteúdo) e marca presença junto, ou usa "Marcar presença" pra uma chamada rápida sem precisar preencher conteúdo; envia livros para a biblioteca.
- **Aluno**: só enxerga o diário da própria turma; pode ler e baixar livros da biblioteca, mas não enviar.

## Próximos passos possíveis

- Adicionar lançamento de notas/boletim.
- Trocar SQLite por PostgreSQL se for hospedar em produção.
- Hospedar no servidor do colégio ou em um serviço como Render/Railway quando decidirem.
