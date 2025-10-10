from db_connector import DB_Connector

if __name__ == "__main__":
    connector = DB_Connector()
    connector.insert_data_to_test_table()
    
