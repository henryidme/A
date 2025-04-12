import streamlit as st
import yfinance as yf
import pandas as pd

st.set_page_config(page_title="美股财报查询", layout="centered")

def get_financials(ticker):
    stock = yf.Ticker(ticker)

    try:
        financials = stock.financials
        balance_sheet = stock.balance_sheet
        cashflow = stock.cashflow
        info = stock.info
        latest_col = financials.columns[0]
    except Exception as e:
        return None, f"数据获取失败：{e}"

    try:
        data = {
            "公司名称": info.get("longName", ""),
            "股票代码": ticker,
            "财报年度": latest_col.year,
            "总收入 (Revenue)": financials.loc["Total Revenue", latest_col],
            "营业利润 (Operating Income)": financials.loc["Operating Income", latest_col],
            "净利润 (Net Income)": financials.loc["Net Income", latest_col],
            "每股收益 EPS": info.get("trailingEps", None),
            "总资产": balance_sheet.loc["Total Assets", latest_col],
            "总负债": balance_sheet.loc["Total Liab", latest_col],
            "股东权益": balance_sheet.loc["Total Stockholder Equity", latest_col],
            "经营现金流": cashflow.loc["Total Cash From Operating Activities", latest_col],
            "自由现金流 FCF": cashflow.loc["Free Cash Flow", latest_col] if "Free Cash Flow" in cashflow.index else "N/A"
        }

        df = pd.DataFrame(data.items(), columns=["指标", "数值"])
        return df, None
    except Exception as e:
        return None, f"解析失败：{e}"

# UI
st.title("📊 美股财报信息查询工具")
ticker_input = st.text_input("请输入美股代码（如 AAPL、MSFT、TSLA）:", value="AAPL")

if st.button("查询财报信息"):
    with st.spinner("正在加载数据..."):
        df, error = get_financials(ticker_input.upper())
        if error:
            st.error(error)
        else:
            st.success("查询成功！以下是财报关键信息：")
            st.dataframe(df)
