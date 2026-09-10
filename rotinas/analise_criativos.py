#!/usr/bin/env python3
"""
rotinas/analise_criativos.py — Ranking e Análise de Performance de Criativos

Algoritmo que analisa o desempenho dos anúncios ativas (CPL, CTR, ROAS, Retenção 3s)
e classifica os criativos campeões (Top Performers).
"""

import sys
import os
from typing import List, Dict, Any

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.formatadores import formatar_moeda_brl, formatar_porcentagem


def ranquear_criativos_campeoes(anuncios: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Ranqueia os anúncios com base no CPL (Custo por Lead) e CTR (Taxa de Cliques).
    """
    # Ordena pelo CPL mais baixo (do menor para o maior)
    criativos_ordenados = sorted(
        anuncios,
        key=lambda x: (x.get("cpl", 9999), -x.get("ctr", 0))
    )
    return criativos_ordenados


def gerar_relatorio_top_criativos(anuncios: List[Dict[str, Any]]) -> str:
    """
    Formata o ranking de criativos campeões para envio em relatórios.
    """
    ranking = ranquear_criativos_campeoes(anuncios)
    
    linhas = ["🏆 *RANKING DOS MELHORES CRIATIVOS (TOP PERFORMERS)*\n"]
    for i, item in enumerate(ranking[:5], 1):
        linhas.append(
            f"{i}️⃣ *{item['nome_anuncio']}*\n"
            f"   💰 Investimento: {formatar_moeda_brl(item['spend'])}\n"
            f"   🎯 Leads: {item['leads']} | 📉 CPL: {formatar_moeda_brl(item['cpl'])}\n"
            f"   🖱️ CTR: {formatar_porcentagem(item['ctr'])}\n"
        )

    return "\n".join(linhas)


if __name__ == "__main__":
    exemplo_anuncios = [
        {"nome_anuncio": "Ad 01 - Reel Depoimento", "spend": 450.0, "leads": 25, "cpl": 18.0, "ctr": 2.45},
        {"nome_anuncio": "Ad 02 - Carrossel Benefícios", "spend": 300.0, "leads": 12, "cpl": 25.0, "ctr": 1.80},
        {"nome_anuncio": "Ad 03 - Foto Oferta Direta", "spend": 500.0, "leads": 35, "cpl": 14.28, "ctr": 3.10}
    ]

    print(gerar_relatorio_top_criativos(exemplo_anuncios))
