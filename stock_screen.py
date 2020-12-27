# -*- coding: utf-8 -*-
"""
Created on Fri Dec  4 19:28:58 2020

@author: Hogan
"""
from DataEnvelopmentAnalysis import *
import yfinance as yf
import yahoo_fin.stock_info as si
import datetime as dt
import time
import random

stocks=pd.read_excel('stock_screen.xlsx', 'Sheet1', encoding = 'gb18030')
stock_list_all = list(stocks['Consumer Discretionary'].dropna())
stock_list=random.sample(stock_list_all, min(len(stock_list_all),100)) # Randomly select stocks to avoid query limit

operating_names=['Beta','Operating Margin', 'Profit Margin', 'Revenue Per Share', 'Return on Assets','Return on Equity','Diluted EPS','Revenue Growth','Debt/Equity']
valuation_names=['Trailing P/E', 'Forward P/E','Enterprise Value/Revenue','Enterprise Value/EBITDA','Price/Book','PEG','Price/Sales']



"Data Extraction"
operating_stats=pd.DataFrame(data=np.nan, index=stock_list, columns=operating_names)
for i in range(len(stock_list)):
    print('Operating Stats: stock '+str(i)+' '+ str(stock_list[i]))
    df1 = si.get_stats(stock_list[i])
    if len(df1.index)<45:
        continue
    for j in range(len(operating_stats.columns)):
         operating_stats.iloc[i,j] = df1.loc[df1.iloc[:,0].str.contains(operating_stats.columns[j])].iloc[0,1]
pause=800
print('Pause to avoid query limit, resume at '+(dt.datetime.now()+dt.timedelta(0,pause)).strftime("%H:%M:%S"))
time.sleep(pause) # Add a pause period because yahoo finance has a query limit for valuation stats

valuation_stats=pd.DataFrame(data=np.nan, index=stock_list, columns=valuation_names)
for i in range(len(stock_list)):
    print('Valuation Stats: stock '+str(i)+' '+ str(stock_list[i]))
    df2 = si.get_stats_valuation(stock_list[i])
    if len(df1.index)<4:
        continue
    for j in range(len(valuation_stats.columns)):
         valuation_stats.iloc[i,j] = df2.loc[df2.iloc[:,0].str.contains(valuation_stats.columns[j])].iloc[0,1]


"Data Cleaning"
for i in range(len(stock_list)):
    
    for j in range(len(operating_stats.columns)):
        val=operating_stats.iloc[i,j]
        if isinstance(val,str):
            operating_stats.iloc[i,j]=float(val.replace('%', '').replace(',', ''))
        if isinstance(val,float):
            operating_stats.iloc[i,j]=val
            
    for j in range(len(valuation_stats.columns)):
        val=valuation_stats.iloc[i,j]
        if isinstance(val,str):
            valuation_stats.iloc[i,j]=float(val.replace('%', '').replace(',', '').replace('k',''))
        if isinstance(val,float):
            valuation_stats.iloc[i,j]=val
        


"DEA"
stock_info=operating_stats.join(valuation_stats[['Trailing P/E','Enterprise Value/Revenue','Enterprise Value/EBITDA','Price/Book','Price/Sales']]).dropna()

inputs=stock_info.iloc[:,:9]
outputs=stock_info.iloc[:,9:]

screen=DEA(inputs=inputs, outputs=outputs)

status, weights, efficiency = screen.solve()

"Most Undervalued Stocks"
temp=efficiency.sort_values(by=['Efficiency'],ascending=['True'])[:15]
res=pd.DataFrame(data=np.nan, index=temp.index, columns=['Efficiency', 'Market Cap'])
res['Efficiency']=temp.iloc[:,0]
for i in range(len(res.index)):
    val=si.get_stats_valuation(res.index[i])
    res.iloc[i,1]=val.loc[val.iloc[:,0].str.contains('Market Cap')].iloc[0,1]


print(res)