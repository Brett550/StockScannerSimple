from danel import DanelClient
from zacks import ZacksClient
from csv_maker import CsvMaker
from emailer import send_email
from datetime import date

stocks = []

#first get stocks with danel scores 9 or 10
danel_client = DanelClient("https://apirest.danelfin.com")

print("Fetching DanelFin data...")
tickers = []

dan_stocks = danel_client.get_rankings()

for stock_group in dan_stocks.values():
    tickers.extend(stock_group.keys())

#cross reference against Zacks to keep ones with Zack score of 1 or 2
print("Cross referencing with Zacks...")
zacks_client = ZacksClient()

zacks_data = zacks_client.get_zacks_data(tickers)

for result in zacks_data:
    if not result.get('success'):
        continue

    data = result.get('data', {}) #response object from the Zacks API
    ticker = data.get('ticker')

    if data.get('zacksRank') in ['1', '2']:
        stocks.append({
            'ticker': ticker,
            'name': data.get('name')
        })

# save as CSV
print("Saving as CSV...")
csv_maker = CsvMaker()
csv_maker.make_csv(stocks, 'stockReport.csv')
# csv_maker.print_csv(stocks)

print("Emailing report...")
date = str(date.today())

send_email(
    subject="Stock Report " + date,
    body="Attached is stock scanner report for " + date,
    file_path="stockReport.csv"
)

print("Done!")