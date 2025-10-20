import os

from dotenv import load_dotenv
from sqlalchemy import create_engine
from sqlalchemy.engine import Engine
from typing import List

class DB_Connector:
    def __init__(self):
        self.engine = None

    def established_connection(self):
        if self.engine is None:
            try:
                self.engine = self.setup_engine()
                if self.engine is None:
                    raise RuntimeError("Failed to create engine.")
            except Exception as ex:
                raise RuntimeError(f"Database connection error: {str(ex)}")

    def setup_engine(self) -> Engine:
        load_dotenv("./../env")

        DB_USER = os.getenv("DB_USER", "user")
        DB_PASSWORD = os.getenv("DB_PASSWORD", "user")
        DB_NAME = os.getenv("DB_NAME", "DR")
        DB_HOST = os.getenv("DB_HOST", "localhost")
        DB_PORT = os.getenv("DB_OUT_PORT", "3306")

        db_connection = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

        try:
            self.engine = create_engine(db_connection)
        except Exception as ex:
            raise RuntimeError(f'Engine creation error: {str(ex)=}')
        return self.engine

    def insert_data_to_test_table(self):
        self.established_connection()
        
        query = "INSERT INTO Test_table (DT) VALUES (DATE_FORMAT(SYSDATE(), '%Y-%m-%d %H:%i:%s'));"
        cmd = query.strip()
        cmd_safe = cmd.replace('%', '%%')

        with self.engine.begin() as conn:
            try:
                conn.exec_driver_sql(cmd_safe)
            except Exception as ex:
                raise RuntimeError(f'Insert error: {str(ex)=}')
        
    def get_all_data_from_test_table(self) -> List[str]:
        result: List[str] = []
        self.established_connection()
        
        query = "SELECT DT FROM Test_table;"

        try:
            with self.engine.begin() as conn:
                cursor = conn.exec_driver_sql(query)
                response = cursor.fetchall()
                if response is not None:
                    for row in response:
                        result.append(row[0])
        except Exception as ex:
            raise RuntimeError(f'Getting all data error: {str(ex)=}')
        
        return result
        
    def get_last_data_from_test_table(self) -> List[str]:
        result: List[str] = []
        self.established_connection()
        
        query = "SELECT DT FROM Test_table ORDER BY DT DESC LIMIT 1;"

        try:
            with self.engine.begin() as conn:
                cursor = conn.exec_driver_sql(query)
                response = cursor.fetchone()
                if response is not None:
                    result.append(response[0])
        except Exception as ex:
            raise RuntimeError(f'Getting last data error: {str(ex)=}')
        
        return result
    
    def delete_all_data_from_test_table(self):
        self.established_connection()
        
        query = "DELETE FROM Test_table;"

        with self.engine.begin() as conn:
            try:
                conn.exec_driver_sql(query)
            except Exception as ex:
                raise RuntimeError(f'Delete error: {str(ex)=}')