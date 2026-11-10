"""
Project 02: Stock Data Visualization
=====================================
This script fetches stock data using yfinance and visualizes 
historical share prices and revenue data for Tesla and GameStop.

Original notebook: python final project.ipynb

Author: Data Analysis Portfolio
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import requests
from bs4 import BeautifulSoup
try:
    import yfinance as yf
except ImportError:
    yf = None
    print('Warning: yfinance not installed. Install with: pip install yfinance')
import warnings

warnings.filterwarnings("ignore", category=FutureWarning)

# ================================================================================
# HELPER FUNCTIONS
# ================================================================================

def make_graph(stock_data, revenue_data, stock_name):
    """
    Create a dual-axis plot showing stock price and revenue over time.
    
    Parameters:
    - stock_data: DataFrame with Date and Close columns
    - revenue_data: DataFrame with Date and Revenue columns
    - stock_name: String name of the stock for title
    """
    # Filter data to match original notebook date ranges
    stock_data_specific = stock_data[stock_data.Date <= '2021-06-14'].copy()
    revenue_data_specific = revenue_data[revenue_data.Date <= '2021-04-30'].copy()
    
    fig, axes = plt.subplots(2, 1, figsize=(14, 10), sharex=True)
    
    # Stock price plot
    axes[0].plot(
        pd.to_datetime(stock_data_specific.Date), 
        stock_data_specific.Close.astype("float"), 
        label="Share Price", 
        color="blue"
    )
    axes[0].set_ylabel("Price ($US)")
    axes[0].set_title(f"{stock_name} - Historical Share Price")
    axes[0].legend()
    axes[0].grid(True, alpha=0.3)
    
    # Revenue plot
    axes[1].plot(
        pd.to_datetime(revenue_data_specific.Date), 
        revenue_data_specific.Revenue.astype("float"), 
        label="Revenue", 
        color="green"
    )
    axes[1].set_ylabel("Revenue ($US Millions)")
    axes[1].set_xlabel("Date")
    axes[1].set_title(f"{stock_name} - Historical Revenue")
    axes[1].legend()
    axes[1].grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig(f'{stock_name.lower()}_stock_revenue.png', dpi=150, bbox_inches='tight')
    print(f"Saved {stock_name.lower()}_stock_revenue.png")
    plt.close()

def fetch_tesla_data():
    """Fetch Tesla stock data and revenue data."""
    print("Fetching Tesla data...")
    
    if yf is None:
        print("  yfinance not available, returning sample data")
        return create_sample_stock_data('TSLA'), create_sample_revenue_data()
    
    # Stock data
    tsla = yf.Ticker('TSLA')
    tesla_data = tsla.history(period="max")
    tesla_data.reset_index(inplace=True)
    tesla_data['Date'] = tesla_data['Date'].dt.strftime('%Y-%m-%d')
    
    # Revenue data from web scraping
    url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/revenue.htm"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    tesla_revenue = pd.DataFrame(columns=["Date", "Revenue"])
    
    for row in soup.find("tbody").find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 2:
            date = cols[0].text.strip()
            revenue = cols[1].text.strip()
            tesla_revenue = pd.concat([
                tesla_revenue, 
                pd.DataFrame({"Date": [date], "Revenue": [revenue]})
            ], ignore_index=True)
    
    # Clean revenue data
    tesla_revenue["Revenue"] = tesla_revenue['Revenue'].str.replace(r'[$,]', '', regex=True)
    tesla_revenue.dropna(inplace=True)
    tesla_revenue = tesla_revenue[tesla_revenue['Revenue'] != ""]
    tesla_revenue['Revenue'] = pd.to_numeric(tesla_revenue['Revenue'], errors='coerce')
    tesla_revenue.dropna(inplace=True)
    
    return tesla_data, tesla_revenue

def fetch_gme_data():
    """Fetch GameStop stock data and revenue data."""
    print("Fetching GameStop data...")
    
    if yf is None:
        print("  yfinance not available, returning sample data")
        return create_sample_stock_data('GME'), create_sample_revenue_data()
    
    # Stock data
    gme = yf.Ticker("GME")
    gme_data = gme.history(period="max")
    gme_data.reset_index(inplace=True)
    gme_data['Date'] = gme_data['Date'].dt.strftime('%Y-%m-%d')
    
    # Revenue data from web scraping
    url = "https://cf-courses-data.s3.us.cloud-object-storage.appdomain.cloud/IBMDeveloperSkillsNetwork-PY0220EN-SkillsNetwork/labs/project/stock.html"
    response = requests.get(url)
    soup = BeautifulSoup(response.text, "html.parser")
    
    gme_revenue = pd.DataFrame(columns=["Date", "Revenue"])
    
    for row in soup.find("tbody").find_all("tr"):
        cols = row.find_all("td")
        if len(cols) >= 2:
            date = cols[0].text.strip()
            revenue = cols[1].text.strip()
            gme_revenue = pd.concat([
                gme_revenue, 
                pd.DataFrame({"Date": [date], "Revenue": [revenue]})
            ], ignore_index=True)
    
    # Clean revenue data
    gme_revenue["Revenue"] = gme_revenue['Revenue'].str.replace(r'[$,]', '', regex=True)
    gme_revenue.dropna(inplace=True)
    gme_revenue = gme_revenue[gme_revenue['Revenue'] != ""]
    gme_revenue['Revenue'] = pd.to_numeric(gme_revenue['Revenue'], errors='coerce')
    gme_revenue.dropna(inplace=True)
    
    return gme_data, gme_revenue

# ================================================================================
# MAIN EXECUTION
# ================================================================================

def create_sample_stock_data(symbol):
    """Create sample stock data for demo."""
    dates = pd.date_range('2020-01-01', periods=100, freq='D')
    np.random.seed(42)
    base = 100 if symbol == 'TSLA' else 20
    prices = base + np.cumsum(np.random.randn(100) * 2)
    df = pd.DataFrame({'Date': dates.strftime('%Y-%m-%d'), 'Close': prices})
    return df

def create_sample_revenue_data():
    """Create sample revenue data for demo."""
    dates = pd.date_range('2020-01-01', periods=20, freq='QE')
    np.random.seed(42)
    revenue = np.cumsum(np.random.uniform(1000, 5000, 20))
    df = pd.DataFrame({'Date': dates.strftime('%Y-%m-%d'), 'Revenue': revenue.astype(int)})
    return df

if __name__ == "__main__":
    print("=" * 60)
    print("PROJECT 02: STOCK DATA VISUALIZATION")
    print("=" * 60)
    
    try:
        # Fetch and visualize Tesla data
        print("\n[1] Processing Tesla (TSLA)...")
        tesla_stock, tesla_revenue = fetch_tesla_data()
        print(f"  Stock data shape: {tesla_stock.shape}")
        print(f"  Revenue data shape: {tesla_revenue.shape}")
        make_graph(tesla_stock, tesla_revenue, "Tesla")
        
        # Fetch and visualize GameStop data
        print("\n[2] Processing GameStop (GME)...")
        gme_stock, gme_revenue = fetch_gme_data()
        print(f"  Stock data shape: {gme_stock.shape}")
        print(f"  Revenue data shape: {gme_revenue.shape}")
        make_graph(gme_stock, gme_revenue, "GameStop")
        
        print("\n" + "=" * 60)
        print("VISUALIZATION COMPLETE")
        print("=" * 60)
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Note: This script requires internet connection to fetch live data.")
        print("Install required packages: pip install yfinance beautifulsoup4 requests")
