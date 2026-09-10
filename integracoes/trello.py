#!/usr/bin/env python3
"""
integracoes/trello.py — Integração com Trello REST API para Gestão de Kanban e Onboarding

Permite criar novos cartões de cliente, mover de listas e adicionar checklists de onboarding.
"""

import os
import requests
from typing import Dict, Any, Optional

try:
    from config import Config
    API_KEY = Config.TRELLO_API_KEY
    TOKEN = Config.TRELLO_TOKEN
    LISTA_NOVOS_CLIENTES = Config.TRELLO_LIST_NOVOS_CLIENTES_ID
except ImportError:
    API_KEY = os.getenv("TRELLO_API_KEY", "")
    TOKEN = os.getenv("TRELLO_TOKEN", "")
    LISTA_NOVOS_CLIENTES = os.getenv("TRELLO_LIST_NOVOS_CLIENTES_ID", "")

BASE_URL = "https://api.trello.com/1"


def _auth_params() -> Dict[str, str]:
    return {"key": API_KEY, "token": TOKEN}


def criar_cartao_cliente(nome_cliente: str, descricao: str, id_lista: Optional[str] = None) -> Dict[str, Any]:
    """
    Cria um novo cartão no Trello na lista de Onboarding.
    """
    target_list = id_lista or LISTA_NOVOS_CLIENTES
    if not API_KEY or not TOKEN or not target_list:
        return {"erro": "TRELLO_API_KEY, TRELLO_TOKEN ou TRELLO_LIST_NOVOS_CLIENTES_ID não configurados."}

    url = f"{BASE_URL}/cards"
    params = _auth_params()
    params.update({
        "idList": target_list,
        "name": f"🚀 Onboarding - {nome_cliente}",
        "desc": descricao,
        "pos": "top"
    })

    try:
        r = requests.post(url, params=params, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"erro": f"Erro ao criar cartão no Trello: {str(e)}"}


if __name__ == "__main__":
    print("Módulo de integração Trello carregado.")
