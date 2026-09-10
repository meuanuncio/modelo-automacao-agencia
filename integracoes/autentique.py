#!/usr/bin/env python3
"""
integracoes/autentique.py — Assinatura Digital de Contratos via Autentique GraphQL API

Permite enviar minutas de contrato em PDF para que o cliente e a agência
assinem digitalmente.
"""

import os
import requests
from typing import Dict, Any, List, Optional

try:
    from config import Config
    AUTENTIQUE_TOKEN = Config.AUTENTIQUE_TOKEN
    IS_SANDBOX = Config.AUTENTIQUE_SANDBOX
except ImportError:
    AUTENTIQUE_TOKEN = os.getenv("AUTENTIQUE_TOKEN", "")
    IS_SANDBOX = True

URL_GRAPHQL = "https://api.autentique.com.br/v2/graphql"


def criar_documento_para_assinatura(titulo: str, caminho_pdf: str, signatarios: List[Dict[str, str]], sandbox: Optional[bool] = None) -> Dict[str, Any]:
    """
    Envia um arquivo PDF para o Autentique para coletar assinaturas.
    
    :param titulo: Nome do documento exibido para os signatários
    :param caminho_pdf: Caminho local para o PDF do contrato
    :param signatarios: Lista de dicts ex: [{'email': 'cliente@empresa.com', 'action': 'SIGN'}]
    """
    if not os.path.exists(caminho_pdf):
        return {"erro": f"Arquivo PDF não encontrado: {caminho_pdf}"}

    use_sandbox = IS_SANDBOX if sandbox is None else sandbox
    sandbox_flag = "true" if use_sandbox else "false"

    # Query GraphQL da API do Autentique
    query = """
    mutation CreateDocumentMutation(
        $document: DocumentInput!,
        $signers: [SignerInput]!,
        $file: Upload!
    ) {
        createDocument(
            sandbox: """ + sandbox_flag + """,
            document: $document,
            signers: $signers,
            file: $file
        ) {
            id
            name
            created_at
        }
    }
    """

    operations = {
        "query": query,
        "variables": {
            "document": {"name": titulo},
            "signers": signatarios,
            "file": None
        }
    }

    map_file = {"0": ["variables.file"]}

    headers = {
        "Authorization": f"Bearer {AUTENTIQUE_TOKEN}"
    }

    try:
        with open(caminho_pdf, "rb") as f:
            files = {
                "operations": (None, requests.compat.json.dumps(operations), "application/json"),
                "map": (None, requests.compat.json.dumps(map_file), "application/json"),
                "0": (os.path.basename(caminho_pdf), f, "application/pdf")
            }
            response = requests.post(URL_GRAPHQL, headers=headers, files=files, timeout=60)
            return response.json()
    except Exception as e:
        return {"erro": f"Falha ao enviar contrato para o Autentique: {str(e)}"}


if __name__ == "__main__":
    print("Módulo de integração Autentique carregado.")
