# 🚀 HOW TO RUN THE PROJECT

## ✅ Setup Complete!

All dependencies are installed and sample data is generated. You're ready to go!

---

## 🎯 3 Ways to Run the Project

### **Option 1: Web Interface (EASIEST - Recommended)**

This is the best way to use the application with a beautiful UI.

```bash
streamlit run app.py
```

Then open your browser to: **http://localhost:8501**

**What you can do:**
- Upload your own CSV files
- Use pre-generated sample data
- Configure settings via sidebar
- Run backtests with one click
- View interactive charts
- Get AI-powered insights
- Download results

---

### **Option 2: Command Line Interface**

Run backtests directly from the terminal.

**Basic usage:**
```bash
python main.py sample_data/stock_data.csv
```

**With custom initial capital:**
```bash
python main.py sample_data/stock_data.csv --capital 50000
```

**Skip AI insights (faster):**
```bash
python main.py sample_data/stock_data.csv --no-ai
```

**All options:**
```bash
python main.py sample_data/stock_data.csv --capital 100000 --output-dir my_results --no-ai
```

**Get help:**
```bash
python main.py --help
```

---

### **Option 3: Python Script**

Use the application in your own Python scripts.

Create a file called `test_backtest.py`:

```python
from main import PortfolioBacktester

# Initialize backtester
backtester = PortfolioBacktester(
    data_file='sample_data/stock_data.csv',
    initial_capital=100000
)

# Run complete analysis
backtester.run_complete_analysis()
```

Then run:
```bash
python test_backtest.py
```

---

## 📊 What You'll Get

After running a backtest, you'll get:

### **Console Output:**
- Strategy comparison table
- Performance metrics
- Best strategy identification
- Summary statistics

### **Files in `output/` directory:**
- `strategy_comparison.csv` - Metrics table
- `summary_report.txt` - Full text report
- `portfolio_value.png` - Portfolio value chart
- `drawdown_chart.png` - Drawdown visualization
- `returns_distribution.png` - Returns histogram
- `technical_indicators.png` - Technical analysis
- `dashboard.html` - Interactive dashboard (open in browser)

### **AI Insights (if enabled):**
- Strategy performance analysis
- Risk assessment with recommendations
- Market commentary
- Trading suggestions

---

## 🎮 Quick Test Run

Try this right now to see it in action:

```bash
streamlit run app.py
```

1. App opens in browser
2. Sample data is already available
3. Click "🚀 Run Backtest" button
4. See results in seconds!

---

## 📁 Sample Data Available

The following sample datasets are ready to use:

- `sample_data/stock_data.csv` - Generic stock (2 years of daily data)
- `sample_data/AAPL_data.csv` - Apple stock simulation
- `sample_data/GOOGL_data.csv` - Google stock simulation
- `sample_data/MSFT_data.csv` - Microsoft stock simulation
- `sample_data/AMZN_data.csv` - Amazon stock simulation
- `sample_data/TSLA_data.csv` - Tesla stock simulation

---

## 🤖 AI Features (Optional)

To enable AI-powered insights:

1. Get a free API key from: https://makersuite.google.com/app/apikey
2. Create a `.env` file in the project root
3. Add your key: `GEMINI_API_KEY=your_key_here`

The app works fine without AI - you just won't get the insights section.

---

## 🔧 Troubleshooting

**Web app won't start?**
```bash
pip install streamlit
streamlit run app.py
```

**Import errors?**
```bash
pip install -r requirements.txt
```

**Need new sample data?**
```bash
python generate_sample_data.py
```

**Want to see examples?**
Check the `examples.py` file for 10 different usage examples.

---

## 📚 Documentation

- **README.md** - Complete documentation
- **QUICKSTART.md** - 5-minute quick start
- **USAGE_GUIDE.md** - Comprehensive tutorial
- **PROJECT_SUMMARY.md** - Technical overview
- **examples.py** - 10 working examples

---

## 🎯 Recommended First Steps

1. **Start the web app**: `streamlit run app.py`
2. **Use sample data** - already loaded
3. **Click "Run Backtest"**
4. **Explore the results** - charts, metrics, insights
5. **Try different strategies** - experiment with settings
6. **Upload your own data** - when ready

---

## ⚡ Quick Commands Cheat Sheet

```bash
# Start web interface (RECOMMENDED)
streamlit run app.py

# Run CLI backtest
python main.py sample_data/stock_data.csv

# With custom capital
python main.py sample_data/stock_data.csv --capital 50000

# Skip AI (faster)
python main.py sample_data/stock_data.csv --no-ai

# Generate new sample data
python generate_sample_data.py

# Get help
python main.py --help
```

---

## 🎉 You're Ready!

**Start now with:**
```bash
streamlit run app.py
```

Open http://localhost:8501 and enjoy backtesting! 📈

---

**Questions?** Check the other documentation files in this directory.
