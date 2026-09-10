# 🚀 Template de Automação para Agências de Tráfego e Performance

Este repositório é um **modelo/template base sanitizado** projetado para auxiliar agências na montagem de suas estruturas de automação comercial, criação e gestão de campanhas de anúncios, onboarding de clientes, disparo de faturas, monitoramento de saldo e relatórios automatizados via WhatsApp.

---

## 🛠️ Arquitetura do Projeto

O projeto está organizado de forma totalmente modular:

```text
modelo-automacao-agencia/
├── .env.example              # Modelo de variáveis de ambiente (sem segredos)
├── .gitignore                # Regras de proteção para arquivos sensíveis e tokens
├── requirements.txt          # Dependências do Python
├── config.py                 # Carregador central de configurações (.env)
│
├── integracoes/              # Módulos isolados de APIs externas
│   ├── __init__.py
│   ├── meta_ads.py           # Meta Ads API (Métricas, Criação de Campanhas/Ads e URLs)
│   ├── google_ads.py         # Google Ads API (Relatórios GAQL e Campanhas Search)
│   ├── ga4.py                # GA4 Data API (Métricas de Tráfego, Conversões, UTMs)
│   ├── gtm.py                # Google Tag Manager API (Inspeção de Contêineres/Tags)
│   ├── google_business.py    # Google Meu Negócio API (Reviews, Locais, Métricas)
│   ├── linkedin_ads.py       # LinkedIn Ads API (Métricas B2B e Campanhas)
│   ├── tiktok_ads.py         # TikTok Business API (Upload de Vídeos e Métricas)
│   ├── youtube.py            # YouTube Data API v3 (Upload de Vídeos e Shorts)
│   ├── wordpress.py          # WordPress REST API (Gestão de Páginas e Posts)
│   ├── typebot.py            # Typebot API (Qualificação de Leads MQL)
│   ├── evolution_api.py      # WhatsApp API (Mensagens de Texto, PDFs, Mídias)
│   ├── asaas.py              # Asaas API (Cobranças Recorrentes, PIX, Clientes)
│   ├── autentique.py         # Autentique API (Assinatura Digital de Contratos)
│   └── trello.py             # Trello API (Kanban de Onboarding / Suporte)
│
├── rotinas/                  # Workflows completos de automação
│   ├── __init__.py
│   ├── onboarding_cliente.py # Workflow: Cadastro + Contrato + Trello + Boas-vindas
│   ├── cobranca_lembretes.py # Workflow: Consulta de faturas em atraso e avisos
│   ├── relatorio_diario.py   # Workflow: Coleta de métricas e envio no WhatsApp
│   ├── monitor_saldo.py      # Workflow: Alerta de saldo pré-pago no Meta Ads
│   ├── monitor_orcamento.py  # Workflow: Alerta de estouro de orçamento diário
│   ├── analise_criativos.py  # Workflow: Ranking dos criativos mais lucrativos (ROAS, CPL)
│   └── kw_manager.py         # Workflow: Negativação em lote no Google Ads
│
└── utils/                    # Utilitários de apoio
    ├── __init__.py
    ├── formatadores.py       # Formatação de moeda BRL, telefones e porcentagens
    └── gerar_proposta_pdf.py # Gerador de propostas e relatórios em PDF
```

---

## 🔒 Segurança e Boas Práticas (LGPD & Tokens)

1. **Variáveis de Ambiente (`.env`):**
   * Nenhuma chave de API, token ou senha está gravada no código fonte.
   * Copie o arquivo `.env.example` para `.env` e preencha com as suas credenciais.
   * O arquivo `.env` **nunca deve ser commitado no Git**.

2. **Isolamento de Dados de Clientes:**
   * Nenhum dado de cliente (CPF, CNPJ, telefone, relatório em PDF ou histórico de faturas) deve ser persistido em código ou repositório público/compartilhado.

---

## ⚡ Como Configurar e Executar

### 1. Clonar o Repositório e Instalar Dependências
```bash
git clone https://github.com/meuanuncio/modelo-automacao-agencia.git
cd modelo-automacao-agencia

# Criar e ativar ambiente virtual Python
python -m venv venv
# No Windows:
venv\Scripts\activate
# No Linux/Mac:
source venv/bin/activate

# Instalar dependências
pip install -r requirements.txt
```

### 2. Configurar o `.env`
```bash
cp .env.example .env
```
Edite o arquivo `.env` fornecendo seus tokens de acesso conforme documentado no arquivo.

### 3. Validar a Configuração
Rode o script central para verificar se há pendências de configuração:
```bash
python config.py
```

---

## 📝 Como Adaptar para a Sua Agência

* **Com qualquer IA (Claude Code, Antigravity, Codex, Freebuff):**
  Basta abrir uma sessão com o seu assistente de código e solicitar:
  > *"Clone o repositório https://github.com/meuanuncio/modelo-automacao-agencia e me ajude a configurar o `.env` e personalizar as rotinas para a minha agência."*

---
*Template criado para fins de treinamento e mentoria em automações de tráfego pago.*
