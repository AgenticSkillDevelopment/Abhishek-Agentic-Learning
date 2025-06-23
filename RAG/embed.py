from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

import pickle

with open("chunks.pkl", "rb") as f:
    docs = pickle.load(f)

embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
vectorstore = FAISS.from_documents(docs, embeddings)
vectorstore.save_local("rag_faiss")

print("✅ Embeddings stored in FAISS DB.")
