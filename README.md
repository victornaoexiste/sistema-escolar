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

# 4. Criar usuários e dados de exemplo pra testar (admin, professor, aluno, turma)
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

## Estrutura do projeto

- `contas/` — usuário customizado (com papel/tipo), login, logout e painel de cada papel.
- `biblioteca/` — modelo `Livro`, upload, listagem com busca, leitura online e download.
- `diario/` — modelos `Turma`, `Disciplina`, `Aula`, `Presenca`; lançamento de aula e presença.
- `templates/` — template base (menu, mensagens) compartilhado por todas as páginas.

## Cadastrando turmas, disciplinas e usuários

Use o **painel de administração do Django** em `/admin/` (só o usuário Administrador tem acesso). Lá dá pra:

- Criar turmas e disciplinas.
- Criar professores e alunos, e definir o "tipo" de cada um.
- Matricular um aluno numa turma (campo "Turma" no cadastro do usuário).

Não é necessário escrever telas novas pra isso — o Django já gera esse painel automaticamente a partir dos modelos.

## Como cada papel usa o sistema

- **Administrador**: cadastra usuários/turmas/disciplinas em `/admin/`, e também pode enviar livros e ver todos os diários.
- **Professor**: lança aulas e marca presença das próprias turmas; envia livros para a biblioteca.
- **Aluno**: só enxerga o diário da própria turma; pode ler e baixar livros da biblioteca, mas não enviar.

## Próximos passos possíveis

- Adicionar lançamento de notas/boletim.
- Trocar SQLite por PostgreSQL se for hospedar em produção.
- Hospedar no servidor do colégio ou em um serviço como Render/Railway quando decidirem.
