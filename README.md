# 🚀 Template de Automação para Agências de Tráfego e Performance

Este repositório é um **modelo/template base sanitizado** projetado para auxiliar agências na montagem de suas estruturas de automação comercial, onboarding de clientes, disparo de faturas e relatórios automatizados de tráfego pago via WhatsApp.

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
│   ├── meta_ads.py           # Meta Ads Graph API (Métricas, Anúncios, Criativos)
│   ├── google_ads.py         # Google Ads API (Relatórios GAQL, Orçamentos)
│   ├── evolution_api.py      # WhatsApp API (Mensagens de Texto, PDFs, Mídias)
│   ├── asaas.py              # Asaas API (Cobranças Recorrentes, PIX, Clientes)
│   ├── autentique.py         # Autentique API (Assinatura Digital de Contratos)
│   └── trello.py             # Trello API (Kanban de Onboarding / Suporte)
│
├── rotinas/                  # Workflows completos de automação
│   ├── __init__.py
│   ├── onboarding_cliente.py # Workflow: Cadastro + Contrato + Trello + Boas-vindas
│   ├── cobranca_lembretes.py # Workflow: Consulta de faturas em atraso e avisos
│   └── relatorio_diario.py   # Workflow: Coleta de métricas e envio no WhatsApp
│
└── utils/                    # Utilitários de apoio
    ├── __init__.py
    └── formatadores.py       # Formatação de moeda BRL, telefones e porcentagens
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
git clone <URL_DO_SEU_REPOSITORIO>
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
Edite o arquivo `.env` fornecendo seus tokens de acesso:
* **Meta Ads:** `META_ACCESS_TOKEN`, `META_ACCOUNT_ID`
* **Evolution API:** `EVOLUTION_URL`, `EVOLUTION_API_KEY`, `EVOLUTION_INSTANCE`
* **Asaas:** `ASAAS_API_KEY_PROD` ou `ASAAS_API_KEY_SANDBOX`
* **Autentique:** `AUTENTIQUE_TOKEN`
* **Trello:** `TRELLO_API_KEY`, `TRELLO_TOKEN`, `TRELLO_LIST_NOVOS_CLIENTES_ID`

### 3. Validar a Configuração
Rode o script central para verificar se há pendências de configuração:
```bash
python config.py
```

### 4. Executar os Workflows de Exemplo
* **Onboarding de Novo Cliente:**
  ```bash
  python rotinas/onboarding_cliente.py
  ```
* **Lembrete de Cobranças Vencidas:**
  ```bash
  python rotinas/cobranca_lembretes.py
  ```
* **Relatório no WhatsApp:**
  ```bash
  python rotinas/relatorio_diario.py
  ```

---

## 📝 Como Adaptar para a Sua Agência

* **Para alterar a linguagem das mensagens:** Modifique os templates de texto dentro de `rotinas/onboarding_cliente.py` e `rotinas/relatorio_diario.py`.
* **Para adicionar novas integrações (ex: CRM, RD Station, ActiveCampaign):** Crie um novo módulo em `integracoes/seu_crm.py` seguindo a mesma estrutura com `requests`.
* **Para agendar a execução automática:** Você pode configurar o Windows Task Scheduler ou Cron (Linux/VPS) para executar os scripts da pasta `rotinas/` em horários fixos.

---
*Template criado para fins de treinamento e mentoria em automações de tráfego pago.*
