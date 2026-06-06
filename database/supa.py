from sqlalchemy import create_engine
from dotenv import load_dotenv
import os

load_dotenv()


class supa:
    def __init__(self):
        self.engine = create_engine(f'postgresql+psycopg2://postgres:{os.getenv("SUPABASE_PASS")}@db.ihxtvivmofoiztjfhuwg.supabase.co:5432/postgres')

    def insert_data(self, data):
        data.to_sql(
            name='history', 
            con=self.engine, 
            schema='public', 
            if_exists='append',
            index=False
        )