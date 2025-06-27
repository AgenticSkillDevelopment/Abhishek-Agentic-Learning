# query_llm.py
import os
from langchain.chains import RetrievalQA
from langchain.prompts import PromptTemplate
from langchain_community.vectorstores import FAISS
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_groq import ChatGroq  # ✅ Groq LLM
from dotenv import load_dotenv
load_dotenv()
# ✅ Set Groq API Key
os.environ["GROQ_API_KEY"] = os.getenv("GROQ_API_KEY")

# ✅ Load retriever
embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
db = FAISS.load_local("faiss_store", embeddings, allow_dangerous_deserialization=True)
retriever = db.as_retriever()

# ✅ Create LLM
llm = ChatGroq(model="llama3-8b-8192")

# ✅ (Optional) Prompt template
prompt_template = PromptTemplate(
    input_variables=["context", "question"],
    template="""
You are a helpful assistant answering questions from the given context.

Context:
{context}

Question:
{question}

Answer:
""",
)

# ✅ QA Chain
qa = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    chain_type="stuff",
    return_source_documents=False,
    chain_type_kwargs={"prompt": prompt_template}
)

# ✅ Ask user query
query = input("🧠 Ask me anything: ")
result = qa.astream({"query": query})
print("\n🤖 Answer:", result['result'])
