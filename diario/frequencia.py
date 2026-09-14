MINIMO_FREQUENCIA = 75.0


def _percentual(presentes, total):
    return round(presentes / total * 100, 1) if total else 100.0


def frequencia_por_disciplina(turma, aluno):
    """Frequência do aluno em cada disciplina já lecionada na turma."""
    from .models import Aula, Disciplina, Presenca

    linhas = []
    disciplinas = Disciplina.objects.filter(aulas__turma=turma).distinct().order_by('nome')
    for disciplina in disciplinas:
        aulas_disciplina = Aula.objects.filter(turma=turma, disciplina=disciplina)
        total = aulas_disciplina.count()
        presentes = Presenca.objects.filter(aula__in=aulas_disciplina, aluno=aluno, presente=True).count()
        percentual = _percentual(presentes, total)
        linhas.append({
            'disciplina': disciplina,
            'total': total,
            'presentes': presentes,
            'percentual': percentual,
            'em_risco': percentual < MINIMO_FREQUENCIA,
        })
    return linhas


def frequencia_geral(turma, aluno):
    """Percentual de presença do aluno somando todas as disciplinas da turma."""
    from .models import Aula, Presenca

    total = Aula.objects.filter(turma=turma).count()
    presentes = Presenca.objects.filter(aula__turma=turma, aluno=aluno, presente=True).count()
    return _percentual(presentes, total)


def frequencia_turma_por_aluno(turma):
    """Frequência geral de cada aluno da turma, do menor pro maior percentual."""
    from django.contrib.auth import get_user_model

    from .models import Aula, Presenca

    Usuario = get_user_model()
    total_aulas = Aula.objects.filter(turma=turma).count()
    alunos = Usuario.objects.filter(tipo=Usuario.Tipo.ALUNO, turma=turma).order_by('first_name', 'username')

    linhas = []
    for aluno in alunos:
        presentes = Presenca.objects.filter(aula__turma=turma, aluno=aluno, presente=True).count()
        percentual = _percentual(presentes, total_aulas)
        linhas.append({
            'aluno': aluno,
            'total': total_aulas,
            'presentes': presentes,
            'percentual': percentual,
            'em_risco': percentual < MINIMO_FREQUENCIA,
        })
    linhas.sort(key=lambda linha: linha['percentual'])
    return linhas


def alunos_em_risco_por_turma():
    """Turmas que têm pelo menos um aluno abaixo do mínimo de frequência."""
    from .models import Turma

    resultado = []
    for turma in Turma.objects.all():
        em_risco = [linha for linha in frequencia_turma_por_aluno(turma) if linha['em_risco']]
        if em_risco:
            resultado.append({'turma': turma, 'alunos': em_risco})
    return resultado
