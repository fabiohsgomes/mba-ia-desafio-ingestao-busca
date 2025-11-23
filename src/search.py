import os
from dotenv import load_dotenv

from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_postgres import PGVector

from langchain.prompts import PromptTemplate

load_dotenv()

PROMPT_TEMPLATE = """
CONTEXTO:
{contexto}

REGRAS:
- Responda somente com base no CONTEXTO.
- Se a informação não estiver explicitamente no CONTEXTO, responda:
  "Não tenho informações necessárias para responder sua pergunta."
- NUNCA invente ou use conhecimento externo.
- NUNCA produza opiniões ou interpretações além do que está escrito.

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
prompt = PromptTemplate(
    input_variables=["contexto","pergunta"],
    template=PROMPT_TEMPLATE,
)

llm = ChatGoogleGenerativeAI(model=os.getenv("GOOGLE_LLM"), temperature=0.3)

question_embeddings = GoogleGenerativeAIEmbeddings(model=os.getenv("GENAI_EMBEDDING_MODEL","gemini-embedding-001"))

store = PGVector(
    embeddings=question_embeddings,
    collection_name=os.getenv("PG_VECTOR_COLLECTION_NAME"),
    connection=os.getenv("DATABASE_URL"),
    use_jsonb=True
)

chain = prompt | llm

def search_prompt(question=None)-> any:
    if not question:
        raise ValueError("Question is required")

    result = store.similarity_search_with_score(question, k=10)

    contexto = []
    for doc, score in result:
        contexto.append(f"Content: {doc.page_content}\nSource: {doc.metadata.get('source', 'N/A')}\nScore: {score}")

    llm_response = chain.invoke({"contexto": "\n\n".join(contexto), "pergunta": question})

    return llm_response.content