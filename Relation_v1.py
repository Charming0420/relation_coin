#https://www.coingecko.com/

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from pycoingecko import CoinGeckoAPI
import time

sns.set_style('darkgrid')

cg = CoinGeckoAPI()

hottokens = ['near']  # keep 'ethereum' as default

# Ask the user for additional tokens
while True:
    new_token = input("輸入代幣名稱，輸入'done'完成: ")
    if new_token.lower() == 'done':
        break
    else:
        hottokens.append(new_token)

print("正在繪製 ", hottokens)
symbols = []
for hottoken in hottokens:
    time.sleep(1)
    symbol = cg.get_coin_by_id(hottoken)['symbol']
    symbols.append(symbol.upper())

symbols_ids = dict(zip(hottokens, symbols))

HotTokens = {}

for id in hottokens:
    time.sleep(5)
    info = cg.get_coin_market_chart_by_id(id, vs_currency='usd', days=90)
    price = []
    for i in range(0, 167):
        price.append(info['prices'][i][1])
    HotTokens[symbols_ids[id]] = price

df_HotTokens = pd.DataFrame(HotTokens)
df_corr = df_HotTokens.corr()

plt.figure(dpi=300)
plt.rcParams['font.sans-serif'] = 'SimHei'
plt.rcParams['axes.unicode_minus'] = False
cmap = sns.diverging_palette(0, 230, 90, 60, as_cmap=True)

sns.heatmap(data=df_corr, annot=True, fmt='.2f', vmin=-1, vmax=1, cmap=cmap, cbar_kws={"shrink": .8}, square=True)


plt.title('90 day\'s relation', loc='left')


# 显示热图

plt.show()
