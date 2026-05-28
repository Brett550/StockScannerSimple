# StockScannerSimple

A small Python-based stock scanner that combines Danelfin ranking data and Zacks ratings, then generates a CSV report and sends it by email.

## Overview

`StockScannerSimple` is designed for users who want a minimal pipeline that:

- Fetches stock rankings from the Danelfin API
- Filters results to high-scoring tickers
- Enriches those tickers using a Zacks lookup through a local Node.js bridge
- Writes matching stocks to `stockReport.csv`
- Emails the report using SMTP credentials from environment variables

## Repository Layout

- `main.py` - orchestration script that executes the scanner workflow
- `danel.py` - Danelfin API client
- `zacks.py` - Node bridge invoker for Zacks data
- `csv_maker.py` - CSV generation utility
- `emailer.py` - SMTP email sender
- `stockReport.csv` - sample/output report file
- `requirements.txt` - Python dependencies
- `zacks-bridge/` - Node.js wrapper that calls `zacks-api`

## Prerequisites

- Python 3.11+ installed
- Node.js installed (for the Zacks bridge)
- A Danelfin API key
- An SMTP-capable email account and credentials

## Setup

1. Clone the repository or download the source.

2. Create a Python virtual environment and activate it:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

3. Install Python dependencies:

```powershell
python -m pip install -r requirements.txt
```

4. Install Node dependencies for the Zacks bridge:

```powershell
cd zacks-bridge
npm install
cd ..
```

5. Create a `.env` file in the repo root with the following values:

```text
DANELFIN_API_KEY=your_danelfin_api_key
EMAIL_ADDRESS=your_email@example.com
EMAIL_PASSWORD=your_smtp_password
TO_EMAIL=recipient@example.com
```

> If you are using Gmail, you may need an app password or enable SMTP access for the account.

## Running the Project

From the repository root, run:

```powershell
python main.py
```

The script will:

1. Fetch Danelfin rankings with `aiscore_min=9`
2. Call the Node.js `zacks-bridge` to resolve Zacks rank data
3. Produce `stockReport.csv`
4. Send the report as an email attachment

## What to Expect

- `stockReport.csv` will contain the filtered ticker data
- The email is sent using `smtp.gmail.com:465` by default
- If any API call fails, the script raises an exception and stops

## Customization Notes

- Adjust the Danelfin score filter in `main.py` or `danel.py`
- Change Zacks ranking logic in `main.py` if you want different thresholds
- Update `emailer.py` to use another SMTP server or delivery method

## Troubleshooting

- `node` must be available on the PATH for `zacks.py` to work
- Verify `zacks-bridge/index.js` can run independently if Zacks results fail
- Check `.env` values for typos and missing credentials

## Dependencies

- Python dependencies are listed in `requirements.txt`
- Node dependency: `zacks-api`
