import os
import streamlit as st
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.vectorstores import FAISS
from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
from langchain.chains import create_retrieval_chain
from langchain.chains.combine_documents import create_stuff_documents_chain
from langchain_core.prompts import ChatPromptTemplate
from dotenv import load_dotenv

load_dotenv()

st.set_page_config(page_title="AI Research Assistant", layout="wide")
st.title("📚 AI Research Paper Assistant")

# Initialize Vector Store
@st.cache_resource
def load_and_process_pdfs():
    loader = PyPDFDirectoryLoader("./docs")
    docs = loader.load()
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    final_documents = text_splitter.split_documents(docs)
    
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectors = FAISS.from_documents(final_documents, embeddings)
    return vectors

api_key = os.getenv("GOOGLE_API_KEY")

if not api_key:
    st.warning("⚠️ Please configure your GOOGLE_API_KEY in a .env file or environment variables.")
else:
    try:
        vectors = load_and_process_pdfs()
        st.success("✅ Research Papers Loaded Successfully!")
        
        llm = ChatGoogleGenerativeAI(model="gemini-1.5-flash", temperature=0.3)
        
        system_prompt = (
            "You are an expert AI research assistant. Use the following retrieved context "
            "from research papers to answer the question. If you don't know the answer, "
            "say that you don't know. Keep the answer concise and clear.\n\n"
            "{context}"
        )
        
        prompt = ChatPromptTemplate.from_messages([
            ("system", system_prompt),
            ("human", "{input}"),
        ])
        
        question_answer_chain = create_stuff_documents_chain(llm, prompt)
        rag_chain = create_retrieval_chain(vectors.as_retriever(), question_answer_chain)
        
        user_query = st.text_input("Ask any question about the downloaded research papers:")
        
        if user_query:
            with st.spinner("Analyzing papers..."):
                response = rag_chain.invoke({"input": user_query})
                st.write("### Answer:")
                st.write(response["answer"])
                
    except Exception as e:
        st.error(f"Error loading model or papers: {e}")