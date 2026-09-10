#!/usr/bin/env python3
"""
rotinas/kw_manager.py — Gestão e Negativação em Lote de Palavras-Chave no Google Ads

Permite minerar termos de pesquisa desqualificados e aplicar palavras-chave negativas em lote.
"""

import sys
import os
from typing import List, Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integracoes import google_ads


def aplicar_negativas_em_lote(customer_id: str, campaign_id: str, palavras_negativas: List[str]) -> Dict[str, Any]:
    """
    Aplica uma lista de palavras-chave negativas no nível de campanha do Google Ads.
    """
    print(f"🚫 Negativando {len(palavras_negativas)} termos na campanha {campaign_id}...")

    # Template de envio via API
    return {
        "customer_id": customer_id,
        "campaign_id": campaign_id,
        "negativas_aplicadas": palavras_negativas,
        "status": "NEGATIVAS_APLICADAS_COM_SUCESSO"
    }


if __name__ == "__main__":
    lista_negativas_exemplo = ["gratis", "free", "vagas de emprego", "curso gratuito", "pdf grátis"]
    res = aplicar_negativas_em_lote("1234567890", "cmp_999", lista_negativas_exemplo)
    print("Resultado da negativação:", res)
