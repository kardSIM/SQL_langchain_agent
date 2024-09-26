# SQL_langchain_agent
## Description 
The LangChain SQL Agent enables intuitive interaction with SQL databases by translating natural language queries into SQL statements, simplifying data retrieval and processing for users without SQL expertise.

## Key Features 
This agent Utilize the Llama3-8B LLM model as its reasoning engine and as    generator, enhancing the agent's ability to understand and process complex natural language queries.

it also comes pre-loaded with two robust tools:
SQLDatabaseToolkit: Facilitates seamless query translation and efficient data retrieval from SQL databases.
PythonREPLTool: Enables running Python code to process data, allowing for advanced data manipulation and analysis.

## Database
The Pagila database, a sample DVD rental database for PostgreSQL, is ideal for experimentation. To set it up using Docker, run the following command:
```bash
sh run-pg-pagila-docker.sh pagila_postgresql_docker
```
This script performs several actions:
Builds the Docker container: Initializes the environment for running PostgreSQL.
Downloads the Pagila database: Retrieves the necessary data and schema files.
Instantiates the cluster: pre-configuration of the database.

connect to the Pagila database using the following command:
```bash
psql -U postgres -d pagila
```
create a new user role and grant him group permission :
```bash
CREATE ROLE new_user; WITH LOGIN PASSWORD 'password';
GRANT pagila_dba TO new_user;
```
## Run the agent

Claim Your API Key: First, obtain your API key from Groq and store it in .env file

Run the Streamlit Application: 
```bash
streamlit run main.py
```

enter credentials to log in to the database.

Start Querying: Once logged in, you can begin querying the Groq API through the Streamlit interface.

## Results

The SQL Agent can:
Answer Database-Related Questions: 
Create and Save Plots
Return SQL Statements


To customize agent behavior, modify the template.py file.




