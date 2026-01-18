import os
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain.agents import initialize_agent, AgentType
from langchain.tools.retriever import create_retriever_tool
from langchain_community.tools import DuckDuckGoSearchRun

load_dotenv()
DB_FAISS_PATH = "vectorstore/db_faiss"
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

def build_chain():
    """Builds and returns a Hybrid Agent using initialize_agent (Legacy Compatible)."""
    if not GROQ_API_KEY:
        raise ValueError("GROQ_API_KEY not found in .env")

    llm = ChatGroq(
        model="llama-3.3-70b-versatile",
        api_key=GROQ_API_KEY,
        temperature=0.1
    )

    # 2. Embeddings & Retriever
    embeddings = HuggingFaceEmbeddings(
        model_name='sentence-transformers/all-MiniLM-L6-v2',
        model_kwargs={'device': 'cpu'}
    )

    if not os.path.exists(DB_FAISS_PATH):
        raise FileNotFoundError("FAISS database not found. Run ingest.py first.")

    db = FAISS.load_local(DB_FAISS_PATH, embeddings, allow_dangerous_deserialization=True)
    retriever = db.as_retriever(search_type="similarity", search_kwargs={'k': 5})

    # 3. Define Tools
    campus_tool = create_retriever_tool(
        retriever,
        "campus_retriever",
        "Search for information about A.P. Shah Institute of Technology (APSIT), including fees, admission, faculty, placements, and campus details. ALWAYS use this tool first for college-related queries."
    )

    web_tool = DuckDuckGoSearchRun(
        name="web_search",
        description="Search the web for general knowledge, current events, or comparison data not available in the college database. Use this if 'campus_retriever' fails."
    )

    tools = [campus_tool, web_tool]

    # 4. Initialize Agent (Legacy Mode for Compatibility)
    # CHAT_ZERO_SHOT_REACT_DESCRIPTION works well with Chat models
    agent_executor = initialize_agent(
        tools,
        llm,
        agent=AgentType.CHAT_ZERO_SHOT_REACT_DESCRIPTION,
        verbose=True,
        handle_parsing_errors=True,
        max_iterations=5
    )

    print("Hybrid Agent (Groq Llama 3) initialized successfully.")
    return agent_executor