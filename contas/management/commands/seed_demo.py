from django.contrib.auth import get_user_model
from django.core.management.base import BaseCommand

from diario.models import Disciplina, Turma

Usuario = get_user_model()


class Command(BaseCommand):
    help = 'Cria usuários e dados de exemplo (admin, professor, aluno, turma) para testar o sistema.'

    def handle(self, *args, **options):
        turma, _ = Turma.objects.get_or_create(nome='9º Ano A', defaults={'ano_letivo': 2026})
        Disciplina.objects.get_or_create(nome='Matemática')
        Disciplina.objects.get_or_create(nome='Português')

        if not Usuario.objects.filter(username='admin').exists():
            Usuario.objects.create_superuser(
                username='admin', password='admin123', email='admin@escola.local', tipo=Usuario.Tipo.ADMIN
            )
            self.stdout.write(self.style.SUCCESS('Criado: admin / admin123'))

        if not Usuario.objects.filter(username='professor1').exists():
            Usuario.objects.create_user(
                username='professor1',
                password='professor123',
                first_name='Ana',
                last_name='Professora',
                tipo=Usuario.Tipo.PROFESSOR,
            )
            self.stdout.write(self.style.SUCCESS('Criado: professor1 / professor123'))

        if not Usuario.objects.filter(username='aluno1').exists():
            Usuario.objects.create_user(
                username='aluno1',
                password='aluno123',
                first_name='João',
                last_name='Aluno',
                tipo=Usuario.Tipo.ALUNO,
                turma=turma,
            )
            self.stdout.write(self.style.SUCCESS('Criado: aluno1 / aluno123'))

        self.stdout.write(self.style.SUCCESS('Dados de exemplo prontos.'))
