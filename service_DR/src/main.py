import os
import sqlalchemy as sqa

from dotenv import load_dotenv

load_dotenv("./../env")

DB_USER = os.getenv("DB_USER", "user")
DB_PASSWORD = os.getenv("DB_PASSWORD", "user")
DB_NAME = os.getenv("DB_NAME", "DR")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_OUT_PORT", "3306")

db_connection = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

def init_db():
    engine = sqa.create_engine(db_connection)
    fd = open('init_db.sql', 'r', encoding='utf-8')
    sql_file = fd.read()
    fd.close()

    sqlcommands = sql_file.split(';')

    with engine.begin() as conn:
        for command in sqlcommands:
            cmd = command.strip()
            if not cmd:
                continue
            cmd_safe = cmd.replace('%', '%%')
            try:
                conn.exec_driver_sql(cmd_safe)
            except Exception as ex:
                print(f'Command skipped: {command=}, {str(ex)=}')

if __name__ == "__main__":
    init_db()
    
