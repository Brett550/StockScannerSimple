from danel import DanelClient
from zacks import ZacksClient

#ZACKS TESTING
# zacks_client = ZacksClient()

# zacks_data = zacks_client.get_zacks_data('TSLA')
    
# print(zacks_data)

#ACTUAL APP

stocks = []

#first get danel scores
danel_client = DanelClient("https://apirest.danelfin.com")

#get stocks with 9 or 10 AI score
dan_stocks = danel_client.get_rankings()

#cross reference against Zacks to keep ones with Zack score of 1 or 2
zacks_client = ZacksClient()

for stock in dan_stocks:
    ticker = stock['ticker']
    zacks_data = zacks_client.get_zacks_data(ticker)

    # keep ones with rank of 1 or 2
    if zacks_data.get('zacksRank') in [1, 2]:
        stocks.append({
            'ticker': ticker,
            'name': zacks_data.get('name')
        })
