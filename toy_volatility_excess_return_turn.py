import os
import numpy as np
import pandas as pd
import yfinance as yf

# 创建一个文件夹来保存结果
folder_name = "index_analysis_results"
if not os.path.exists(folder_name):
    os.makedirs(folder_name)

# 指数列表及其文件名
indices = {
    'SPY': 'SPY_ETF',
    '^GSPC': 'S&P_500',
    '^DJI': 'Dow_Jones_Industrial_Average',
    'DIA': 'DIA_ETF'
}

# 下载3个月期美国国债收益率数据
t_bill_data = yf.Ticker("^IRX")
t_bill_df = t_bill_data.history(start="2004-01-01", end="2024-12-31")

# 假设无风险利率是每日变化的，将每日无风险利率转换为每日利率
daily_risk_free_rate = t_bill_df['Close'].pct_change().dropna() / 252

# 滚动窗口大小
window = 20

# 循环处理每个指数
for ticker, filename in indices.items():
    # 下载指数数据
    data = yf.download(ticker, start="2004-01-01", end="2024-12-31")
    prices = data['Adj Close']

    # 计算每日收益率
    returns = prices.pct_change().dropna()

    # 创建一个空的DataFrame来存储结果
    columns = ['Volatility', 'Excess Return', 'Sharpe Ratio', 'Turnover Rate']
    results_df = pd.DataFrame(index=returns.index, columns=columns)

    for i in range(window, len(returns)):
        # 计算波动率
        volatility = np.std(returns.iloc[i-window:i])

        # 计算超额回报率
        excess_return = np.mean(returns.iloc[i-window:i]) - np.mean(daily_risk_free_rate.iloc[i-window:i])

        # 计算夏普比率
        sharpe_ratio = excess_return / volatility if volatility != 0 else np.nan

        # 计算换手率（假设用每日成交量变化率作为换手率的代理）
        if i > window:
            turnover_rate = (data['Volume'].iloc[i] - data['Volume'].iloc[i-1]) / data['Volume'].iloc[i-1]
        else:
            turnover_rate = np.nan

        # 存储结果
        results_df.iloc[i] = [volatility, excess_return, sharpe_ratio, turnover_rate]

    # 删除缺失值的行（前window天的结果）
    results_df = results_df.dropna()

    # 保存为Excel文件到指定文件夹
    file_path = os.path.join(folder_name, f"{filename}_volatility_excess_return_sharpe_ratio_with_turnover_rate.xlsx")
    results_df.to_excel(file_path)
