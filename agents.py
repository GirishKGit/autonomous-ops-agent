import os
import json
from datetime import datetime
from dotenv import load_dotenv
from langchain_cohere import ChatCohere, CohereEmbeddings
from crewai import Agent
from langchain_community.vectorstores import Chroma
from langchain.chains import RetrievalQA
from langchain.tools import Tool
import logging

# Load environment variables
load_dotenv()

# Configure logging
from pythonjsonlogger import jsonlogger

logHandler = logging.StreamHandler()
formatter = jsonlogger.JsonFormatter('%(asctime)s %(levelname)s %(name)s %(message)s')
logHandler.setFormatter(formatter)

logger = logging.getLogger()
logger.setLevel(logging.INFO)
logger.addHandler(logHandler)


# Set up the LLM
llm = ChatCohere(
    cohere_api_key=os.getenv("COHERE_API_KEY"),
    temperature=0.7,
    model="command"
)

# Set up the retriever
retriever = Chroma(
    persist_directory="rag_policy_db",
    embedding_function=CohereEmbeddings(
        model="embed-english-light-v3.0",
        cohere_api_key=os.getenv("COHERE_API_KEY")
    )
).as_retriever()

# Create a RetrievalQA chain
rag_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=retriever,
    return_source_documents=True
)

# MCP-enabled query handler

def policy_rag_with_mcp(query: str) -> str:
    try:
        logger.info(f"Received query: {query}")
        response = rag_chain(query)
        logger.info(f"Response from rag_chain: {response}")
        result = response["result"]

        # Extract and format metadata
        source_metadata = [
            {
                "chunk_id": doc.metadata.get("chunk_id", "unknown"),
                "source": doc.metadata.get("source", "unknown")
            }
            for doc in response.get("source_documents", [])
        ]

        mcp_metadata = {
            "model": "cohere/command",
            "retrieved_documents": source_metadata,
            "timestamp": datetime.now().isoformat(),
            "agent": "PolicyBot",
            "confidence": "high",
            "query": query
        }

        logger.info(f"MCP Metadata: {mcp_metadata}")

        with open("mcp_log.jsonl", "a", encoding="utf-8") as f:
            f.write(json.dumps({
                "response": result,
                "mcp": mcp_metadata
            }) + "\n")

        logger.info("MCP metadata logged successfully.")

        # Return formatted result with source details
        formatted_sources = "\n".join([
            f"📄 Source: {doc['source']} | Chunk: {doc['chunk_id']}"
            for doc in source_metadata
        ])
        return f"{result}\n\n🔗 Sources:\n{formatted_sources}"

    except Exception as e:
        logger.error(f"Error processing query: {str(e)}")
        return f"Error processing query: {str(e)}"

# Placeholder function for security analysis
def security_analysis_with_mcp(logs: str) -> str:
    return "Security analysis placeholder response."

# Wrap into a Tool for CrewAI
policy_tool = Tool(
    name="Policy Retrieval QA",
    func=policy_rag_with_mcp,
    description="Use this tool to answer questions about company policies based on the employee handbook"
)

# Define agents AFTER the tool is defined
PolicyBot = Agent(
    role="HR Policy Expert",
    goal="Provide clear, accurate, and concise answers about company policies",
    backstory="""You are an experienced HR professional with deep knowledge of company policies.
    You provide clear, structured answers and always cite specific policy documents when available.
    If information is not available, you clearly state this and suggest where to find the information.
    You maintain a professional and helpful tone.""",
    llm=llm,
    tools=[policy_tool],
    verbose=True
)

MonitorBot = Agent(
    role="System Security Analyst",
    goal="Analyze system logs and identify security threats or system issues",
    backstory="""You are a cybersecurity expert specializing in log analysis.
    You examine system logs for patterns of suspicious activity, security breaches, and system anomalies.
    You provide detailed analysis with severity levels and recommended actions.
    You focus on technical details and security implications.""",
    llm=llm,
    verbose=True
)

# Function to test file writing permissions
def test_file_write():
    try:
        with open("test_write.txt", "w") as f:
            f.write("This is a test write.")
        logger.info("Test write successful.")
    except Exception as e:
        logger.error(f"Test write failed: {str(e)}")

# Call the test function
test_file_write()
