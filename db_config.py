from langchain_community.utilities import SQLDatabase

def get_db():
    db_uri = "mysql+pymysql://root:Mynameisf1_@localhost:3306/atliq_tshirts"
    return SQLDatabase.from_uri(db_uri)
