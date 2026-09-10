#!/usr/bin/env python3
"""
integracoes/meta_ads.py — Integração Sanitizada com Meta Ads Graph API

Permite realizar consultas de métricas de conta/campanha, criação automática de campanhas,
conjuntos de anúncios e anúncios, além de atualização de URLs de destino.
"""

import os
import json
import ssl
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

try:
    from config import Config
    ACCESS_TOKEN = Config.META_ACCESS_TOKEN
    BASE_URL = Config.META_BASE_URL
except ImportError:
    ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
    GRAPH_VERSION = "v21.0"
    BASE_URL = f"https://graph.facebook.com/{GRAPH_VERSION}"

CTX = ssl._create_unverified_context()


def graph_get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Executa uma requisição GET para a Meta Graph API."""
    if params is None:
        params = {}
    params["access_token"] = ACCESS_TOKEN

    url = f"{BASE_URL}/{path}?{urllib.parse.urlencode(params)}"
    try:
        with urllib.request.urlopen(url, timeout=20, context=CTX) as response:
            return json.loads(response.read())
    except Exception as e:
        return {"error": f"Erro na requisição Graph GET: {str(e)}"}


def graph_post(path: str, data: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """Executa uma requisição POST para a Meta Graph API."""
    if data is None:
        data = {}
    data["access_token"] = ACCESS_TOKEN

    payload = urllib.parse.urlencode(data).encode("utf-8")
    req = urllib.request.Request(f"{BASE_URL}/{path}", data=payload, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=20, context=CTX) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as e:
        return {"error": e.read().decode("utf-8")}
    except Exception as e:
        return {"error": f"Erro na requisição Graph POST: {str(e)}"}


def obter_metricas_conta(account_id: str, since: str, until: str) -> Dict[str, Any]:
    """Retorna métricas consolidadas de uma conta de anúncios em determinado período."""
    params = {
        "time_range": json.dumps({"since": since, "until": until}),
        "fields": "spend,impressions,clicks,cpc,cpm,ctr,actions",
        "level": "account"
    }
    
    res = graph_get(f"{account_id}/insights", params=params)
    if "error" in res or not res.get("data"):
        return {"erro": res.get("error", "Sem dados retornados para o período.")}

    dados = res["data"][0]
    spend = float(dados.get("spend", 0.0))
    impressions = int(dados.get("impressions", 0))
    clicks = int(dados.get("clicks", 0))
    
    leads = 0
    actions = dados.get("actions", [])
    for act in actions:
        if act.get("action_type") in ("lead", "onsite_conversion.messaging_conversation_started_7d"):
            leads += int(act.get("value", 0))

    cpl = (spend / leads) if leads > 0 else 0.0
    cpc = (spend / clicks) if clicks > 0 else 0.0
    ctr = (clicks / impressions * 100) if impressions > 0 else 0.0

    return {
        "periodo": f"{since} ate {until}",
        "investimento": round(spend, 2),
        "impressoes": impressions,
        "cliques": clicks,
        "leads": leads,
        "cpl": round(cpl, 2),
        "cpc": round(cpc, 2),
        "ctr_porcentagem": round(ctr, 2)
    }


def criar_campanha_meta(account_id: str, nome: str, objetivo: str = "OUTCOME_LEADS",
                         orcamento_diario_centavos: Optional[int] = None, status: str = "PAUSED") -> Dict[str, Any]:
    """
    Cria uma nova campanha no Meta Ads.
    
    :param account_id: ID da conta no formato 'act_123456789'
    :param nome: Nome da campanha
    :param objetivo: Ex: 'OUTCOME_LEADS', 'OUTCOME_TRAFFIC', 'OUTCOME_SALES'
    :param orcamento_diario_centavos: Valor diário em centavos (ex: 2000 = R$ 20,00)
    :param status: 'PAUSED' ou 'ACTIVE'
    """
    payload = {
        "name": nome,
        "objective": objetivo,
        "status": status,
        "special_ad_categories": json.dumps([])
    }
    if orcamento_diario_centavos:
        payload["daily_budget"] = str(orcamento_diario_centavos)

    return graph_post(f"{account_id}/campaigns", payload)


def criar_conjunto_anuncios_meta(account_id: str, campaign_id: str, nome: str,
                                 targeting: dict, orcamento_diario_centavos: int = 2000,
                                 status: str = "PAUSED") -> Dict[str, Any]:
    """
    Cria um conjunto de anúncios (AdSet) associado a uma campanha.
    """
    payload = {
        "name": nome,
        "campaign_id": campaign_id,
        "daily_budget": str(orcamento_diario_centavos),
        "billing_event": "IMPRESSIONS",
        "optimization_goal": "LEAD_GENERATION",
        "targeting": json.dumps(targeting),
        "status": status
    }
    return graph_post(f"{account_id}/adsets", payload)


def criar_anuncio_meta(account_id: str, adset_id: str, creative_id: str,
                        nome: str, status: str = "PAUSED") -> Dict[str, Any]:
    """
    Cria um anúncio (Ad) associando um criativo a um conjunto de anúncios.
    """
    payload = {
        "name": nome,
        "adset_id": adset_id,
        "creative": json.dumps({"creative_id": creative_id}),
        "status": status
    }
    return graph_post(f"{account_id}/ads", payload)


def atualizar_url_destino_anuncio(ad_id: str, nova_url: str) -> Dict[str, Any]:
    """Atualiza a URL de destino de um anúncio Meta mantendo o criativo existente."""
    ad = graph_get(ad_id, params={"fields": "id,name,creative{id}"})
    if "error" in ad:
        return {"erro": f"Não foi possível ler o anúncio: {ad['error']}"}

    cid = ad.get("creative", {}).get("id")
    if not cid:
        return {"erro": "Anúncio não possui um creative_id associado."}

    res = graph_post(ad_id, {"creative": json.dumps({"creative_id": cid, "link_url": nova_url})})
    if res.get("success") or ("error" not in res):
        return {"ok": True, "ad_id": ad_id, "nova_url": nova_url}
    
    return {"erro": res.get("error", "Falha ao atualizar URL do anúncio.")}


if __name__ == "__main__":
    print("Módulo de integração Meta Ads carregado.")
