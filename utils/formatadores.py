#!/usr/bin/env python3
"""
utils/formatadores.py — Funções Utilitárias para Formatação de Dados

Formatação de moeda BRL, números de telefone, porcentagens e datas.
"""

import re
from datetime import datetime


def formatar_moeda_brl(valor: float) -> str:
    """
    Formata um valor float para a moeda brasileira (ex: R$ 1.250,50).
    """
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


def formatar_telefone_whatsapp(telefone: str) -> str:
    """
    Normaliza uma string de telefone para o padrão WhatsApp Brasil (55 + DDD + Número).
    Ex: '(11) 99999-8888' -> '5511999998888'
    """
    numeros = re.sub(r"\D", "", telefone)
    if not numeros.startswith("55") and len(numeros) in (10, 11):
        numeros = "55" + numeros
    return numeros


def formatar_porcentagem(valor: float) -> str:
    """
    Formata float para porcentagem (ex: 2.35 -> '2,35%').
    """
    return f"{valor:.2f}%".replace(".", ",")


if __name__ == "__main__":
    print("Testes de formatação:")
    print("Moeda:", formatar_moeda_brl(1250.5))
    print("Telefone:", formatar_telefone_whatsapp("(11) 99999-8888"))
    print("Porcentagem:", formatar_porcentagem(3.14159))
