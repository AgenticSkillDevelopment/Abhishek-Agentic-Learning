# retriever_setup.py
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import WebBaseLoader

# 1. Load text file
loader = WebBaseLoader(["https://en.wikipedia.org/wiki/Zodiac_(film)"])
docs = loader.load()

# 2. Split the document into chunks
splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=100)
chunks = splitter.split_documents(docs)

# 3. Generate embeddings
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")

# 4. Build and save FAISS vectorstore
db = FAISS.from_documents(chunks, embeddings)
db.save_local("faiss_store")

retriever = db.as_retriever()
print("✅ Retriever ready and saved.")
