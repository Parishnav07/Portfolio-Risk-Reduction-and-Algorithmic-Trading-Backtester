# Quick Start Guide

## Portfolio Risk Reduction - Getting Started in 5 Minutes

### Step 1: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 2: Set Up Gemini API (Optional)
1. Get API key from: https://makersuite.google.com/app/apikey
2. Create `.env` file:
```bash
cp .env.example .env
```
3. Edit `.env` and add your key:
```
GEMINI_API_KEY=your_key_here
```

### Step 3: Generate Sample Data
```bash
python generate_sample_data.py
```

### Step 4: Run Backtest

**Option A - Web Interface (Easiest)**
```bash
streamlit run app.py
```
Then open http://localhost:8501 in your browser

**Option B - Command Line**
```bash
python main.py sample_data/stock_data.csv
```

### Step 5: View Results
Results are saved in the `output/` directory:
- Charts (PNG files)
- Interactive dashboard (HTML)
- Summary report (TXT)
- Comparison table (CSV)

## Common Commands

### Run with custom capital
```bash
python main.py sample_data/stock_data.csv --capital 50000
```

### Skip AI insights (faster)
```bash
python main.py sample_data/stock_data.csv --no-ai
```

### Only generate visuals, no AI or export
```bash
python main.py sample_data/stock_data.csv --no-ai --no-export
```

### Get help
```bash
python main.py --help
```

## Using Your Own Data

1. Prepare CSV with columns: `Timestamp, Open, High, Low, Close, Volume`
2. Run: `python main.py your_data.csv`

Example CSV format:
```csv
Timestamp,Open,High,Low,Close,Volume,Open Interest
2023-01-01,100.5,102.3,99.8,101.2,5000000,150000
2023-01-02,101.2,103.5,100.5,102.8,5500000,155000
```

## Troubleshooting

**"Module not found" error**
```bash
pip install -r requirements.txt
```

**"API key not found" warning**
- The app works without AI insights
- Or set up your Gemini API key in `.env`

**Data format error**
- Ensure CSV has required columns
- Check date format in Timestamp column

## What's Included

✅ 6 trading strategies (Moving Average, Momentum, RSI, etc.)  
✅ Risk analysis (VaR, Sharpe Ratio, Drawdown)  
✅ AI-powered insights (with Gemini API)  
✅ Interactive visualizations  
✅ Web interface and CLI  
✅ Sample data generator  

## Next Steps

1. ✅ Run first backtest with sample data
2. Try different strategies in the web interface
3. Upload your own stock data
4. Experiment with different time periods
5. Compare multiple strategies
6. Read AI insights for recommendations

Need help? Check the full README.md for detailed documentation.
