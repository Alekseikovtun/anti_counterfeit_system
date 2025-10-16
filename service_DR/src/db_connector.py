import os
# import sqlalchemy as sqa

from dotenv import load_dotenv
from sqlalchemy import create_engine

class DB_Connector:
    def __init__(self):
        self.engine = None

    def established_connection(self):
        if self.engine is None:
            try:
                engine = self.connection()
                if engine is None:
                    raise RuntimeError("Failed to create engine.")
                self.engine = engine
            except Exception as ex:
                raise RuntimeError(f"Database connection error: {str(ex)}")
        return self.engine

    def connection(self):
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
        engine = self.established_connection()
        if engine is None:
            raise RuntimeError("No DB connection, abort insert")
        
        sql = "INSERT INTO Test_table (DT) VALUES (DATE_FORMAT(SYSDATE(), '%Y-%m-%d %H:%i:%s'));"
        cmd = sql.strip()
        if not cmd:
            return
        cmd_safe = cmd.replace('%', '%%')

        with engine.begin() as conn:
            try:
                conn.exec_driver_sql(cmd_safe)
            except Exception as ex:
                raise RuntimeError(f'Insert error: {str(ex)=}')
        
    def get_all_data_from_test_table(self):
        engine = self.established_connection()
        if engine is None:
            raise RuntimeError("No DB connection, abort getting all data")
        
        sql = "SELECT * FROM Test_table;"
        cmd = sql.strip()
        if not cmd:
            return []
        cmd_safe = cmd.replace('%', '%%')

        with engine.begin() as conn:
            try:
                result = conn.exec_driver_sql(cmd_safe)
                rows = result.fetchall()
                return rows
            except Exception as ex:
                raise RuntimeError(f'Getting all data error: {str(ex)=}')
        
    def get_last_data_from_test_table(self):
        engine = self.established_connection()
        if engine is None:
            raise RuntimeError("No DB connection, abort getting last data")
        
        sql = "SELECT * FROM Test_table ORDER BY DT DESC LIMIT 1;"
        cmd = sql.strip()
        if not cmd:
            return None
        cmd_safe = cmd.replace('%', '%%')

        with engine.begin() as conn:
            try:
                result = conn.exec_driver_sql(cmd_safe)
                row = result.fetchone()
                return row
            except Exception as ex:
                raise RuntimeError(f'Getting last data error: {str(ex)=}')
    
    def delete_all_data_from_test_table(self):
        engine = self.established_connection()
        if engine is None:
            raise RuntimeError("No DB connection, abort delete")
        
        sql = "DELETE FROM Test_table;"
        cmd = sql.strip()
        if not cmd:
            return
        cmd_safe = cmd.replace('%', '%%')

        with engine.begin() as conn:
            try:
                conn.exec_driver_sql(cmd_safe)
            except Exception as ex:
                raise RuntimeError(f'Delete error: {str(ex)=}')