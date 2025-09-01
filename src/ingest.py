import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector
from langchain.schema import Document

load_dotenv()

PDF_PATH = os.getenv("PDF_PATH")

def ingest_pdf():
    if not PDF_PATH:
        raise ValueError("PDF_PATH não configurado no arquivo .env")


    print(f"Carregando PDF: {PDF_PATH}")
    loader = PyPDFLoader(PDF_PATH)
    documents = loader.load()

    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        length_function=len,
    )

    chunks = text_splitter.split_documents(documents)
    print(f"Documento dividido em {len(chunks)} chunks")

    embeddings = GoogleGenerativeAIEmbeddings(
        model=os.getenv("GOOGLE_EMBEDDING_MODEL", "models/embedding-001"),
        google_api_key=os.getenv("GOOGLE_API_KEY")
    )


    print("Armazenando vetores no PostgreSQL...")


    connection_string = os.getenv("DATABASE_URL")
    collection_name = os.getenv("PG_VECTOR_COLLECTION_NAME", "rag_collection")

    vectorstore = PGVector.from_documents(
        documents=chunks,
        embedding=embeddings,
        collection_name=collection_name,
        connection=connection_string,
        use_jsonb=True,
    )

    print("Ingestão concluída com sucesso!")

if __name__ == "__main__":
    ingest_pdf()