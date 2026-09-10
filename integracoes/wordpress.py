#!/usr/bin/env python3
"""
integracoes/wordpress.py — Módulo Sanitizado para a WordPress REST API

Gerencia a criação e edição de posts, páginas, landing pages e atualização de URLs no WordPress.
"""

import os
import requests
from typing import Dict, Any, List, Optional

try:
    from config import Config
    WP_URL = Config.WP_URL
    WP_USER = Config.WP_USER
    WP_APP_PASSWORD = Config.WP_APP_PASSWORD
except ImportError:
    WP_URL = os.getenv("WP_URL", "").rstrip("/")
    WP_USER = os.getenv("WP_USER", "")
    WP_APP_PASSWORD = os.getenv("WP_APP_PASSWORD", "")


def _auth():
    return (WP_USER, WP_APP_PASSWORD)


def criar_atualizar_pagina_wp(titulo: str, conteudo: str, slug: str, status: str = "publish") -> Dict[str, Any]:
    """
    Cria ou atualiza uma página/landing page no WordPress.
    """
    if not WP_URL or not WP_USER or not WP_APP_PASSWORD:
        return {
            "erro": "WP_CONFIG_PENDENTE",
            "mensagem": "Configure WP_URL, WP_USER e WP_APP_PASSWORD no arquivo .env"
        }

    url = f"{WP_URL}/wp-json/wp/v2/pages"
    payload = {
        "title": titulo,
        "content": conteudo,
        "slug": slug,
        "status": status
    }

    try:
        r = requests.post(url, auth=_auth(), json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"erro": f"Erro na API do WordPress: {str(e)}"}


def listar_paginas_wp() -> List[Dict[str, Any]]:
    """
    Retorna a lista de páginas publicadas no WordPress com seus respetivos Slugs e IDs.
    """
    if not WP_URL:
        return []

    url = f"{WP_URL}/wp-json/wp/v2/pages"
    try:
        r = requests.get(url, params={"per_page": 20}, timeout=20)
        return r.json()
    except Exception:
        return []


if __name__ == "__main__":
    print("Módulo de integração WordPress REST API carregado.")
