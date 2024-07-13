import yfinance as yf
import matplotlib.pyplot as plt
import pandas as pd

CSV=pd.read_csv("bats_symbols.csv")
symbols=list(CSV["Name"])
n=len(symbols)

for i in range(n):
    symbol=symbols[i]
    try:
        data = yf.download(symbol)
        data.to_csv("chart_data/"+symbol+".csv")
    except:
        pass
