import io

from django.utils import timezone
from reportlab.lib import colors
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import cm
from reportlab.platypus import Paragraph, SimpleDocTemplate, Spacer, Table, TableStyle

NOME_ESCOLA = 'Escola Técnica'


def _documento_base(titulo):
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(
        buffer, pagesize=A4,
        topMargin=2.5 * cm, bottomMargin=2.5 * cm, leftMargin=2.5 * cm, rightMargin=2.5 * cm,
    )
    estilos = getSampleStyleSheet()
    elementos = [
        Paragraph(NOME_ESCOLA, ParagraphStyle('cabecalho', parent=estilos['Heading2'], alignment=1)),
        Spacer(1, 0.3 * cm),
        Paragraph(titulo, ParagraphStyle('titulo', parent=estilos['Heading3'], alignment=1)),
        Spacer(1, 1 * cm),
    ]
    return buffer, doc, elementos, estilos


def gerar_declaracao_matricula(aluno):
    buffer, doc, elementos, estilos = _documento_base('Declaração de Matrícula')

    corpo = ParagraphStyle('corpo', parent=estilos['Normal'], fontSize=12, leading=20, alignment=4)
    hoje = timezone.localdate()
    texto = (
        f'Declaramos, para os devidos fins, que <b>{aluno.get_full_name() or aluno.username}</b>'
        f'{f", matrícula nº {aluno.matricula},"if aluno.matricula else ""} '
        f'está regularmente matriculado(a) no curso <b>{aluno.turma.curso}</b>, módulo {aluno.turma.modulo}'
        f'{f" {aluno.turma.identificador}" if aluno.turma.identificador else ""}, '
        f'ano letivo de {aluno.turma.ano_letivo}, desta instituição de ensino técnico.'
    )
    elementos.append(Paragraph(texto, corpo))
    elementos.append(Spacer(1, 2 * cm))
    elementos.append(Paragraph(f'Documento emitido eletronicamente em {hoje.strftime("%d/%m/%Y")}.', corpo))

    doc.build(elementos)
    return buffer.getvalue()


def gerar_extrato_frequencia(aluno):
    from diario.frequencia import frequencia_por_disciplina

    buffer, doc, elementos, estilos = _documento_base('Extrato de Frequência')

    corpo = ParagraphStyle('corpo', parent=estilos['Normal'], fontSize=11, leading=16)
    hoje = timezone.localdate()
    elementos.append(Paragraph(
        f'Aluno(a): <b>{aluno.get_full_name() or aluno.username}</b>'
        f'{f" — matrícula nº {aluno.matricula}" if aluno.matricula else ""}<br/>'
        f'Turma: {aluno.turma}',
        corpo,
    ))
    elementos.append(Spacer(1, 0.8 * cm))

    linhas = frequencia_por_disciplina(aluno.turma, aluno)
    dados_tabela = [['Disciplina', 'Aulas', 'Presenças', 'Frequência']]
    for linha in linhas:
        dados_tabela.append([
            str(linha['disciplina']), str(linha['total']), str(linha['presentes']), f"{linha['percentual']}%",
        ])

    tabela = Table(dados_tabela, colWidths=[7 * cm, 2.5 * cm, 3 * cm, 3 * cm])
    tabela.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.HexColor('#221F1A')),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.white),
        ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),
        ('FONTNAME', (1, 1), (-1, -1), 'Courier'),
        ('GRID', (0, 0), (-1, -1), 0.5, colors.HexColor('#DAD2BC')),
        ('ROWBACKGROUNDS', (0, 1), (-1, -1), [colors.white, colors.HexColor('#EEEBDE')]),
        ('ALIGN', (1, 0), (-1, -1), 'CENTER'),
        ('VALIGN', (0, 0), (-1, -1), 'MIDDLE'),
        ('TOPPADDING', (0, 0), (-1, -1), 6),
        ('BOTTOMPADDING', (0, 0), (-1, -1), 6),
    ]))
    elementos.append(tabela)
    elementos.append(Spacer(1, 1.5 * cm))
    elementos.append(Paragraph(
        'O mínimo de frequência exigido por disciplina é de 75%.', corpo,
    ))
    elementos.append(Spacer(1, 1 * cm))
    elementos.append(Paragraph(f'Documento emitido eletronicamente em {hoje.strftime("%d/%m/%Y")}.', corpo))

    doc.build(elementos)
    return buffer.getvalue()
