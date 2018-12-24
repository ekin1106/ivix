from datetime import datetime
import pandas as pd
from iVIX import calDayVIX
shibor_rate = pd.read_csv('shibor.csv',index_col=0,encoding='GBK')
options_data = pd.read_csv('options.csv',index_col=0,encoding='GBK')
tradeday = pd.read_csv('tradeday.csv',encoding='GBK')
true_ivix = pd.read_csv('tradeday.csv',encoding='GBK')
print(tradeday['DateTime'].iloc[-1])
lastestday =  tradeday['DateTime'].iloc[-1]
csvfile = open('ALLHISTORYIVIX.csv', 'a', newline='')
print(lastestday,calDayVIX(lastestday))