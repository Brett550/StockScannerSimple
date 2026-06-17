from flask import Flask, request
from datetime import date, datetime, time
from db.supabase import supabase
from services.service import get_stats, get_stocks, get_streaks, get_newly_added, get_newly_removed


app = Flask(__name__)


def validate_date(date_str):
    try:
        datetime.strptime(date_str, "%Y-%m-%d")
        return True
    except ValueError:
        return False

@app.route('/stocks', methods=['GET'])
def stocks_route():
    #input validation
    try:
        limit = int(request.args.get("limit", 100))
        offset = int(request.args.get("offset", 0))
    except ValueError:
        return {"success": False, "data": [], "error": "Invalid limit or offset"}, 400
    
    limit = min(limit, 100)  # enforce a maximum limit of 100
    if limit < 1:
        return {"success": False, "data": [], "error": "Limit must be at least 1"}, 400
    offset = max(offset, 0)  # ensure offset is non-negative

    date = request.args.get("date")  # optional
    if date:
        if not validate_date(date):
            return {"success": False, "data": [], "error": "Invalid date format. Please use YYYY-MM-DD."}, 400

    try:
        stocks = get_stocks(limit, offset, date)
        return {"success": True, "data": stocks, "error": None}, 200
    except Exception as e:
        app.logger.error(f"Error fetching data from Supabase: {e}")
        return {"success": False, "data": [], "error": f"Failed to fetch data"}, 500


@app.route('/analytics/streaks', methods=['GET'])
def streaks_route():
    try:
        stocks = get_streaks()
        return {"success": True, "data": stocks, "error": None}, 200
    except Exception as e:
        app.logger.error(f"Error fetching data from Supabase: {e}")
        return {"success": False, "data": [], "error": f"Failed to fetch data"}, 500
    
@app.route('/analytics/newly_added', methods=['GET'])
def newly_added_route():
    try:
        stocks = get_newly_added()
        return {"success": True, "data": stocks, "error": None}, 200
    except Exception as e:
        app.logger.error(f"Error fetching data from Supabase: {e}")
        return {"success": False, "data": [], "error": f"Failed to fetch data"}, 500

@app.route('/analytics/newly_removed', methods=['GET'])
def newly_removed_route():
    try:
        stocks = get_newly_removed()
        return {"success": True, "data": stocks, "error": None}, 200
    except Exception as e:
        app.logger.error(f"Error fetching data from Supabase: {e}")
        return {"success": False, "data": [], "error": f"Failed to fetch data"}, 500
    
@app.route('/analytics/stats', methods=['GET'])
def stats_route():
    try:
        stats = get_stats()
        return {"success": True, "data": stats, "error": None}, 200
    except Exception as e:
        app.logger.error(f"Error fetching data from Supabase: {e}")
        return {"success": False, "data": [], "error": f"Failed to fetch data"}, 500