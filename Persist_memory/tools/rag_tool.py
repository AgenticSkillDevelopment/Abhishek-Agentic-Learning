import os
from dotenv import load_dotenv
from pinecone import Pinecone, ServerlessSpec
from langchain_pinecone import PineconeVectorStore as LangchainPinecone 
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from pinecone import Pinecone


load_dotenv()

def create_rag_tool():
    pc = Pinecone(api_key=os.getenv("PINECONE_API_KEY"))
    index_name = os.getenv("PINECONE_INDEX")

    if index_name not in pc.list_indexes().names():
        pc.create_index(
            name=index_name,
            dimension=384,
            metric="cosine",
            spec=ServerlessSpec(cloud="gcp", region="gcp-starter")
        )

    embedding = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

    loader = TextLoader("data/knowledge_base.txt")
    documents = loader.load()
    chunks = CharacterTextSplitter(chunk_size=600, chunk_overlap=50).split_documents(documents)

    # ✅ Use LangchainPinecone here
    vectordb =LangchainPinecone.from_documents(
    documents=chunks,
    embedding=embedding,
    index_name=index_name,
    pinecone_api_key=os.getenv("PINECONE_API_KEY"),
    
)

    def query_knowledge(query: str) -> str:
        results = vectordb.similarity_search(query, k=3)
        return "\n".join([r.page_content for r in results])

    return query_knowledge
