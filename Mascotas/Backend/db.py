import json
import pyodbc

def get_db_connection():
    with open('db_config.json') as config_file:
        config = json.load(config_file)
    connection_string = f"DRIVER={{ODBC Driver 17 for SQL Server}};SERVER={config['server']};DATABASE={config['database']};UID={config['user']};PWD={config['password']}"
    return pyodbc.connect(connection_string)