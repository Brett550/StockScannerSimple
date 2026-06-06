from supabase import create_client
import os
from dotenv import load_dotenv

load_dotenv()

supabase = create_client(
    os.getenv("SUPABASE_URL"),
    os.getenv("SUPABASE_KEY")
)

class supa:
    def insert_data(self, data):
        records = data.to_dict(orient="records")
        supabase.table("history").insert(records).execute()