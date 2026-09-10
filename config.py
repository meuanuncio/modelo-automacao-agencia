#!/usr/bin/env python3
"""
config.py — Gerenciador Central de Configurações da Agência
Carrega e valida as variáveis de ambiente a partir do arquivo .env.
"""

import os
import sys
from dotenv import load_dotenv

# Carrega as variáveis contidas no arquivo .env
load_dotenv()


class Config:
    """Classe para centralizar o acesso às variáveis de ambiente da aplicação."""

    # Configurações Gerais
    NOME_AGENCIA = os.getenv("NOME_AGENCIA", "Minha Agência de Tráfego")
    EMAIL_AGENCIA = os.getenv("EMAIL_NOTIFICACAO_AGENCIA", "contato@suaagencia.com.br")
    GRUPO_ALERTAS_WHATSAPP = os.getenv("GRUPO_WHATSAPP_ALERTAS_INTERNOS", "")

    # Meta Ads
    META_ACCESS_TOKEN = os.getenv("META_ACCESS_TOKEN", "")
    META_ACCOUNT_ID = os.getenv("META_ACCOUNT_ID", "")
    META_BUSINESS_ID = os.getenv("META_BUSINESS_ID", "")
    META_GRAPH_VERSION = "v21.0"
    META_BASE_URL = f"https://graph.facebook.com/{META_GRAPH_VERSION}"

    # Google Ads
    GOOGLE_ADS_DEVELOPER_TOKEN = os.getenv("GOOGLE_ADS_DEVELOPER_TOKEN", "")
    GOOGLE_ADS_CLIENT_ID = os.getenv("GOOGLE_ADS_CLIENT_ID", "")
    GOOGLE_ADS_CLIENT_SECRET = os.getenv("GOOGLE_ADS_CLIENT_SECRET", "")
    GOOGLE_ADS_REFRESH_TOKEN = os.getenv("GOOGLE_ADS_REFRESH_TOKEN", "")
    GOOGLE_ADS_CUSTOMER_ID = os.getenv("GOOGLE_ADS_CUSTOMER_ID", "")

    # Evolution API (WhatsApp)
    EVOLUTION_URL = os.getenv("EVOLUTION_URL", "").rstrip("/")
    EVOLUTION_INSTANCE = os.getenv("EVOLUTION_INSTANCE", "comercial")
    EVOLUTION_API_KEY = os.getenv("EVOLUTION_API_KEY", "")

    # Asaas (Cobranças)
    ASAAS_API_KEY_PROD = os.getenv("ASAAS_API_KEY_PROD", "")
    ASAAS_API_KEY_SANDBOX = os.getenv("ASAAS_API_KEY_SANDBOX", "")
    ASAAS_SANDBOX = os.getenv("ASAAS_SANDBOX", "True").lower() in ("true", "1", "yes")
    ASAAS_WALLET_ID = os.getenv("ASAAS_WALLET_ID", "")

    # Autentique (Contratos)
    AUTENTIQUE_TOKEN = os.getenv("AUTENTIQUE_TOKEN", "")
    AUTENTIQUE_SANDBOX = os.getenv("AUTENTIQUE_SANDBOX", "True").lower() in ("true", "1", "yes")

    # Trello
    TRELLO_API_KEY = os.getenv("TRELLO_API_KEY", "")
    TRELLO_TOKEN = os.getenv("TRELLO_TOKEN", "")
    TRELLO_BOARD_ONBOARDING_ID = os.getenv("TRELLO_BOARD_ONBOARDING_ID", "")
    TRELLO_LIST_NOVOS_CLIENTES_ID = os.getenv("TRELLO_LIST_NOVOS_CLIENTES_ID", "")

    @classmethod
    def validar_configuracoes_basicas(cls) -> bool:
        """
        Verifica se as configurações mínimas essenciais foram preenchidas.
        Retorna True se estiver tudo ok, ou imprime os avisos de pendência.
        """
        pendencias = []
        if not cls.META_ACCESS_TOKEN:
            pendencias.append("META_ACCESS_TOKEN não configurado no .env")
        if not cls.EVOLUTION_URL or not cls.EVOLUTION_API_KEY:
            pendencias.append("EVOLUTION_URL ou EVOLUTION_API_KEY não configurados no .env")

        if pendencias:
            print("⚠️  Aviso de Configuração Pendente:")
            for item in pendencias:
                print(f"   - {item}")
            return False
        
        print("✅ Configurações básicas validadas com sucesso.")
        return True


if __name__ == "__main__":
    Config.validar_configuracoes_basicas()
