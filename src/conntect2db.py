from sqlalchemy.exc import SQLAlchemyError
from langchain.sql_database import SQLDatabase

def get_db_connection(username,password):
    try:
        db = SQLDatabase.from_uri(
            f"postgresql+psycopg2://{username}:{password}@127.0.0.1:65001/pagila"
        )
        return db
    except SQLAlchemyError as e:
        print(f"An error occurred while connecting to the database: {e}")
        return None
    