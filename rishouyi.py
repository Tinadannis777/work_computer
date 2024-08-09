import yfinance as yf
import pandas as pd

# 下载标普500指数数据
data = yf.download("^GSPC", start="2004-01-01", end="2024-12-31")

# 使用调整后的收盘价来计算日收益率
daily_returns = data['Adj Close'].pct_change().dropna()

# 将日收益率导出为Excel文件
daily_returns.to_excel("sp500_daily_returns.xlsx", sheet_name="Daily Returns")

print("日收益率已成功导出为 'sp500_daily_returns.xlsx'")
