# app.py 示例
import yfinance as yf
import pandas as pd
from prophet import Prophet
import streamlit as st
import matplotlib.pyplot as plt
import plotly.graph_objects as go

# 函数：下载历史数据
def get_stock_data(stock_symbol, start_date, end_date):
    data = yf.download(stock_symbol, start=start_date, end=end_date)
    return data

# 函数：预测股票价格
def predict_stock_price(data, periods=365*3):  # 默认预测 3 年
    df = data[['Close']].reset_index()
    df = df.rename(columns={'Date': 'ds', 'Close': 'y'})
    
    # 使用 Prophet 进行预测
    model = Prophet(daily_seasonality=True)
    model.fit(df)
    
    # 创建未来数据
    future = model.make_future_dataframe(df, periods=periods)
    
    # 预测
    forecast = model.predict(future)
    return forecast

# 函数：绘制图表
def plot_forecast(forecast, stock_symbol):
    fig = go.Figure()
    
    # 原始数据
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat'], mode='lines', name='Predicted'))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_lower'], mode='lines', name='Lower Bound', line=dict(dash='dash')))
    fig.add_trace(go.Scatter(x=forecast['ds'], y=forecast['yhat_upper'], mode='lines', name='Upper Bound', line=dict(dash='dash')))
    
    fig.update_layout(
        title=f'{stock_symbol} 3-Year Price Prediction',
        xaxis_title='Date',
        yaxis_title='Price (USD)',
        showlegend=True
    )
    return fig

# Streamlit 交互
st.title("Stock Price Prediction Tool")

# 用户输入股票代码和日期范围
stock_symbol = st.text_input("Enter Stock Symbol (e.g. AAPL, TSLA, MSFT)", "AAPL")
start_date = st.date_input("Select Start Date", pd.to_datetime("2010-01-01"))
end_date = st.date_input("Select End Date", pd.to_datetime("2025-01-01"))

if st.button("Predict"):
    st.write(f"Fetching data for {stock_symbol} from {start_date} to {end_date}...")
    
    # 获取数据并预测
    data = get_stock_data(stock_symbol, start_date, end_date)
    forecast = predict_stock_price(data)
    
    # 绘制预测图表
    fig = plot_forecast(forecast, stock_symbol)
    st.plotly_chart(fig)
    
    st.write("Prediction completed!")

