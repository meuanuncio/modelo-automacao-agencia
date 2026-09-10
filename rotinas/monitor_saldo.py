#!/usr/bin/env python3
"""
rotinas/monitor_saldo.py — Alerta de Saldo Pré-Pago no Meta Ads via WhatsApp

Verifica o saldo restante nas contas pré-pagas do Meta Ads e dispara um aviso
no WhatsApp da agência caso o valor fique abaixo do limite mínimo estipulado.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integracoes import meta_ads, evolution_api
from utils.formatadores import formatar_moeda_brl


def monitorar_saldo_contas(limite_minimo_reais: float = 100.0, grupo_alerta_whatsapp: str = ""):
    """
    Verifica o saldo de contas pré-pagas e envia alerta no WhatsApp caso o saldo seja crítico.
    """
    print(f"🔍 Monitorando saldo de contas pré-pagas (Limite Mínimo: {formatar_moeda_brl(limite_minimo_reais)})...")

    # Exemplo sanitizado de checagem de contas
    contas_exemplo = [
        {"account_id": "act_1001", "nome": "Cliente A", "saldo_reais": 45.00},
        {"account_id": "act_1002", "nome": "Cliente B", "saldo_reais": 350.00}
    ]

    for conta in contas_exemplo:
        saldo = conta["saldo_reais"]
        if saldo < limite_minimo_reais:
            alerta = f"""
🚨 *ALERTA DE SALDO CRÍTICO - META ADS*

📌 *Cliente:* {conta['nome']}
💰 *Saldo Atual:* {formatar_moeda_brl(saldo)}
⚠️ *Limite Mínimo:* {formatar_moeda_brl(limite_minimo_reais)}

_Favor solicitar o boleto/Pix de recarga para o cliente imediatamente para evitar a pausa dos anúncios!_
            """.strip()

            print(f"⚠️ Alerta gerado para {conta['nome']}: Saldo {formatar_moeda_brl(saldo)}")
            if grupo_alerta_whatsapp:
                evolution_api.enviar_texto(grupo_alerta_whatsapp, alerta)


if __name__ == "__main__":
    monitorar_saldo_contas(limite_minimo_reais=100.0)
