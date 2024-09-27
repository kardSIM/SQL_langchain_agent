from langchain_groq import ChatGroq 
from langchain.sql_database import SQLDatabase
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents import initialize_agent
from langchain.agents import AgentType
from src import template

def create_SQL_agent(db, groq_api):
    llm=ChatGroq(groq_api_key=groq_api,model_name="Llama3-8b-8192",streaming=True)
    tools = []
    tools.append(PythonREPLTool())
    tools.extend(SQLDatabaseToolkit(db=db, llm=llm).get_tools())

    agent = initialize_agent(
        tools=tools, 
        llm=llm, 
        agent= AgentType.ZERO_SHOT_REACT_DESCRIPTION, 
        verbose=True,
        handle_parsing_errors=True,
        agent_kwargs={
            'prefix':template.PREFIX,
            'format_instructions': template.FORMAT_INSTRUCTIONS,
        }    
    )
    return agent

def run_agent(agent, query, callbacks):    
    return agent.invoke(query, callbacks=callbacks)
