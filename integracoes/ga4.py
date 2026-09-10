#!/usr/bin/env python3
"""
integracoes/ga4.py — Módulo de Integração Sanitizado para a Google Analytics Data API (GA4)

Permite consultar resumo de tráfego, usuários ativos, conversões e atribuição de canais/UTMs.
"""

import os
from typing import Dict, Any, Optional, List

try:
    from config import Config
    GA4_PROPERTY_ID = Config.GA4_PROPERTY_ID
    SA_CREDS_PATH = Config.GA4_SERVICE_ACCOUNT_PATH
except ImportError:
    GA4_PROPERTY_ID = os.getenv("GA4_PROPERTY_ID", "")
    SA_CREDS_PATH = os.getenv("SA_CREDS_PATH", "service-account.json")


def obter_resumo_ga4(property_id: Optional[str] = None, since: str = "", until: str = "") -> Dict[str, Any]:
    """
    Retorna métricas consolidadas de tráfego do GA4 (Sessões, Usuários, Eventos de Conversão).
    """
    prop = property_id or GA4_PROPERTY_ID
    if not prop:
        return {
            "erro": "GA4_PROPERTY_ID_PENDENTE",
            "mensagem": "Configure GA4_PROPERTY_ID no seu arquivo .env"
        }

    # Template de estrutura de requisição GA4
    request_payload = {
        "property": f"properties/{prop}",
        "dateRanges": [{"startDate": since, "endDate": until}],
        "metrics": [
            {"name": "activeUsers"},
            {"name": "sessions"},
            {"name": "conversions"},
            {"name": "bounceRate"}
        ],
        "dimensions": [
            {"name": "sessionSourceMedium"}
        ]
    }

    return {
        "property_id": prop,
        "periodo": f"{since} ate {until}",
        "request_payload": request_payload,
        "mensagem": "Estrutura pronta para execução via google-analytics-data SDK ou REST API."
    }


def obter_canais_trafego(property_id: Optional[str] = None, since: str = "", until: str = "") -> List[Dict[str, Any]]:
    """
    Retorna a divisão de tráfego por origem e mídia (ex: google / cpc, meta / cpa, organic).
    """
    prop = property_id or GA4_PROPERTY_ID
    if not prop:
        return []

    # Exemplo de estrutura sanitizada de retorno
    return [
        {"origem_midia": "google / cpc", "sessoes": 1250, "conversoes": 45},
        {"origem_midia": "meta / cpa", "sessoes": 3400, "conversoes": 110},
        {"origem_midia": "direct / none", "sessoes": 890, "conversoes": 15}
    ]


if __name__ == "__main__":
    print("Módulo de integração GA4 carregado.")
