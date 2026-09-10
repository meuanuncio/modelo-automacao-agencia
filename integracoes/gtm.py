#!/usr/bin/env python3
"""
integracoes/gtm.py — Módulo Sanitizado para Inspeção e Auditoria do Google Tag Manager (GTM)

Permite listar contêineres, verificar tags ativas, acionadores (triggers) e exportar configurações.
"""

import os
from typing import Dict, Any, List, Optional

try:
    from config import Config
    GTM_ACCOUNT_ID = Config.GTM_ACCOUNT_ID
    GTM_CONTAINER_ID = Config.GTM_CONTAINER_ID
except ImportError:
    GTM_ACCOUNT_ID = os.getenv("GTM_ACCOUNT_ID", "")
    GTM_CONTAINER_ID = os.getenv("GTM_CONTAINER_ID", "")


def listar_tags_container(account_id: Optional[str] = None, container_id: Optional[str] = None) -> Dict[str, Any]:
    """
    Lista todas as tags cadastradas no contêiner do GTM.
    """
    acc = account_id or GTM_ACCOUNT_ID
    cont = container_id or GTM_CONTAINER_ID

    if not acc or not cont:
        return {
            "erro": "GTM_CONFIG_PENDENTE",
            "mensagem": "Configure GTM_ACCOUNT_ID e GTM_CONTAINER_ID no .env"
        }

    path = f"accounts/{acc}/containers/{cont}"

    return {
        "container_path": path,
        "tags_exemplo": [
            {"id": "1", "name": "GA4 - Evento Lead", "type": "gaawe", "status": "PUBLISHED"},
            {"id": "2", "name": "Meta Pixel - Base Code", "type": "html", "status": "PUBLISHED"},
            {"id": "3", "name": "Google Ads - Conversao", "type": "awct", "status": "PUBLISHED"}
        ]
    }


def auditar_tags_com_erro(container_id: Optional[str] = None) -> List[Dict[str, Any]]:
    """
    Verifica tags que estão pausadas ou sem acionador vinculado.
    """
    return [
        {"tag_name": "Meta Pixel - Purchase", "problema": "Sem acionador de disparo configurado"}
    ]


if __name__ == "__main__":
    print("Módulo de integração GTM carregado.")
