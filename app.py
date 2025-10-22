import streamlit as st
from dotenv import load_dotenv
import os
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain_experimental.sql import SQLDatabaseChain
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from fewshot_examples import fewshot_examples
from db_config import get_db

# Load .env & API key
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Get table info and schema for prompt
db = get_db()
table_schema = db.get_table_info()  # Displays columns for LLM context

# SQL instruction prompt (with schema and explicit instructions)
mysql_prompt = """
You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run (using only columns/values seen below), then look at the results to answer the original question as a single sentence.

Schema:
{schema}

Only output the SQL as plain text (no markdown/code fences).
Use LIMIT {top_k} if quantity is unspecified.
Carefully validate column/table names before writing SQL!

Use format:
Question: {input}
SQLQuery: <query>
SQLResult: <result>
Answer: <concise natural language>
"""

# Few-shot prompt template
example_prompt = PromptTemplate(
    input_variables=["question", "sql", "answer"],
    template="Question: {question}\nSQLQuery: {sql}\nAnswer: {answer}\n",
)
few_shot_prompt = FewShotPromptTemplate(
    examples=fewshot_examples,
    example_prompt=example_prompt,
    prefix=mysql_prompt,
    suffix="Question: {input}",
    input_variables=["input", "schema", "top_k"],
)

# Set up Gemini LLM and Chain
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2, api_key=api_key)
chain = SQLDatabaseChain.from_llm(llm, db, verbose=True)

# --- Streamlit UI and Chat History ---
st.set_page_config(page_title="Retail Data Chatbot", layout="centered")
st.title("🛍️ Retail Data Chatbot")
st.markdown("Ask me questions about **Atliq T-Shirts** sales and stock!")

# Initialize chat history in session state
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# Display chat history
for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# User input
if user_input := st.chat_input("Type your question here..."):
    # Add user message to history and display
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Show spinner while processing
    with st.spinner("Thinking..."):
        top_k = 5
        # Build prompt with schema
        full_prompt = few_shot_prompt.format(input=user_input, schema=table_schema, top_k=top_k)
        response = chain.invoke({"query": full_prompt})
        answer = response.get('result', '').strip()
        if not answer:
            answer = "Sorry, I couldn't find an answer. Please check for valid columns/values."

    # Display assistant answer and add to history
    with st.chat_message("assistant"):
        st.markdown(answer)
    st.session_state["messages"].append({"role": "assistant", "content": answer})
