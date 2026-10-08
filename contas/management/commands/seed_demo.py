import datetime

from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from avisos.models import Aviso
from calendario.models import EventoCalendario
from diario.models import Aula, Curso, Disciplina, HorarioAula, Presenca, Turma

Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Cria dados de exemplo (curso, turma, disciplinas, horários, avisos, eventos) para testar o sistema. Usuários devem ser criados manualmente via createsuperuser.'

    def handle(self, *args, **options):
        self.stdout.write('Criando dados de exemplo...')
        curso, _ = Curso.objects.get_or_create(nome='Técnico em Informática')
        turma, _ = Turma.objects.get_or_create(curso=curso, modulo=2, identificador='', defaults={'ano_letivo': 2026})
        matematica, _ = Disciplina.objects.get_or_create(nome='Matemática')
        portugues, _ = Disciplina.objects.get_or_create(nome='Português')

        HorarioAula.objects.get_or_create(
            turma=turma, disciplina=matematica, dia_semana=HorarioAula.DiaSemana.SEGUNDA,
            defaults={'hora_inicio': datetime.time(8, 0), 'hora_fim': datetime.time(9, 40), 'sala': '12'},
        )
        HorarioAula.objects.get_or_create(
            turma=turma, disciplina=portugues, dia_semana=HorarioAula.DiaSemana.QUARTA,
            defaults={'hora_inicio': datetime.time(10, 0), 'hora_fim': datetime.time(11, 40), 'sala': '12'},
        )

        Aviso.objects.get_or_create(
            titulo='Bem-vindo(a) ao sistema escolar',
            defaults={
                'corpo': 'Este é um aviso de exemplo. Fique de olho no quadro de avisos para novidades da escola.',
                'publico': Aviso.Publico.TODOS,
            },
        )

        EventoCalendario.objects.get_or_create(
            titulo='Início do período de matrícula',
            defaults={
                'tipo': EventoCalendario.Tipo.MATRICULA,
                'data_inicio': datetime.date(2026, 12, 1),
                'data_fim': datetime.date(2026, 12, 15),
            },
        )
        EventoCalendario.objects.get_or_create(
            titulo='Prova bimestral de Matemática',
            defaults={
                'tipo': EventoCalendario.Tipo.PROVA,
                'data_inicio': datetime.date(2026, 11, 10),
                'turma': turma,
            },
        )

        # Aulas de exemplo (sem presenças)
        Aula.objects.get_or_create(
            turma=turma, disciplina=matematica, data=datetime.date(2026, 9, 7),
            defaults={'conteudo': 'Introdução a funções'},
        )
        Aula.objects.get_or_create(
            turma=turma, disciplina=matematica, data=datetime.date(2026, 9, 14),
            defaults={'conteudo': 'Funções do 1º grau'},
        )
        Aula.objects.get_or_create(
            turma=turma, disciplina=portugues, data=datetime.date(2026, 9, 9),
            defaults={'conteudo': 'Interpretação de texto'},
        )

        self.stdout.write(self.style.SUCCESS('Dados de exemplo prontos.'))
        self.stdout.write(self.style.NOTICE('Para acessar o sistema, crie um superuser com: python manage.py createsuperuser'))
