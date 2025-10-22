import streamlit as st
import os
import re  # 🔹 For extracting SQL query
from dotenv import load_dotenv
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.utilities import SQLDatabase
from langchain.prompts import FewShotPromptTemplate, PromptTemplate
from fewshot_examples import fewshot_examples
from db_config import get_db
import langchain

os.environ["LANGCHAIN_VERBOSE"] = "true"
langchain.debug = True


# --- PAGE CONFIG ---
st.set_page_config(page_title="Retail Data Chatbot", layout="centered")

# --- UI Theme Customization ---
st.markdown("""
<style>
.stApp { background-color: #0d1a3c; color: #f0f2f6; }
.stApp [data-testid="stSidebar"], .stApp [data-testid="stHeader"] { background-color: #1a2b56; }
.stApp [data-testid="stTextInput"] > div > div > input { background-color: #1a2b56; color: #f0f2f6; }
.stApp [data-testid="chat-input"] { background-color: #1a2b56; }
[data-testid="stChatMessage"] {
    background-color: #1a2b56;
    border-radius: 12px;
    padding: 10px 15px;
    margin-bottom: 10px;
}
[data-testid="stChatMessage"][data-testid="user"] {
    background-color: #233469;
}

</style>
""", unsafe_allow_html=True)

# -----------------------------
load_dotenv()
api_key = os.getenv("GOOGLE_API_KEY")

# Database connection
db = get_db()
table_schema = db.get_table_info()

# --- PROMPT SETUP ---
mysql_prompt = """
You are a MySQL expert. Given an input question, first create a syntactically correct MySQL query to run (using only columns/values seen below),
then look at the results to answer the original question as a single sentence.

Schema:
{schema}

Only output the SQL query as plain text (no markdown/code fences).
Carefully validate column/table names before writing SQL!

Use format:
Question: {input}
SQLQuery: <query>
Answer: <concise natural language answer>
"""

example_prompt = PromptTemplate(
    input_variables=["Question", "SQLQuery", "SQLResult", "Answer"],
    template="Question: {Question}\nSQLQuery: {SQLQuery}\nSQLResult: {SQLResult}\nAnswer: {Answer}\n"
)
few_shot_prompt = FewShotPromptTemplate(
    examples=fewshot_examples,
    example_prompt=example_prompt,
    prefix=mysql_prompt,
    suffix="Question: {input}",
    input_variables=["input", "schema", "top_k"],
)

# --- MODEL ---
llm = ChatGoogleGenerativeAI(model="gemini-2.5-pro", temperature=0.2, api_key=api_key)

# --- STREAMLIT UI ---
st.set_page_config(page_title="Retail Data Chatbot", layout="centered")
st.title("🛍️ Retail Data Chatbot")
st.markdown("Ask me questions about **Atliq T-Shirts** sales and stock!")

# --- CHAT HISTORY ---
if "messages" not in st.session_state:
    st.session_state["messages"] = []

for msg in st.session_state["messages"]:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# --- Helper: Extract SQL query ---
def extract_sql_query(text):
    """Find SQLQuery: ... and return the actual query string."""
    match = re.search(r"SQLQuery:\s*(.*)", text, re.DOTALL)
    if match:
        query = match.group(1).strip()
        # Remove any trailing Answer: if LLM appends it
        query = query.split("Answer:")[0].strip()
        return query
    return None

# --- CHAT INPUT ---
if user_input := st.chat_input("Type your question here..."):
    st.session_state["messages"].append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    with st.spinner("Thinking..."):
        top_k = 5
        # 🔹 Step 1: Ask LLM to produce SQL query
        full_prompt = few_shot_prompt.format(input=user_input, schema=table_schema, top_k=top_k)
        generated = llm.invoke(full_prompt).content

        # 🔹 Step 2: Extract the SQL query
        sql_query = extract_sql_query(generated)

        if not sql_query:
            answer = "I couldn't generate a valid SQL query. Please check your question."
        else:
            try:
                # 🔹 Step 3: Execute SQL query
                sql_result = db.run(sql_query)

                # 🔹 Step 4: Generate final natural-language answer
                result_text = str(sql_result)
                answer_prompt = (
                    f"The SQL query result is: {result_text}. "
                    f"Now answer the original question: '{user_input}' "
                    f"in a concise and natural way, using the actual result number."
                )
                answer = llm.invoke(answer_prompt).content.strip()


            except Exception as e:
                answer = f"Error executing query: {e}"

    # --- Display Assistant Message ---
    with st.chat_message("assistant"):
        st.markdown(answer)

    st.session_state["messages"].append({"role": "assistant", "content": answer})
