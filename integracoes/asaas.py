#!/usr/bin/env python3
"""
integracoes/asaas.py — Gestão de Cobranças e Clientes no Asaas

Permite buscar/cadastrar clientes, gerar cobranças pontuais e recorrentes (Boleto/PIX)
e consultar faturas pendentes ou em atraso.
"""

import os
import requests
from typing import Dict, Any, Optional, List

try:
    from config import Config
    API_KEY_PROD = Config.ASAAS_API_KEY_PROD
    API_KEY_SANDBOX = Config.ASAAS_API_KEY_SANDBOX
    IS_SANDBOX = Config.ASAAS_SANDBOX
except ImportError:
    API_KEY_PROD = os.getenv("ASAAS_API_KEY_PROD", "")
    API_KEY_SANDBOX = os.getenv("ASAAS_API_KEY_SANDBOX", "")
    IS_SANDBOX = True

BASE_URL_PROD = "https://api.asaas.com/v3"
BASE_URL_SANDBOX = "https://api-sandbox.asaas.com/v3"


def _config(sandbox: Optional[bool] = None):
    use_sandbox = IS_SANDBOX if sandbox is None else sandbox
    base_url = BASE_URL_SANDBOX if use_sandbox else BASE_URL_PROD
    api_key = API_KEY_SANDBOX if use_sandbox else API_KEY_PROD
    headers = {
        "access_token": api_key,
        "Content-Type": "application/json",
        "User-Agent": "modelo-automacao-agencia"
    }
    return base_url, headers


def _request(method: str, path: str, sandbox: Optional[bool] = None, **kwargs) -> Dict[str, Any]:
    base_url, headers = _config(sandbox)
    try:
        resp = requests.request(method, f"{base_url}{path}", headers=headers, timeout=30, **kwargs)
        data = resp.json()
    except Exception as e:
        return {"error": str(e)}

    if resp.status_code >= 400:
        return {"error": data}
    return data


def buscar_cliente_por_cpf_cnpj(cpf_cnpj: str, sandbox: Optional[bool] = None) -> Optional[Dict[str, Any]]:
    """Busca um cliente já cadastrado no Asaas pelo CPF/CNPJ."""
    resp = _request("GET", "/customers", sandbox=sandbox, params={"cpfCnpj": cpf_cnpj})
    if "error" in resp:
        return None
    itens = resp.get("data", [])
    return itens[0] if itens else None


def criar_cliente(nome: str, cpf_cnpj: str, email: str = "", telefone: str = "", sandbox: Optional[bool] = None) -> Dict[str, Any]:
    """Cria um novo cadastro de cliente no Asaas."""
    existente = buscar_cliente_por_cpf_cnpj(cpf_cnpj, sandbox=sandbox)
    if existente:
        return existente

    payload = {
        "name": nome,
        "cpfCnpj": cpf_cnpj,
        "email": email,
        "phone": telefone
    }
    return _request("POST", "/customers", sandbox=sandbox, json=payload)


def criar_cobranca(customer_id: str, valor: float, data_vencimento: str, descricao: str = "Mensalidade Gestao de Trafego",
                   billing_type: str = "UNDEFINED", sandbox: Optional[bool] = None) -> Dict[str, Any]:
    """
    Gera uma cobrança no Asaas.
    
    :param billing_type: 'BOLETO', 'CREDIT_CARD', 'PIX', ou 'UNDEFINED' (deixa o cliente escolher)
    """
    payload = {
        "customer": customer_id,
        "billingType": billing_type,
        "value": valor,
        "dueDate": data_vencimento,
        "description": descricao
    }
    return _request("POST", "/payments", sandbox=sandbox, json=payload)


def listar_cobrancas_pendentes(sandbox: Optional[bool] = None) -> List[Dict[str, Any]]:
    """Retorna lista de cobranças que estão pendentes ou em atraso (OVERDUE)."""
    resp = _request("GET", "/payments", sandbox=sandbox, params={"status": "OVERDUE"})
    if "error" in resp:
        return []
    return resp.get("data", [])


if __name__ == "__main__":
    print("Módulo de integração Asaas carregado.")
