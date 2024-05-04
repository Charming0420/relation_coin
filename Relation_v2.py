#https://www.coingecko.com/

import pandas as pd
from pycoingecko import CoinGeckoAPI
import time
import sys
from concurrent.futures import ThreadPoolExecutor

cg = CoinGeckoAPI()

# 請求用戶輸入分析的天數
days = int(input("請輸入分析的天數: "))
data_points = (days // 3) + 1  # 假設每三天抓取一次數據

hottokens = []
# 用戶輸入代幣名稱
while True:
    new_token = input("輸入代幣名稱，輸入'done'完成: ")
    if new_token.lower() == 'done':
        break
    else:
        hottokens.append(new_token)

print("正在處理: ", hottokens)

def fetch_symbol(hottoken):
    symbol = cg.get_coin_by_id(hottoken)['symbol']
    return hottoken, symbol.upper()

# 使用多線程獲取代幣符號
with ThreadPoolExecutor(max_workers=len(hottokens)) as executor:
    results = executor.map(fetch_symbol, hottokens)

symbols_ids = {}
for result in results:
    hottoken, symbol = result
    symbols_ids[hottoken] = symbol
    sys.stdout.write(f"\r獲取代幣符號: {hottoken} -> {symbol}\n")
    sys.stdout.flush()

HotTokens = {}

def fetch_prices(hottoken):
    info = cg.get_coin_market_chart_by_id(hottoken, vs_currency='usd', days=days)
    price = []
    for i in range(data_points):
        if i * 3 < len(info['prices']):
            price.append(info['prices'][i * 3][1])
    return symbols_ids[hottoken], price

# 使用多線程獲取價格數據
with ThreadPoolExecutor(max_workers=len(hottokens)) as executor:
    results = executor.map(fetch_prices, hottokens)

for result in results:
    symbol, prices = result
    HotTokens[symbol] = prices
    sys.stdout.write(f"\r完成處理 {symbol} 的價格數據\n")
    sys.stdout.flush()

df_HotTokens = pd.DataFrame(HotTokens)
df_corr = df_HotTokens.corr()

# Print the correlation matrix
print("代幣間的相關性矩陣:")
print(df_corr)
