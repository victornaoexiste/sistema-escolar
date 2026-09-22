import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from avisos.models import Aviso
from calendario.models import EventoCalendario
from diario.models import Aula, Curso, Disciplina, HorarioAula, Presenca, Turma

Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Cria usuários e dados de exemplo (admin, professor, aluno, curso, turma) para testar o sistema.'

    def handle(self, *args, **options):
        curso, _ = Curso.objects.get_or_create(nome='Técnico em Informática')
        turma, _ = Turma.objects.get_or_create(curso=curso, modulo=2, identificador='', defaults={'ano_letivo': 2026})
        matematica, _ = Disciplina.objects.get_or_create(nome='Matemática')
        portugues, _ = Disciplina.objects.get_or_create(nome='Português')

        senha_demo = '741852963ç'

        if not Usuario.objects.filter(username='admin').exists():
            Usuario.objects.create_superuser(
                username='admin', password=senha_demo, email='admin@escola.local', tipo=Usuario.Tipo.ADMIN
            )
            self.stdout.write(self.style.SUCCESS(f'Criado: admin / {senha_demo}'))

        if not Usuario.objects.filter(username='secretaria1').exists():
            Usuario.objects.create_user(
                username='secretaria1',
                password=senha_demo,
                first_name='Maria',
                last_name='Secretaria',
                tipo=Usuario.Tipo.SECRETARIA,
            )
            self.stdout.write(self.style.SUCCESS(f'Criado: secretaria1 / {senha_demo}'))

        professor, criado = Usuario.objects.get_or_create(
            username='professor1',
            defaults={
                'first_name': 'Ana',
                'last_name': 'Professora',
                'tipo': Usuario.Tipo.PROFESSOR,
            },
        )
        if criado:
            professor.set_password(senha_demo)
            professor.save()
            self.stdout.write(self.style.SUCCESS(f'Criado: professor1 / {senha_demo}'))

        aluno, criado = Usuario.objects.get_or_create(
            username='aluno1',
            defaults={
                'first_name': 'João',
                'last_name': 'Aluno',
                'email': 'aluno1@escola.local',
                'tipo': Usuario.Tipo.ALUNO,
                'turma': turma,
                'matricula': '2026001',
            },
        )
        if criado:
            aluno.set_password(senha_demo)
            aluno.save()
            self.stdout.write(self.style.SUCCESS(f'Criado: aluno1 / {senha_demo}'))

        HorarioAula.objects.get_or_create(
            turma=turma, disciplina=matematica, dia_semana=HorarioAula.DiaSemana.SEGUNDA,
            defaults={'professor': professor, 'hora_inicio': datetime.time(8, 0), 'hora_fim': datetime.time(9, 40), 'sala': '12'},
        )
        HorarioAula.objects.get_or_create(
            turma=turma, disciplina=portugues, dia_semana=HorarioAula.DiaSemana.QUARTA,
            defaults={'professor': professor, 'hora_inicio': datetime.time(10, 0), 'hora_fim': datetime.time(11, 40), 'sala': '12'},
        )

        Aviso.objects.get_or_create(
            titulo='Bem-vindo(a) ao sistema escolar',
            defaults={
                'corpo': 'Este é um aviso de exemplo. Fique de olho no quadro de avisos para novidades da escola.',
                'autor': professor,
                'publico': Aviso.Publico.TODOS,
            },
        )

        EventoCalendario.objects.get_or_create(
            titulo='Início do período de matrícula',
            defaults={
                'tipo': EventoCalendario.Tipo.MATRICULA,
                'data_inicio': datetime.date(2026, 12, 1),
                'data_fim': datetime.date(2026, 12, 15),
                'criado_por': professor,
            },
        )
        EventoCalendario.objects.get_or_create(
            titulo='Prova bimestral de Matemática',
            defaults={
                'tipo': EventoCalendario.Tipo.PROVA,
                'data_inicio': datetime.date(2026, 11, 10),
                'turma': turma,
                'criado_por': professor,
            },
        )

        # Aulas e presenças de exemplo, pra demonstrar o cálculo de frequência
        # (matemática fica de propósito abaixo do mínimo de 75%, pra mostrar o alerta).
        aula1, _ = Aula.objects.get_or_create(
            turma=turma, disciplina=matematica, data=datetime.date(2026, 9, 7),
            defaults={'professor': professor, 'conteudo': 'Introdução a funções'},
        )
        aula2, _ = Aula.objects.get_or_create(
            turma=turma, disciplina=matematica, data=datetime.date(2026, 9, 14),
            defaults={'professor': professor, 'conteudo': 'Funções do 1º grau'},
        )
        aula3, _ = Aula.objects.get_or_create(
            turma=turma, disciplina=portugues, data=datetime.date(2026, 9, 9),
            defaults={'professor': professor, 'conteudo': 'Interpretação de texto'},
        )
        Presenca.objects.get_or_create(aula=aula1, aluno=aluno, defaults={'presente': True})
        Presenca.objects.get_or_create(aula=aula2, aluno=aluno, defaults={'presente': False})
        Presenca.objects.get_or_create(aula=aula3, aluno=aluno, defaults={'presente': True})

        self.stdout.write(self.style.SUCCESS('Dados de exemplo prontos.'))
