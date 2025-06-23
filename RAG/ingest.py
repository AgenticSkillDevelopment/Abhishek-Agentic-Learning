from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.document_loaders import TextLoader
import pickle

loader = TextLoader("my_data.txt")
documents = loader.load()

splitter = RecursiveCharacterTextSplitter(chunk_size=500, chunk_overlap=50)
docs = splitter.split_documents(documents)

with open("chunks.pkl", "wb") as f:
    pickle.dump(docs, f)

print("✅ Document split and saved as chunks.pkl")
