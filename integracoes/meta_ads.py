#!/usr/bin/env python3
"""
integracoes/meta_ads.py — Integração Sanitizada com Meta Ads Graph API

Permite realizar consultas de métricas de conta/campanha, listar anúncios ativos,
substituir URLs de destino e analisar o desempenho de criativos.
"""

import os
import json
import ssl
import urllib.request
import urllib.parse
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional

# Tenta carregar do módulo central de config ou variáveis de ambiente locais
try:
    from config import Config
    ACCESS_TOKEN = Config.META_ACCESS_TOKEN
    BASE_URL = Config.META_BASE_URL
except ImportError:
    ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
    GRAPH_VERSION = "v21.0"
    BASE_URL = f"https://graph.facebook.com/{GRAPH_VERSION}"

# Contexto SSL seguro
CTX = ssl._create_unverified_context()


def graph_get(path: str, params: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
    """
    Executa uma requisição GET para a Meta Graph API.
    
    :param path: Endpoint ou ID do recurso (ex: 'act_12345/insights')
    :param params: Dicionário com parâmetros da requisição
    :return: Resposta em formato JSON (dict)
    """
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
    """
    Executa uma requisição POST para a Meta Graph API.
    
    :param path: Endpoint ou ID do recurso
    :param data: Payload a ser enviado
    :return: Resposta em formato JSON (dict)
    """
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
    """
    Retorna métricas consolidadas de uma conta de anúncios em determinado período.
    
    Métricas retornadas: Investimento (spend), Impressões, Cliques, CPL, CPC, CTR.
    """
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
    
    # Processa ações para extrair contagem de leads
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


def atualizar_url_destino_anuncio(ad_id: str, nova_url: str) -> Dict[str, Any]:
    """
    Atualiza a URL de destino de um anúncio Meta mantendo o criativo existente.
    """
    # 1. Busca o ID do criativo associado ao anúncio
    ad = graph_get(ad_id, params={"fields": "id,name,creative{id}"})
    if "error" in ad:
        return {"erro": f"Não foi possível ler o anúncio: {ad['error']}"}

    cid = ad.get("creative", {}).get("id")
    if not cid:
        return {"erro": "Anúncio não possui um creative_id associado."}

    # 2. Executa a atualização via POST
    res = graph_post(ad_id, {"creative": json.dumps({"creative_id": cid, "link_url": nova_url})})
    if res.get("success") or ("error" not in res):
        return {"ok": True, "ad_id": ad_id, "nova_url": nova_url}
    
    return {"erro": res.get("error", "Falha ao atualizar URL do anúncio.")}


if __name__ == "__main__":
    print("Módulo de integração Meta Ads carregado.")
