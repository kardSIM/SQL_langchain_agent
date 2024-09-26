import os
import streamlit as st
from langchain.callbacks import StreamlitCallbackHandler
from src.conntect2db import get_db_connection
from src.agents import create_SQL_agent, run_agent
from dotenv import load_dotenv




def extract_python_code(text):
    """Extract Python code from the text, assuming it's wrapped in triple backticks."""
    start = text.find("```python")
    end = text.find("```", start + 1)
    if start != -1 and end != -1:
        return text[start+9:end].strip()
    return None


def login():
    st.title("Login")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    
    if st.button("Login"):

        db = get_db_connection(username, password)  
        if db:
            st.session_state["authenticated"] = True
            st.session_state["db_connection"] = db  
            st.success("Logged in successfully!")
        else:
            st.error("Invalid username or password")

def run_streamlit_app():


    load_dotenv()
    groq_api = os.environ['GROQ_API']
    st.set_page_config(page_title="DBCopilot", page_icon="😊")
    st.header('📊 Welcome to SQL agent')

    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        login()
    else:

        if "messages" not in st.session_state or st.sidebar.button("Clear message history"):
            st.session_state["messages"] = [{"role": "assistant", "content": "Ask me anything about the pagila database 🎬"}]
        for msg in st.session_state.messages:
            st.chat_message(msg["role"]).write(msg["content"])
        db = st.session_state.get("db_connection")

        user_input = st.chat_input(placeholder="Ask me anything!")
        agent = create_SQL_agent(db, groq_api)  

        
        if user_input:
            st.session_state.messages.append({"role": "user", "content": user_input})
            st.chat_message("user").write(user_input)

            with st.chat_message("assistant"):
                st_cb = StreamlitCallbackHandler(st.container())
                result = run_agent(agent, user_input, callbacks = [st_cb])
                st.session_state.messages.append({"role": "assistant", "content": result["output"]})
                st.write(result["output"])            

