# Desafio MBA Engenharia de Software com IA - Full Cycle

Este projeto implementa um sistema RAG (Retrieval-Augmented Generation) capaz de responder perguntas baseadas no conteúdo de um arquivo PDF. O sistema utiliza LangChain para orquestrar o processo, Google Gemini para os modelos de linguagem (embeddings e geração de respostas) e PostgreSQL com a extensão pgVector para o armazenamento e busca dos dados vetoriais.

## Tecnologias Utilizadas

- **Linguagem**: Python
- **Framework**: LangChain
- **Banco de Dados**: PostgreSQL + pgVector
- **LLM**: Google Gemini (`gemini-2.5-flash-lite`)
- **Embeddings**: Google (`models/embedding-001`)
- **Containerização**: Docker & Docker Compose

## Pré-requisitos

- [Docker](https://www.docker.com/get-started) e [Docker Compose](https://docs.docker.com/compose/install/) instalados.
- [Python 3.9+](https://www.python.org/downloads/) instalado.
- Uma **chave de API do Google** para usar os modelos Gemini. Você pode obter uma no [Google AI Studio](https://aistudio.google.com/app/apikey).

## Passo a Passo para Execução

### 1. Clonar o Repositório

```bash
git clone https://github.com/Thiago-Cardoso/mba-ia-desafio-ingestao-busca.git
cd mba-ia-desafio-ingestao-busca
```

### 2. Configurar Variáveis de Ambiente

Crie um arquivo chamado `.env` na raiz do projeto. Você pode copiar o template `.env.example`.

```bash
cp .env.example .env
```

Agora, abra o arquivo `.env` e preencha as variáveis com seus próprios valores:

```env
# Sua chave de API do Google
GOOGLE_API_KEY="SUA_CHAVE_API_AQUI"

# Caminho para o arquivo PDF que será ingerido
PDF_PATH="document.pdf"

# Modelo de embedding do Google
GOOGLE_EMBEDDING_MODEL="models/embedding-001"

# URL de conexão com o banco de dados PostgreSQL
DATABASE_URL="postgresql+psycopg://postgres:postgres@localhost:5433/rag"

# Nome da coleção (tabela) no banco de dados vetorial
PG_VECTOR_COLLECTION_NAME="rag_collection"
```
**Observação**: Certifique-se de que o arquivo PDF (`document.pdf` ou outro de sua escolha) esteja na raiz do projeto.

### 3. Iniciar o Banco de Dados com Docker

Com o Docker em execução, suba o container do PostgreSQL com a extensão pgVector.

```bash
docker-compose up -d
```
Este comando irá:
- Baixar a imagem do `pgvector`.
- Criar e iniciar um container chamado `postgres_rag`.
- Configurar o banco de dados `rag` com o usuário e senha `postgres`.
- Habilitar a extensão `vector` automaticamente após o banco de dados ficar pronto.

Para verificar se o banco de dados está rodando corretamente, execute:
```bash
docker ps
```

### 4. Instalar as Dependências Python

É altamente recomendado criar um ambiente virtual para isolar as dependências do projeto.

```bash
# Criar o ambiente virtual
python -m venv venv

# Ativar o ambiente virtual
# No macOS/Linux:
source venv/bin/activate
# No Windows:
.\\venv\\Scripts\\activate

# Instalar as dependências
pip install -r requirements.txt
```

### 5. Ingestão dos Dados do PDF

Com o banco de dados rodando e as dependências instaladas, execute o script de ingestão para processar o PDF e armazenar os vetores no banco.

```bash
python src/ingest.py
```
O script irá carregar o PDF, dividi-lo em `chunks`, gerar os `embeddings` para cada `chunk` e salvá-los no PostgreSQL.

### 6. Executar o Chat Interativo

Após a ingestão, você pode iniciar o chat para fazer perguntas sobre o conteúdo do documento.

```bash
python src/chat.py
```

O terminal ficará aguardando suas perguntas. Para encerrar, digite `sair`.

**Exemplo de interação:**
```
=== Sistema de Ingestão e Busca Semântica com LangChain ===
Digite 'sair' para encerrar o chat

Faça sua pergunta: Qual o faturamento da Empresa Alfa Energia Holding?
RESPOSTA: R$ 858.537,02.

Faça sua pergunta: Qual o ano de fundação da empresa Alfa Energia Holding?
RESPOSTA: 1971

Faça sua pergunta: Quantos clientes tem a empresa Aurora Eventos ME?
RESPOSTA: Não tenho informações necessárias para responder sua pergunta.
---
```

## Estrutura do Projeto

```
├── docker-compose.yml      # Configuração do container do PostgreSQL
├── requirements.txt        # Dependências do projeto Python
├── .env.example            # Template para as variáveis de ambiente
├── src/
│   ├── ingest.py           # Script para ingestão e vetorização do PDF
│   ├── search.py           # Lógica de busca semântica e geração de resposta
│   └── chat.py             # CLI para interação com o usuário
├── document.pdf            # Documento base para o sistema de perguntas e respostas
└── README.md               # Este arquivo
```