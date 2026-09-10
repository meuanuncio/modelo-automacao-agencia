#!/usr/bin/env python3
"""
integracoes/youtube.py — Módulo Sanitizado para a YouTube Data API v3

Permite publicar vídeos e Shorts automaticamente no canal do YouTube da agência ou do cliente.
"""

import os
from typing import Dict, Any, List, Optional

try:
    from config import Config
    YOUTUBE_API_KEY = Config.YOUTUBE_API_KEY
except ImportError:
    YOUTUBE_API_KEY = os.getenv("YOUTUBE_API_KEY", "")


def upload_video_youtube(caminho_video: str, titulo: str, descricao: str,
                         tags: Optional[List[str]] = None, categoria_id: str = "22") -> Dict[str, Any]:
    """
    Realiza o envio de um arquivo de vídeo para o YouTube via OAuth2 ou Service Account.
    
    :param caminho_video: Caminho local do vídeo em MP4
    :param titulo: Título do vídeo
    :param descricao: Descrição formatada com links/hashtags
    :param tags: Lista de tags do vídeo
    :param categoria_id: Categoria ('22' = People & Blogs, '28' = Science & Technology)
    """
    if not os.path.exists(caminho_video):
        return {"erro": f"Arquivo de vídeo não encontrado: {caminho_video}"}

    payload = {
        "snippet": {
            "title": titulo,
            "description": descricao,
            "tags": tags or ["gestao de trafego", "marketing digital"],
            "categoryId": categoria_id
        },
        "status": {
            "privacyStatus": "unlisted"  # 'public', 'private', ou 'unlisted'
        }
    }

    return {
        "ok": True,
        "payload_snippet": payload,
        "caminho_video": caminho_video,
        "mensagem": "Estrutura pronta para execução via googleapiclient.discovery (YouTube API v3)."
    }


if __name__ == "__main__":
    print("Módulo de integração YouTube API carregado.")
