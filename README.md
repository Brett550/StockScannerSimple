# StockScannerSimple

A small Python-based stock scanner that combines Danelfin ranking data and Zacks ratings, then generates a CSV report and sends it by email.

Inspired by my dad who vibe-coded an app just like this. The AI ended up generating many more files and making the logic and architecture way more complex than it needed to be. I decided to simplify it all while keeping the core functionality, resulting in this project!

## Overview

`StockScannerSimple` is designed for users who want a minimal pipeline that:

- Fetches stock rankings from the Danelfin API
- Filters results to high-scoring tickers
- Enriches those tickers using a Zacks lookup through a local Node.js bridge
- Writes matching stocks to `stockReport.csv`
- Emails the report using SMTP credentials from environment variables
- Exposes a Flask API for retrieving stored stock history and analytics

## Repository Layout

- `script/main.py` - orchestration script that executes the scanner workflow
- `script/danel.py` - Danelfin API client
- `script/zacks.py` - Node bridge invoker for Zacks data
- `script/csv_maker.py` - CSV generation utility
- `script/emailer.py` - SMTP email sender
- `script/requirements.txt` - Python dependencies for the scanner
- `script/zacks-bridge/` - Node.js wrapper that calls `zacks-api`
- `script/database/` - Handles Supabase connection for the script
- `api/app.py` - Flask API server exposing stock and analytics endpoints
- `api/services/service.py` - service layer for Supabase queries
- `api/db/supabase.py` - Supabase client configuration for API
- `api/requirements.txt` - Python dependencies for the API backend

## API Endpoints

The API server exposes the following endpoints:

- `GET /stocks`
  - Query params:
    - `limit` (default `100`, max `100`)
    - `offset` (default `0`)
    - `date` (optional, format `YYYY-MM-DD`)
  - Returns stored history rows from the `history` table.

- `GET /analytics/streaks`
  - Returns ticker streak analytics from the `ticker_streaks_noweekends` table.

- `GET /analytics/newly_added`
  - Returns tickers that appeared in today's scan that were not in yesterday's

- `GET /analytics/newly_removed`
  - Returns ticker that were in yesterday's scan but not in today's

Responses are returned as JSON with the shape:

```json
{
  "success": true,
  "data": [ ... ],
  "error": null
}
```

## Prerequisites

- Python 3.11+ installed
- Node.js installed (for the Zacks bridge)
- A Danelfin API key
- Supabase credentials for the API backend
- An SMTP-capable email account and credentials

## Setup

1. Clone the repository or download the source.

2. Create a Python virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install Python dependencies for the scanner:

```powershell
python -m pip install -r script/requirements.txt
```

4. Install Node dependencies for the Zacks bridge:

```powershell
cd zacks-bridge
npm install
cd ..
```

5. Install the API backend dependencies:

```powershell
python -m pip install -r api/requirements.txt
```

6. Create a `.env` file in the repo root with the following values:

```text
DANELFIN_API_KEY=your_danelfin_api_key
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_smtp_password
TO_EMAIL=recipient@example.com
SUPABASE_URL=https://your-supabase-url
SUPABASE_KEY=your_supabase_anon_or_service_key
```

> If you are using Gmail, you may need an app password or enable SMTP access for the account.

## Running the Scanner

From the repository root, run:

```powershell
python script/main.py
```

The script will:

1. Fetch Danelfin rankings with `aiscore_min=9`
2. Call the Node.js `zacks-bridge` to resolve Zacks rank data
3. Produce `stockReport.csv`
4. Send the report as an email attachment

## Running the API

From the api folder, start the Flask API with:

```powershell
flask run
```

Then access the endpoints at:

- `http://127.0.0.1:5000/stocks`
- `http://127.0.0.1:5000/analytics/streaks`

## Customization Notes

- Adjust the Danelfin score filter in `main.py` or `danel.py`
- Change Zacks ranking logic in `main.py` if you want different thresholds
- Update `emailer.py` to use another SMTP server or delivery method
- Modify `api/services/service.py` to change the stock query or analytics behavior

## Troubleshooting

- `node` must be available on the PATH for `zacks.py` to work
- Verify `zacks-bridge/index.js` can run independently if Zacks results fail
- Check `.env` values for typos and missing credentials
- Ensure `SUPABASE_URL` and `SUPABASE_KEY` are set before starting the API

## Dependencies

- Python dependencies for the scanner are listed in `requirements.txt`
- Python dependencies for the API are listed in `api/requirements.txt`
- Node dependency: `zacks-api`
