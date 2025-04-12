import streamlit as st
import yfinance as yf
import pandas as pd

def get_financial_summary(ticker_symbol):
    ticker = yf.Ticker(ticker_symbol)
    info = ticker.info

    try:
        financials = ticker.financials
        balance_sheet = ticker.balance_sheet
        cashflow = ticker.cashflow
        latest_col = financials.columns[0]
    except Exception as e:
        return {"错误": f"获取财报失败：{e}"}

    data = {
        "公司名称": info.get("longName", ""),
        "股票代码": ticker_symbol,
        "财报年度": latest_col.year if hasattr(latest_col, 'year') else str(latest_col),
        "总收入 (Revenue)": financials.loc["Total Revenue", latest_col] if "Total Revenue" in financials.index else "N/A",
        "营业利润 (Operating Income)": financials.loc["Operating Income", latest_col] if "Operating Income" in financials.index else "N/A",
        "净利润 (Net Income)": financials.loc["Net Income", latest_col] if "Net Income" in financials.index else "N/A",
        "每股收益 EPS": info.get("trailingEps", "N/A"),
        "总资产": balance_sheet.loc["Total Assets", latest_col] if "Total Assets" in balance_sheet.index else "N/A",
        "总负债": balance_sheet.loc["Total Liab", latest_col] if "Total Liab" in balance_sheet.index else "N/A",
        "股东权益": balance_sheet.loc["Total Stockholder Equity", latest_col] if "Total Stockholder Equity" in balance_sheet.index else "N/A",
        "经营现金流": cashflow.loc["Total Cash From Operating Activities", latest_col] if "Total Cash From Operating Activities" in cashflow.index else "N/A",
        "自由现金流 FCF": cashflow.loc["Free Cash Flow", latest_col] if "Free Cash Flow" in cashflow.index else "N/A"
    }

    return data

def main():
    st.set_page_config(page_title="美股财报查询", layout="centered")
    st.title("📊 美股财报关键信息查询工具")

    ticker_input = st.text_input("请输入美股股票代码（如 AAPL、MSFT）:", "AAPL")

    if st.button("获取财报"):
        with st.spinner("正在获取数据..."):
            result = get_financial_summary(ticker_input.upper())
            if "错误" in result:
                st.error(result["错误"])
            else:
                st.success("获取成功！")
                for k, v in result.items():
                    st.write(f"**{k}**: {v}")

if __name__ == "__main__":
    main()
