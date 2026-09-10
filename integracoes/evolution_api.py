#!/usr/bin/env python3
"""
integracoes/evolution_api.py — Disparo de Mensagens WhatsApp via Evolution API

Módulo completo e sanitizado para enviar mensagens de texto, mídias e relatórios formatados
para números individuais ou grupos de clientes via Evolution API.
"""

import os
import requests
from typing import Dict, Any, Optional

try:
    from config import Config
    EVOLUTION_URL = Config.EVOLUTION_URL
    EVOLUTION_INSTANCE = Config.EVOLUTION_INSTANCE
    EVOLUTION_API_KEY = Config.EVOLUTION_API_KEY
except ImportError:
    EVOLUTION_URL = os.getenv("EVOLUTION_URL", "").rstrip("/")
    EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE", "comercial")
    EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")


def _headers() -> Dict[str, str]:
    """Retorna os cabeçalhos padrão para a requisição da Evolution API."""
    return {
        "Content-Type": "application/json",
        "apikey": EVOLUTION_API_KEY,
    }


def enviar_texto(numero_ou_grupo: str, mensagem: str, instancia: Optional[str] = None) -> Dict[str, Any]:
    """
    Envia uma mensagem de texto simples ou formatada no WhatsApp.
    
    :param numero_ou_grupo: Número com DDD no formato 5511999999999 ou Group ID (ex: 12036300000@g.us)
    :param mensagem: Texto da mensagem (suporta formatação Markdown do WhatsApp: *negrito*, _itálico_)
    :param instancia: Nome da instância Evolution (opcional, utiliza a definida no .env)
    """
    if not EVOLUTION_URL or not EVOLUTION_API_KEY:
        return {"erro": "EVOLUTION_URL ou EVOLUTION_API_KEY não configurados no .env"}

    inst = instancia or EVOLUTION_INSTANCE
    url = f"{EVOLUTION_URL}/message/sendText/{inst}"
    payload = {
        "number": numero_ou_grupo,
        "text": mensagem
    }

    try:
        r = requests.post(url, headers=_headers(), json=payload, timeout=30)
        r.raise_for_status()
        return r.json()
    except requests.exceptions.HTTPError as e:
        return {"erro": f"HTTP {e.response.status_code}: {e.response.text[:300]}"}
    except requests.exceptions.RequestException as e:
        return {"erro": f"Falha na requisição: {str(e)}"}


def enviar_relatorio_cliente(id_grupo: str, mensagem: str, instancia: Optional[str] = None) -> Dict[str, Any]:
    """
    Envia um relatório formatado para o grupo do WhatsApp do cliente.
    """
    if not id_grupo:
        return {"erro": "ID do grupo de destino não foi fornecido."}
    return enviar_texto(id_grupo, mensagem, instancia=instancia)


def enviar_midia(numero_ou_grupo: str, caminho_arquivo: str, mediatype: str = "document",
                 legenda: str = "", instancia: Optional[str] = None) -> Dict[str, Any]:
    """
    Envia um arquivo (PDF, imagem, documento) via WhatsApp.
    
    :param numero_ou_grupo: Número ou Group ID do destinatário
    :param caminho_arquivo: Caminho absoluto ou relativo para o arquivo local
    :param mediatype: Tipo da mídia ('document', 'image', 'video', 'audio')
    :param legenda: Legenda opcional para a imagem ou documento
    """
    if not os.path.exists(caminho_arquivo):
        return {"erro": f"Arquivo não encontrado no caminho: {caminho_arquivo}"}

    inst = instancia or EVOLUTION_INSTANCE
    url = f"{EVOLUTION_URL}/message/sendMedia/{inst}"
    
    # Exemplo base enviando como multipart/form-data ou payload codificado
    payload = {
        "number": numero_ou_grupo,
        "mediatype": mediatype,
        "caption": legenda,
        "fileName": os.path.basename(caminho_arquivo)
    }
    
    files = {
        'file': (os.path.basename(caminho_arquivo), open(caminho_arquivo, 'rb'))
    }
    
    headers = {"apikey": EVOLUTION_API_KEY}

    try:
        r = requests.post(url, headers=headers, data=payload, files=files, timeout=60)
        r.raise_for_status()
        return r.json()
    except Exception as e:
        return {"erro": f"Erro ao enviar mídia: {str(e)}"}


if __name__ == "__main__":
    print("Módulo de integração Evolution API (WhatsApp) carregado.")
