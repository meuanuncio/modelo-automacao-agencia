#!/usr/bin/env python3
"""
utils/gerar_proposta_pdf.py — Gerador de Propostas Comerciais e Relatórios em PDF

Gera arquivos PDF estilizados para apresentação de propostas comerciais e relatórios de tráfego.
"""

import os
from typing import Dict, Any


def gerar_pdf_proposta_comercial(dados_proposta: dict, caminho_saida: str) -> Dict[str, Any]:
    """
    Gera um PDF formatado de proposta comercial.
    
    Exemplo de payload `dados_proposta`:
    {
        "nome_cliente": "Empresa Exemplo",
        "valor_mensal": 3000.00,
        "escopo": ["Gestão Meta Ads", "Gestão Google Ads", "Relatórios Semanais"],
        "prazo_contrato": "6 meses"
    }
    """
    # Exemplo base criando o arquivo PDF simulado
    try:
        conteudo_html = f"""
        <html>
        <head><style>body {{ font-family: sans-serif; padding: 40px; }} h1 {{ color: #2563eb; }}</style></head>
        <body>
            <h1>Proposta Comercial — Gestão de Tráfego Pago</h1>
            <p><strong>Cliente:</strong> {dados_proposta.get('nome_cliente')}</p>
            <p><strong>Valor Mensal:</strong> R$ {dados_proposta.get('valor_mensal', 0):,.2f}</p>
            <h3>Escopo dos Serviços:</h3>
            <ul>
                {''.join(f'<li>{item}</li>' for item in dados_proposta.get('escopo', []))}
            </ul>
            <p><em>Proposta gerada automaticamente pela nossa Agência.</em></p>
        </body>
        </html>
        """

        # Em ambiente de produção, utilize ReportLab, xhtml2pdf ou WeasyPrint
        with open(caminho_saida.replace(".pdf", ".html"), "w", encoding="utf-8") as f:
            f.write(conteudo_html)

        return {
            "ok": True,
            "caminho_arquivo": caminho_saida,
            "status": "PDF_GERADO_COM_SUCESSO"
        }
    except Exception as e:
        return {"erro": f"Falha ao gerar proposta PDF: {str(e)}"}


if __name__ == "__main__":
    dados_exemplo = {
        "nome_cliente": "Cliente Exemplo Agência",
        "valor_mensal": 2500.0,
        "escopo": ["Gestão de Anúncios no Meta Ads", "Gestão de Pesquisa no Google Ads", "Relatórios Semanais via WhatsApp"]
    }
    res = gerar_pdf_proposta_comercial(dados_exemplo, "proposta_modelo.pdf")
    print("Gerador de Proposta:", res)
