from sqlalchemy import create_engine, text
import os 
from dotenv import load_dotenv
load_dotenv()

engine=create_engine(f"postgresql://{os.getenv("db_user")}:{os.getenv("db_password")}@{os.getenv("db_host")}:{os.getenv("db_port")}/{os.getenv("db_database")}")



try:
    print("Trying to connect to PostgreSQL")
    with engine.connect() as connection:
        result= connection.execute(text("SELECT 'This is a test.'"))
        mesaj = result.scalar()
        print("SUCCES!")
        print(f"Bd response: {mesaj}")
except Exception as e:
    print("Couldnt connect")
    print(f"Details: {e}")
