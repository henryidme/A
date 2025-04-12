import yfinance as yf
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# 获取股票数据
def get_stock_data(ticker):
    # 下载数据
    data = yf.download(ticker, start="2015-01-01", end="2024-01-01")
    print(data.columns)  # 打印列名检查数据
    # 保留 'Adj Close' 和 'Date' 列
    if 'Adj Close' in data.columns:
        data = data[['Adj Close']]
    else:
        # 如果没有 'Adj Close' 列，尝试使用 'Close' 列
        data = data[['Close']]
    
    # 重命名列名，Prophet 需要 'ds' 和 'y'
    data = data.rename(columns={'Adj Close': 'y'} if 'Adj Close' in data.columns else {'Close': 'y'})
    data['ds'] = data.index
    return data

# 处理数据：确保 'y' 列是数值型，并处理缺失值
def preprocess_data(df):
    # 将 'y' 列转为数值型
    df['y'] = pd.to_numeric(df['y'], errors='coerce')  # 非数值的转换为 NaN
    # 处理缺失值（填充缺失值）
    df['y'].fillna(df['y'].mean(), inplace=True)
    return df

# 使用 Prophet 模型进行股票预测
def predict_stock_price(df):
    # 创建并拟合 Prophet 模型
    model = Prophet()
    model.fit(df)
    
    # 创建未来的数据框架（预测未来 365 天）
    future = model.make_future_dataframe(df, periods=365)
    
    # 进行预测
    forecast = model.predict(future)
    
    # 可视化结果
    model.plot(forecast)
    plt.show()

    return forecast

# 主函数
def main():
    # 获取股票数据
    ticker = 'AAPL'  # 你可以替换成你想要分析的股票代码
    data = get_stock_data(ticker)
    
    # 预处理数据
    data = preprocess_data(data)
    
    # 进行预测
    forecast = predict_stock_price(data)
    
    # 显示预测结果
    print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

if __name__ == "__main__":
    main()
