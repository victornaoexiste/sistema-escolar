import re

from django.core.exceptions import ValidationError


def _digitos_verificadores(cpf_numeros):
    def calcular(fatia):
        soma = sum(int(d) * peso for d, peso in zip(fatia, range(len(fatia) + 1, 1, -1)))
        resto = (soma * 10) % 11
        return resto if resto < 10 else 0

    primeiro = calcular(cpf_numeros[:9])
    segundo = calcular(cpf_numeros[:9] + str(primeiro))
    return primeiro, segundo


def validar_cpf(valor):
    numeros = re.sub(r'\D', '', valor or '')
    if len(numeros) != 11 or numeros == numeros[0] * 11:
        raise ValidationError('Digite um CPF válido.')
    primeiro, segundo = _digitos_verificadores(numeros)
    if numeros[-2:] != f'{primeiro}{segundo}':
        raise ValidationError('Digite um CPF válido.')
