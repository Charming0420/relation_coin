#https://www.coingecko.com/

import pandas as pd
from pycoingecko import CoinGeckoAPI
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from requests.exceptions import RequestException

cg = CoinGeckoAPI()

# 請求用戶輸入分析的天數
days = int(input("請輸入分析的天數: "))

hottokens = []
# 用戶輸入代幣名稱
while True:
    new_token = input("輸入代幣名稱，輸入'done'完成: ")
    if new_token.lower() == 'done':
        break
    else:
        hottokens.append(new_token)

print("正在處理: ", hottokens)

def fetch_data(hottoken):
    # 嘗試多次請求以處理可能的網絡錯誤或API錯誤
    attempts = 0
    while attempts < 3:
        try:
            symbol = cg.get_coin_by_id(hottoken)['symbol'].upper()
            info = cg.get_coin_market_chart_by_id(hottoken, vs_currency='usd', days=days)
            prices = []
            if len(info['prices']) >= days:
                step = len(info['prices']) // days
                prices = [info['prices'][i * step][1] for i in range(days)]
            else:
                print(f"警告: {hottoken} 返回的數據點不足。")
            return symbol, prices
        except RequestException as e:
            attempts += 1
            print(f"嘗試 {attempts} 失敗，代幣 {hottoken}: {e}")
            if attempts == 3:
                return hottoken, []

HotTokens = {}
with ThreadPoolExecutor(max_workers=min(12, len(hottokens))) as executor:
    # 映射執行器到 fetch_data 函數並傳遞代幣
    futures = {executor.submit(fetch_data, token): token for token in hottokens}
    for future in as_completed(futures):
        symbol, prices = future.result()
        HotTokens[symbol] = prices
        print(f"完成處理 {symbol}")

df_HotTokens = pd.DataFrame(HotTokens)
df_corr = df_HotTokens.corr()

# 打印相關性矩陣
print("\n代幣間的相關性矩陣:")
print(df_corr)
