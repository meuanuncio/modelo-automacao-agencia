#!/usr/bin/env python3
"""
integracoes/typebot.py — Módulo Sanitizado para Captura e Atribuição de Leads do Typebot

Permite receber respostas de formulários interativos, qualificar se o lead é MQL e disparar webhooks.
"""

import os
from typing import Dict, Any, Optional

try:
    from config import Config
    TYPEBOT_API_TOKEN = Config.TYPEBOT_API_TOKEN
except ImportError:
    TYPEBOT_API_TOKEN = os.getenv("TYPEBOT_API_TOKEN", "")


def qualificar_lead_typebot(respostas: dict) -> Dict[str, Any]:
    """
    Analisa as respostas de um formulário Typebot e determina a qualificação do lead.
    
    Exemplo de payload `respostas`:
    {
        "nome": "João",
        "faturamento_mensal": "Acima de R$ 50.000",
        "investimento_pretendido": "R$ 3.000/mês",
        "segmento": "E-commerce"
    }
    """
    fat = respostas.get("faturamento_mensal", "")
    inv = respostas.get("investimento_pretendido", "")

    is_mql = False
    if "50.000" in fat or "100.000" in fat or "3.000" in inv:
        is_mql = True

    return {
        "lead_nome": respostas.get("nome"),
        "is_mql": is_mql,
        "classificacao": "MQL_ALTO_VALOR" if is_mql else "LEAD_PADRAO",
        "respostas_brutas": respostas
    }


if __name__ == "__main__":
    print("Módulo de integração Typebot carregado.")
