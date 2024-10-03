from langchain_groq import ChatGroq 
from langchain.agents.agent_toolkits import SQLDatabaseToolkit
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents.agent_toolkits import FileManagementToolkit
from langchain.agents import create_structured_chat_agent
from langchain.agents import AgentExecutor
from src import template
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
import os
def create_SQL_agent(db, groq_api):
    llm=ChatGroq(groq_api_key=groq_api,model_name="Llama3-8b-8192",streaming=True)
    working_directory  = os.getcwd()
    tools = FileManagementToolkit(
        root_dir=str(working_directory),
        selected_tools=["read_file", "write_file", "list_directory"],).get_tools()
    tools.append(PythonREPLTool())
    tools.extend(SQLDatabaseToolkit(db=db, llm=llm).get_tools())
        
    prompt = ChatPromptTemplate.from_messages(
        [
            ("system", template.system),
            MessagesPlaceholder("chat_history", optional=True),
            ("human", template.human),
        ]
    )
    agent = create_structured_chat_agent(llm, tools, prompt)
    agent_executor = AgentExecutor(agent=agent, tools=tools, verbose=True, handle_parsing_errors=True)
    return agent_executor

def run_agent(agent, query, callbacks):    
    return agent.invoke({"input":{query}}, callbacks=callbacks)
