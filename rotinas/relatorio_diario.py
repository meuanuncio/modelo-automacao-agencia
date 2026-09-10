#!/usr/bin/env python3
"""
rotinas/relatorio_diario.py — Envio Diário/Semanal de Relatório de Métricas no WhatsApp

Busca o investimento e os resultados do Meta Ads do mês vigente e envia um resumo
formatado para o grupo de WhatsApp do cliente.
"""

import sys
import os
from datetime import datetime

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integracoes import meta_ads, evolution_api
from utils.formatadores import formatar_moeda_brl, formatar_porcentagem


def enviar_resumo_desempenho_cliente(account_id: str, id_grupo_whatsapp: str, nome_cliente: str):
    """
    Gera e envia o relatório consolidado de anúncios para o cliente.
    """
    hoje = datetime.now()
    since = hoje.replace(day=1).strftime("%Y-%m-%d")
    until = hoje.strftime("%Y-%m-%d")

    print(f"📊 Gerando relatório para {nome_cliente} ({since} a {until})...")
    metricas = meta_ads.obter_metricas_conta(account_id, since, until)

    if "erro" in metricas:
        print(f"❌ Erro ao obter métricas: {metricas['erro']}")
        return

    relatorio_txt = f"""
📊 *Relatório de Desempenho de Anúncios — {nome_cliente}*
🗓️ *Período:* {since} a {until}

💰 *Investimento Total:* {formatar_moeda_brl(metricas['investimento'])}
🎯 *Leads Gerados:* {metricas['leads']}
📉 *Custo por Lead (CPL):* {formatar_moeda_brl(metricas['cpl'])}

👁️ *Impressões:* {metricas['impressoes']:,}
🖱️ *Cliques no Anúncio:* {metricas['cliques']:,}
🔗 *Taxa de Cliques (CTR):* {formatar_porcentagem(metricas['ctr_porcentagem'])}

---
_Relatório gerado automaticamente pela nossa Gestão de Anúncios._
    """.strip()

    print("\n--- Mensagem Formatada para Envio ---")
    print(relatorio_txt)
    print("------------------------------------\n")

    # Descomente a linha abaixo para enviar no grupo do cliente
    # res = evolution_api.enviar_relatorio_cliente(id_grupo_whatsapp, relatorio_txt)
    # print("Resultado do envio no WhatsApp:", res)


if __name__ == "__main__":
    # Teste sanitizado
    enviar_resumo_desempenho_cliente(
        account_id="act_123456789",
        id_grupo_whatsapp="120363000000000000@g.us",
        nome_cliente="Cliente Exemplo"
    )
