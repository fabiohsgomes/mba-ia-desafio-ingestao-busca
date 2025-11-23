import os
from pathlib import Path
from dotenv import load_dotenv

from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_core.documents import Document
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_postgres import PGVector

load_dotenv()

for k in ("GOOGLE_API_KEY", "GOOGLE_EMBEDDING_MODEL","GOOGLE_LLM", "PG_VECTOR_COLLECTION_NAME", "PDF_NAME"):
    if not os.getenv(k):
        raise RuntimeError(f"Environment variable {k} is not set")

PDF_NAME = os.getenv("PDF_NAME")
current_dir = Path(__file__).parent

exists = True
pdf_path = current_dir / PDF_NAME

while not pdf_path.exists():
    current_dir = current_dir.parent
    pdf_path = current_dir / PDF_NAME

    if current_dir == "/":
        exists = False
        break

if exists == False:
    raise FileNotFoundError(f"O arquivo {PDF_NAME} não foi encontrado em nenhum diretório pai.")

def ingest_pdf():
    document = PyPDFLoader(str(pdf_path)).load()
    splits = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=150,
        add_start_index=False,
    ).split_documents(document)

    if not splits:
        raise SystemExit(0)
    
    enriched = [
        Document(
            page_content=d.page_content,
            metadata={k: v for k, v in d.metadata.items() if v not in("", None)},
        )
        for d in splits
    ]

    ids = [f"doc-{i}" for i in range(len(enriched))]

    embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GOOGLE_EMBEDDING_MODEL"))

    store = PGVector(
        embeddings=embeddings,
        collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
        connection=os.getenv("DATABASE_URL"),
        use_jsonb=True
    )

    store.add_documents(documents=enriched, ids=ids)
    
if __name__ == "__main__":
    ingest_pdf()