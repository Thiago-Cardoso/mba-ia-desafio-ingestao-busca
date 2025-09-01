import os
from dotenv import load_dotenv
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain_postgres.vectorstores import PGVector
from langchain.prompts import PromptTemplate

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- Nunca invente ou use conhecimento externo.
- Nunca produza opiniões ou interpretações além do que está escrito.

EXEMPLOS DE PERGUNTAS FORA DO CONTEXTO:
Pergunta: "Qual é a capital da França?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Quantos clientes temos em 2024?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

Pergunta: "Você acha isso bom ou ruim?"
Resposta: "Não tenho informações necessárias para responder sua pergunta."

PERGUNTA DO USUÁRIO:
{pergunta}

RESPONDA A "PERGUNTA DO USUÁRIO"
"""

def get_vector_store():
    embeddings = GoogleGenerativeAIEmbeddings(
        model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"),
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )

    connection_string = os.getenv("DATABASE_URL")
    collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME", "rag_collection")

    return PGVector(
        embeddings=embeddings,
        collection_name=collection_name,
        connection=connection_string,
        use_jsonb=True,
    )

def search_documents(question, k=10):
    try:
        vector_store = get_vector_store()

        results = vector_store.similarity_search_with_score(question, k=k)

        unique_results = []
        seen_contents = set()

        for doc, score in results:
           content_hash = hash(doc.page_content[:500])
           if content_hash not in seen_contents:
                seen_contents.add(content_hash)
                unique_results.append((doc, score))

        return unique_results[:k]

    except Exception as e:
        print(f"Erro na busca vetorial: {str(e)}")
        return []

def search_prompt(question=None):
    if not question:
        return None

    try:
        results = search_documents(question, k=10)

        if not results:
            return "Não tenho informações necessárias para responder sua pergunta."

        context_parts = []
        for doc, score in results:
            context_parts.append(doc.page_content)

        context = "\n\n".join(context_parts)

        llm = ChatGoogleGenerativeAI(
            model="gemini-2.5-flash-lite",
            google_api_key=os.getenv("GOOGLE_API_KEY"),
            temperature=0
        )

        prompt = PromptTemplate(
            template=PROMPT_TEMPLATE,
            input_variables=["contexto", "pergunta"],
        )

        formatted_prompt = prompt.format(
            contexto=context,
            pergunta=question
        )

        response = llm.invoke(formatted_prompt)
        return response.content

    except Exception as e:
        print(f"Erro detalhado: {str(e)}")
        return f"Erro ao obter resposta: {str(e)}"