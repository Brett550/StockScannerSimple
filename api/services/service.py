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
    response = supabase.table("ticker_streaks_noweekend").select("*").order("streak_length_days", desc=True).order("ticker").execute()
    return response.data

def get_newly_added() -> list[dict[str, Any]]:
    response = supabase.table("newly_added").select("*").order("date", desc=True).execute()
    return response.data

def get_newly_removed() -> list[dict[str, Any]]:
    response = supabase.table("newly_removed").select("*").order("date", desc=True).execute()
    return response.data

def get_stats() -> dict[str, Any]:
    # most recent date
    date_response = supabase.table("history").select("date").order("date", desc=True).limit(1).execute()
    most_recent_date = date_response.data[0]["date"].split("T")[0] if date_response.data else None

    # num current tickers
    ticker_response = supabase.table("history").select("ticker").execute()
    num_tickers = len(set(row["ticker"] for row in ticker_response.data))

    # num newly added
    added_response = supabase.table("newly_added").select("*", count="exact").execute()
    num_added = added_response.count

    # num newly removed
    removed_response = supabase.table("newly_removed").select("*", count="exact").execute()
    num_removed = removed_response.count

    # longest streak
    streak_response = supabase.table("ticker_streaks_noweekend").select("streak_length_days").order("streak_length_days", desc=True).limit(1).execute()
    longest_streak = streak_response.data[0]["streak_length_days"] if streak_response.data else None

    return {
        "most_recent_date": most_recent_date,
        "num_tickers": num_tickers,
        "num_added": num_added,
        "num_removed": num_removed,
        "longest_streak": longest_streak
    }