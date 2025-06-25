import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_community.vectorstores import Pinecone as LangchainPinecone
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

load_dotenv()
from pinecone import Pinecone, ServerlessSpec

def create_rag_tool():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX")

    # ✅ Correct: Must specify spec for serverless region
    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=768,
            metric="cosine",
            spec=ServerlessSpec(
                cloud="gcp",
                region="gcp-starter"
            )
        )

    index = pc.Index(index_name)
    embedding = HuggingFaceEmbeddings()

    loader = TextLoader("data/knowledge_base.txt")
    texts = CharacterTextSplitter(chunk_size=500, chunk_overlap=50).split_documents(loader.load())
    vectordb = Pinecone.from_documents(texts, embedding, index_name=index_name)

    def query_knowledge(query: str) -> str:
        results = vectordb.similarity_search(query, k=3)
        return "\n".join([r.page_content for r in results])

    return query_knowledge
