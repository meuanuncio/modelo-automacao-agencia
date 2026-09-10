#!/usr/bin/env python3
"""
rotinas/onboarding_cliente.py — Workflow de Boas-vindas e Entradas de Novos Clientes

Exemplo de automação completa que orquestra:
1. Cadastro do cliente no Asaas (para faturamento/cobrança).
2. Envio de contrato de prestação de serviços no Autentique para assinatura digital.
3. Criação de cartão de Onboarding na lista do Trello da equipe.
4. Envio de mensagem de boas-vindas e orientações de onboarding via WhatsApp.
"""

import sys
import os

# Permite importação dos módulos da pasta integracoes
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from integracoes import asaas, autentique, trello, evolution_api
from utils.formatadores import formatar_telefone_whatsapp


def executar_onboarding_novo_cliente(dados_cliente: dict) -> dict:
    """
    Executa o fluxo completo de entrada de um novo cliente na agência.
    
    Exemplo de payload `dados_cliente`:
    {
        "nome": "Empresa Exemplo LTDA",
        "cpf_cnpj": "12345678000199",
        "email": "contato@empresaexemplo.com.br",
        "telefone": "11999998888",
        "valor_mensalidade": 2500.00,
        "caminho_contrato_pdf": "caminhos/contrato_modelo.pdf",
        "id_grupo_whatsapp": "120363000000000000@g.us"
    }
    """
    relatorio_execucao = {"cliente": dados_cliente.get("nome"), "etapas": {}}

    print(f"🚀 Iniciando Onboarding para o cliente: {dados_cliente.get('nome')}")

    # 1. Cadastrar no Asaas
    res_asaas = asaas.criar_cliente(
        nome=dados_cliente["nome"],
        cpf_cnpj=dados_cliente["cpf_cnpj"],
        email=dados_cliente.get("email"),
        telefone=dados_cliente.get("telefone")
    )
    relatorio_execucao["etapas"]["asaas"] = res_asaas
    print("   [1/4] Cadastro no Asaas concluído.")

    # 2. Criar Card no Trello para a Equipe de Tráfego/Onboarding
    desc_trello = f"""
    **Cliente:** {dados_cliente['nome']}
    **CNPJ/CPF:** {dados_cliente['cpf_cnpj']}
    **Email:** {dados_cliente.get('email')}
    **Valor Contratado:** R$ {dados_cliente.get('valor_mensalidade', 0):,.2f}
    """
    res_trello = trello.criar_cartao_cliente(
        nome_cliente=dados_cliente["nome"],
        descricao=desc_trello
    )
    relatorio_execucao["etapas"]["trello"] = res_trello
    print("   [2/4] Cartão no Trello criado.")

    # 3. Enviar Contrato no Autentique (Se fornecido o PDF)
    if dados_cliente.get("caminho_contrato_pdf") and os.path.exists(dados_cliente["caminho_contrato_pdf"]):
        signatarios = [
            {"email": dados_cliente["email"], "action": "SIGN"}
        ]
        res_autentique = autentique.criar_documento_para_assinatura(
            titulo=f"Contrato Gestão de Tráfego - {dados_cliente['nome']}",
            caminho_pdf=dados_cliente["caminho_contrato_pdf"],
            signatarios=signatarios
        )
        relatorio_execucao["etapas"]["autentique"] = res_autentique
        print("   [3/4] Contrato enviado para assinatura digital.")
    else:
        print("   [3/4] PDF de contrato não informado ou não encontrado. Etapa ignorada.")

    # 4. Enviar Mensagem de Boas-Vindas no WhatsApp
    num_wa = formatar_telefone_whatsapp(dados_cliente.get("telefone", ""))
    msg_boas_vindas = f"""
🎉 *Seja muito bem-vindo(a) à nossa Agência!*

Estamos muito felizes em iniciar nossa parceria com a *{dados_cliente['nome']}*.

📌 *Próximos Passos:*
1️⃣ Enviamos o contrato de prestação de serviços para o e-mail: _{dados_cliente.get('email')}_
2️⃣ Em breve enviaremos o formulário de Onboarding para alinhamento dos acessos às contas de anúncios.

Qualquer dúvida, estamos à disposição!
    """.strip()

    if num_wa:
        res_wa = evolution_api.enviar_texto(num_wa, msg_boas_vindas)
        relatorio_execucao["etapas"]["whatsapp"] = res_wa
        print("   [4/4] Mensagem de boas-vindas enviada no WhatsApp.")

    print("✅ Fluxo de Onboarding finalizado com sucesso!")
    return relatorio_execucao


if __name__ == "__main__":
    # Exemplo de teste sanitizado
    cliente_exemplo = {
        "nome": "Cliente Exemplo Agência",
        "cpf_cnpj": "00.000.000/0001-00",
        "email": "contato@clienteexemplo.com.br",
        "telefone": "(11) 99999-8888",
        "valor_mensalidade": 2000.00
    }
    print("Testando script de onboarding (modo estrutura)...")
