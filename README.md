
# 🛍️ Retail Data Chatbot

A conversational analytics chatbot for querying Atliq T-Shirts retail sales and inventory, powered by Google Gemini LLM, LangChain, and Streamlit.  
Easily ask business questions in natural language—get instant, data-driven answers directly from your MySQL database.

## Features

- **Conversational chat UI** built with Streamlit
- **Natural language to SQL**: Transform business questions into automatic, safe MySQL queries
- **Answers from live data**: Results are computed from your retail database in real-time
- **Supports aggregate questions**: Count inventory, total revenue, stock breakdowns, and more
- **Few-shot learning**: Accurate SQL patterns and chain-of-thought reasoning via LangChain prompt engineering
- **Displays chat history** for rich, interactive analytics sessions
- **Secure API management** with .env file and environment variables

## Tech Stack

- [Streamlit](https://streamlit.io/) — for web app UI
- [Google Gemini API](https://ai.google.dev/) — LLM for question and answer generation
- [LangChain](https://python.langchain.com/) — chains for prompt management and SQL execution
- [MySQL](https://www.mysql.com/) — retail operational database
- [Python](https://python.org/) — data engineering backend

## How It Works

1. User asks a question (e.g. “How many red Adidas shirts are in stock?”)
2. Gemini LLM—guided by prompt templates and few-shot examples—generates a precise, safe SQL query
3. LangChain executes the query on your retail database and returns the results
4. The chatbot formulates and displays a clear, natural-language answer in the UI

## Getting Started

1. **Clone this repo**
2. **Install dependencies**  
   `pip install -r requirements.txt`
3. **Set up your .env file**  
   ```
   GOOGLE_API_KEY=your_gemini_api_key_here
   ```
4. **Configure your MySQL connection** in `db_config.py`
5. **Run the app**  
   `streamlit run app.py`

## Example Questions

- How many large Adidas shirts do we have in stock?
- What is the total revenue for Levi T-shirts after discounts?
- List all brands in stock.
- Show total inventory by color.

## Screenshots
<img width="1885" height="912" alt="image" src="https://github.com/user-attachments/assets/db847403-c775-416e-b55a-d560bcb96376" />

<img width="1895" height="963" alt="Screenshot 2025-10-21 220027" src="https://github.com/user-attachments/assets/0b33e897-fd98-4757-bb5a-9b878c8387a5" />


MIT License

## Credits

- https://discuss.streamlit.io/t/streamlit-best-practices/57921
- https://towardsdatascience.com/rapid-prototyping-of-chatbots-with-streamlit-and-chainlit/
- https://towardsdatascience.com/step-by-step-guide-to-build-and-deploy-an-llm-powered-chat-with-memory-in-streamlit/
- https://github.com/codebasics/langchain
- https://blog.streamlit.io/how-to-build-an-llm-powered-chatbot-with-streamlit/
