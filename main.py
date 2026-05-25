from danel import DanelClient
from zacks import ZacksClient
from csv_maker import CsvMaker

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

for ticker in tickers:
    zacks_data = zacks_client.get_zacks_data(ticker)
    zacks_rank = zacks_data.get('zacksRank') #API returns a string

    # keep ones with rank of 1 or 2
    if zacks_rank in ['1', '2']:
        stocks.append({
            'ticker': ticker,
            'name': zacks_data.get('name')
        })

# save as CSV
print("Saving as CSV...")
csv_maker = CsvMaker()
csv_maker.make_csv(stocks, 'stockReport.csv')