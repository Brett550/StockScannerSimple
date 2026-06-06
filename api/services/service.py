from typing import Any

from db.supabase import supabase
from datetime import date, datetime, time

def get_stocks(limit: int, offset: int, date_str: str | None = None) -> list[dict[str, Any]]:
    query = supabase.table('history').select("*")

    # filter by date if provided
    # Note: database date col is a timestamp
    if date_str:
        parsed_date = datetime.strptime(date_str, "%Y-%m-%d").date()
        start_dt = datetime.combine(parsed_date, time.min)
        end_dt = datetime.combine(parsed_date, time.max)
        query = query.gte("date", start_dt.isoformat()).lte("date", end_dt.isoformat())

    response = query.range(offset, offset + limit - 1).execute()
    return response.data

def get_streaks() -> list[dict[str, Any]]:
    response = supabase.table("ticker_streaks").select("*").order("streak_length_days", desc=True).order("ticker").execute()
    return response.data