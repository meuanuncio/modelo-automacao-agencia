#!/usr/bin/env python3
"""
rotinas/monitor_orcamento.py — Alerta de Estouro de Orçamento Diário de Anúncios

Verifica o gasto diário acumulado das contas e avisa a equipe de tráfego caso
o investimento ultrapasse o teto planejado.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integracoes import meta_ads, evolution_api
from utils.formatadores import formatar_moeda_brl


def verificar_estouro_orcamento(teto_diario_reais: float = 500.0, grupo_alerta_whatsapp: str = ""):
    """
    Verifica o gasto diário das contas de anúncios contra o teto máximo permitido.
    """
    print(f"📈 Auditando investimento diário acumulado (Teto: {formatar_moeda_brl(teto_diario_reais)})...")

    gasto_atual = 540.50  # Valor simulado sanitizado

    if gasto_atual > teto_diario_reais:
        alerta = f"""
⚠️ *ALERTA DE ESTOURO DE ORÇAMENTO*

💰 *Gasto Hoje:* {formatar_moeda_brl(gasto_atual)}
🎯 *Teto Diário:* {formatar_moeda_brl(teto_diario_reais)}
📊 *Diferença:* +{formatar_moeda_brl(gasto_atual - teto_diario_reais)}

_Verifique os orçamentos das campanhas CBO/ABO para evitar que o limite diário seja ultrapassado._
        """.strip()

        print(f"⚠️ Alerta de orçamento disparado! Gasto: {formatar_moeda_brl(gasto_atual)}")
        if grupo_alerta_whatsapp:
            evolution_api.enviar_texto(grupo_alerta_whatsapp, alerta)


if __name__ == "__main__":
    verificar_estouro_orcamento()
