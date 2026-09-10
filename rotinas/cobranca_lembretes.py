#!/usr/bin/env python3
"""
rotinas/cobranca_lembretes.py — Automação de Lembrete de Cobranças em Atraso

Consulta faturas vencidas no Asaas e envia avisos amigáveis via WhatsApp para os clientes.
"""

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integracoes import asaas, evolution_api
from utils.formatadores import formatar_moeda_brl, formatar_telefone_whatsapp


def verificar_e_notificar_cobrancas_vencidas():
    """
    Busca faturas em atraso no Asaas e envia notificação de lembrete no WhatsApp.
    """
    print("🔍 Consultando cobranças pendentes/em atraso no Asaas...")
    faturas_atrasadas = asaas.listar_cobrancas_pendentes()

    if not faturas_atrasadas:
        print("✅ Nenhuma fatura em atraso encontrada.")
        return

    print(f"⚠️  Encontradas {len(faturas_atrasadas)} faturas pendentes.")

    for fatura in faturas_atrasadas:
        valor = float(fatura.get("value", 0.0))
        data_venc = fatura.get("dueDate", "")
        link_pagamento = fatura.get("invoiceUrl") or fatura.get("bankSlipUrl")
        customer_id = fatura.get("customer")

        # Exemplo de lógica de envio
        msg = f"""
Oi! Tudo bem? 

Identificamos que a fatura relativa à gestão de anúncios no valor de *{formatar_moeda_brl(valor)}* (Vencimento: {data_venc}) consta em aberto.

📄 *Link para Segunda Via / Pix:*
{link_pagamento}

Se você já realizou o pagamento, favor desconsiderar este aviso!
        """.strip()

        print(f"   - Fatura ID {fatura.get('id')}: {formatar_moeda_brl(valor)} (Vencimento: {data_venc})")
        # evolution_api.enviar_texto(telefone_cliente, msg)


if __name__ == "__main__":
    verificar_e_notificar_cobrancas_vencidas()
