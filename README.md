Stock Data Visualization

## Overview
Fetches real-time stock data using yfinance API and scrapes revenue data from web pages, then creates dual-axis visualizations comparing stock price vs revenue.

## Original Notebook
- `python final project.ipynb`

## Key Skills Demonstrated
- yfinance API for historical stock data
- Web scraping with BeautifulSoup & requests
- Data cleaning and merging
- Dual-axis matplotlib visualizations
- Time series analysis

## How to Run
```bash
pip install yfinance beautifulsoup4 requests pandas matplotlib
python main.py
```

## Outputs
- `tesla_stock_revenue.png` - Tesla share price & revenue
- `gamestop_stock_revenue.png` - GameStop share price & revenue

## Key Findings
- Stock prices can diverge significantly from revenue trends
- Visual correlation between revenue growth and investor sentiment
- Web scraping enables access to financial data not in APIs
