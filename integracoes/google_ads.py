#!/usr/bin/env python3
"""
integracoes/google_ads.py — Módulo de Integração Sanitizado para a API do Google Ads

Este módulo oferece estruturas completas para:
1. Leitura e relatórios de desempenho de campanhas em GAQL.
2. Template de criação de campanhas de pesquisa (Search) e inclusão de palavras-chave.
"""

import os
from typing import Dict, Any, List, Optional

try:
    from config import Config
    DEVELOPER_TOKEN = Config.GOOGLE_ADS_DEVELOPER_TOKEN
    CUSTOMER_ID = Config.GOOGLE_ADS_CUSTOMER_ID
except ImportError:
    DEVELOPER_TOKEN = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN", "")
    CUSTOMER_ID = os.getenv("GOOGLE_ADS_CUSTOMER_ID", "")


def relatorio_resumo_campanhas(customer_id: Optional[str] = None, data_inicio: str = "", data_fim: str = "") -> Dict[str, Any]:
    """
    Exemplo de função para consultar relatório de desempenho de campanhas no Google Ads.
    """
    cid = customer_id or CUSTOMER_ID
    if not cid or not DEVELOPER_TOKEN:
        return {
            "erro": "CREDENCIAIS_PENDENTES",
            "mensagem": "Configure GOOGLE_ADS_DEVELOPER_TOKEN e GOOGLE_ADS_CUSTOMER_ID no seu arquivo .env"
        }

    query = f"""
        SELECT 
            campaign.id,
            campaign.name,
            campaign.status,
            metrics.cost_micros,
            metrics.impressions,
            metrics.clicks,
            metrics.conversions
        FROM campaign
        WHERE segments.date BETWEEN '{data_inicio}' AND '{data_fim}'
    """

    return {
        "customer_id": cid,
        "periodo": f"{data_inicio} ate {data_fim}",
        "query_executada": query.strip(),
        "observacao": "Execute esta query via biblioteca oficial 'google-ads' ou via REST."
    }


def criar_campanha_search_google(customer_id: Optional[str] = None, nome_campanha: str = "Campanha_Search_Template",
                                orcamento_diario_reais: float = 50.0, palavras_chave: Optional[List[str]] = None) -> Dict[str, Any]:
    """
    Template de estrutura para criar uma campanha de Rede de Pesquisa (Search) no Google Ads.
    
    :param customer_id: ID do cliente no Google Ads (ex: '1234567890')
    :param nome_campanha: Nome da nova campanha
    :param orcamento_diario_reais: Orçamento diário em Reais (R$)
    :param palavras_chave: Lista de palavras-chave para o grupo de anúncios
    """
    cid = customer_id or CUSTOMER_ID
    palavras = palavras_chave or ["gestao de trafego", "agencia de marketing", "anuncios google"]
    
    # Orçamento em micros (R$ 50,00 -> 50_000_000 micros)
    budget_micros = int(orcamento_diario_reais * 1_000_000)

    payload_exemplo = {
        "customer_id": cid,
        "campaign": {
            "name": nome_campanha,
            "advertising_channel_type": "SEARCH",
            "status": "PAUSED",
            "manual_cpc": {},
            "campaign_budget": f"customers/{cid}/campaignBudgets/BUDGET_ID"
        },
        "ad_group": {
            "name": f"{nome_campanha} - Grupo 1",
            "status": "ENABLED"
        },
        "keywords": palavras,
        "budget_micros": budget_micros
    }

    return {
        "ok": True,
        "status": "TEMPLATE_ESTRUTURA_CRIADO",
        "payload_campanha": payload_exemplo,
        "mensagem": "Estrutura pronta para ser enviada via GoogleAdsClient (CampaignService / AdGroupService)."
    }


if __name__ == "__main__":
    print("Módulo de integração Google Ads carregado.")
