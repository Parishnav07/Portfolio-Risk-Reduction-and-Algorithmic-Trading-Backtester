# Complete Usage Guide

## Portfolio Management Risk Reduction - Comprehensive Tutorial

---

## Table of Contents
1. [Installation](#installation)
2. [Quick Start](#quick-start)
3. [Data Preparation](#data-preparation)
4. [Running Backtests](#running-backtests)
5. [Understanding Results](#understanding-results)
6. [AI Insights](#ai-insights)
7. [Advanced Usage](#advanced-usage)
8. [Troubleshooting](#troubleshooting)

---

## Installation

### Step 1: Prerequisites
- Python 3.8 or higher
- pip (Python package manager)
- Internet connection (for Gemini API)

### Step 2: Automated Setup (Recommended)

**Windows:**
```bash
setup.bat
```

**Mac/Linux:**
```bash
chmod +x setup.sh
./setup.sh
```

### Step 3: Manual Setup

```bash
# Create virtual environment
python -m venv venv

# Activate it
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install packages
pip install -r requirements.txt

# Setup environment
cp .env.example .env
# Edit .env and add your Gemini API key
```

### Step 4: Get Gemini API Key (Optional)
1. Visit: https://makersuite.google.com/app/apikey
2. Sign in with Google account
3. Create API key
4. Add to `.env` file:
   ```
   GEMINI_API_KEY=your_key_here
   ```

---

## Quick Start

### Option 1: Web Interface (Easiest)

```bash
streamlit run app.py
```

1. Open browser to http://localhost:8501
2. Upload CSV file or use sample data
3. Configure settings in sidebar
4. Click "Run Backtest"
5. View results and insights

### Option 2: Command Line

```bash
# Generate sample data first
python generate_sample_data.py

# Run backtest
python main.py sample_data/stock_data.csv
```

### Option 3: Python Code

```python
from main import PortfolioBacktester

backtester = PortfolioBacktester('sample_data/stock_data.csv')
backtester.run_complete_analysis()
```

---

## Data Preparation

### Required Format

Your CSV must have these columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| Timestamp | datetime | Date/time | 2023-01-01 |
| Open | float | Opening price | 100.50 |
| High | float | Highest price | 102.30 |
| Low | float | Lowest price | 99.80 |
| Close | float | Closing price | 101.20 |
| Volume | int | Trading volume | 5000000 |
| Open Interest | int | Options OI (optional) | 150000 |

### Example CSV

```csv
Timestamp,Open,High,Low,Close,Volume,Open Interest
2023-01-01,100.5,102.3,99.8,101.2,5000000,150000
2023-01-02,101.2,103.5,100.5,102.8,5500000,155000
2023-01-03,102.8,104.1,101.9,103.5,6000000,160000
```

### Data Sources

**Free Sources:**
- Yahoo Finance (use yfinance library)
- Alpha Vantage
- Quandl
- IEX Cloud

**Sample Code to Download Data:**
```python
import yfinance as yf

# Download data
ticker = yf.Ticker("AAPL")
data = ticker.history(start="2022-01-01", end="2024-01-01")
data = data.reset_index()
data = data.rename(columns={'Date': 'Timestamp'})
data['Open Interest'] = 0  # Add if needed
data.to_csv('AAPL_data.csv', index=False)
```

---

## Running Backtests

### Basic Usage

```bash
python main.py your_data.csv
```

### With Custom Capital

```bash
python main.py your_data.csv --capital 50000
```

### Skip AI (Faster)

```bash
python main.py your_data.csv --no-ai
```

### Full Options

```bash
python main.py your_data.csv \
  --capital 100000 \
  --output-dir my_results \
  --no-ai \
  --no-export
```

### Python API

```python
from main import PortfolioBacktester

# Initialize
backtester = PortfolioBacktester(
    data_file='your_data.csv',
    initial_capital=100000
)

# Run steps individually
data = backtester.load_and_prepare_data()
results = backtester.run_backtests()
backtester.generate_visualizations(output_dir='results')
insights = backtester.generate_ai_insights()
backtester.export_results(output_dir='results')
```

---

## Understanding Results

### Console Output

```
==============================================================
PORTFOLIO BACKTESTING SUMMARY REPORT
==============================================================
Generated: 2024-01-15 10:30:45
Initial Capital: $100,000.00
Data Period: 2022-01-01 to 2024-01-01
Total Days: 731
==============================================================

STRATEGY PERFORMANCE:
--------------------------------------------------------------
           Strategy  Total Return (%)  Sharpe Ratio  Max Drawdown (%)
  Moving Average...              23.45          1.85            -12.34
          Momentum              18.92          1.52            -15.67
   Mean Reversion              15.34          1.23            -10.45
               RSI              21.56          1.67            -13.89
      Buy and Hold              19.45          1.42            -18.23
```

### Key Metrics Explained

**Total Return**: 
- Overall profit/loss percentage
- Higher is better
- 20%+ is excellent for annual returns

**Sharpe Ratio**: 
- Risk-adjusted return measure
- > 1.0 = Good
- > 2.0 = Very Good
- > 3.0 = Excellent

**Max Drawdown**: 
- Largest peak-to-trough decline
- Lower (less negative) is better
- < -20% = High risk
- < -10% = Moderate risk
- < -5% = Low risk

### Output Files

After running, check the `output/` directory:

1. **strategy_comparison.csv** - Metrics table
2. **summary_report.txt** - Full text report
3. **portfolio_value.png** - Value over time chart
4. **drawdown_chart.png** - Drawdown visualization
5. **returns_distribution.png** - Returns histogram
6. **technical_indicators.png** - Technical analysis
7. **dashboard.html** - Interactive dashboard

---

## AI Insights

### What You Get

1. **Strategy Analysis**
   - Performance comparison
   - Best strategy identification
   - Market condition suitability
   - Recommendations

2. **Risk Analysis**
   - Risk profile assessment
   - VaR/CVaR interpretation
   - Volatility analysis
   - Risk mitigation strategies

3. **Market Commentary**
   - Technical analysis
   - Trend assessment
   - Support/resistance levels
   - Trading opportunities

### Using AI Features

**In Web App:**
1. Check "Generate AI Insights"
2. Run backtest
3. View insights in expandable sections

**In CLI:**
```bash
python main.py data.csv  # AI enabled by default
python main.py data.csv --no-ai  # Skip AI
```

**In Python:**
```python
from gemini_insights import GeminiInsights

gemini = GeminiInsights()

# Strategy analysis
insights = gemini.generate_strategy_analysis(results)

# Risk analysis
risk_insights = gemini.generate_risk_analysis(risk_metrics)

# Market commentary
commentary = gemini.generate_market_commentary(data)

# Custom question
custom = gemini.generate_custom_analysis(
    custom_prompt="What's best for volatile markets?",
    context_data=str(results)
)
```

---

## Advanced Usage

### 1. Custom Strategy Parameters

```python
from algorithms import MovingAverageStrategy

strategy = MovingAverageStrategy(
    data=stock_data,
    short_window=10,  # Faster signals
    long_window=30    # Shorter period
)

results = strategy.backtest(initial_capital=100000)
```

### 2. Portfolio Optimization

```python
from data_loader import load_multiple_assets
from backtesting_engine import PortfolioOptimizer

# Load multiple stocks
assets = load_multiple_assets({
    'AAPL': 'data/AAPL.csv',
    'GOOGL': 'data/GOOGL.csv',
    'MSFT': 'data/MSFT.csv',
    'AMZN': 'data/AMZN.csv',
})

# Optimize
optimizer = PortfolioOptimizer(assets)

# Maximum Sharpe ratio
max_sharpe = optimizer.optimize_portfolio(method='max_sharpe')
print(f"Optimal weights: {max_sharpe['weights']}")

# Minimum volatility
min_vol = optimizer.optimize_portfolio(method='min_volatility')
print(f"Min vol weights: {min_vol['weights']}")
```

### 3. Risk Analysis

```python
from backtesting_engine import RiskAnalyzer

# Get portfolio returns
portfolio_returns = results['portfolio']['Returns']

# Analyze risk
analyzer = RiskAnalyzer(portfolio_returns)
metrics = analyzer.risk_metrics_summary()

print(f"VaR 95%: {metrics['var_95']:.2f}%")
print(f"CVaR 95%: {metrics['cvar_95']:.2f}%")
print(f"Max Drawdown: {metrics['max_drawdown']:.2f}%")
```

### 4. Efficient Frontier

```python
from algorithms import MarkowitzOptimizer
import pandas as pd

# Prepare returns
returns_dict = {name: df['Returns'] for name, df in assets.items()}
returns_df = pd.DataFrame(returns_dict).dropna()

# Calculate efficient frontier
optimizer = MarkowitzOptimizer(returns_df)
frontier = optimizer.efficient_frontier(num_portfolios=100)

# Plot
from visualization import Visualizer
vis = Visualizer()
vis.plot_efficient_frontier(frontier)
```

### 5. Custom Visualizations

```python
from visualization import Visualizer

vis = Visualizer(figsize=(16, 10))

# Price and signals
vis.plot_price_and_signals(
    data=signals_df,
    strategy_name='My Strategy',
    save_path='my_chart.png'
)

# Portfolio value
vis.plot_portfolio_value(
    results=backtest_results,
    save_path='portfolio.png'
)

# Interactive dashboard
vis.create_interactive_dashboard(
    results_dict=all_results,
    save_path='dashboard.html'
)
```

---

## Troubleshooting

### Common Issues

**1. "Module not found" error**
```bash
# Solution: Install dependencies
pip install -r requirements.txt
```

**2. "Gemini API key not found"**
```bash
# Solution: Set up .env file
cp .env.example .env
# Edit .env and add your key
```

**3. "Data validation failed"**
- Check CSV format matches required columns
- Ensure no missing values
- Verify date format in Timestamp column

**4. "High/Low/Open/Close relationship invalid"**
- Data preprocessing filters invalid rows
- High should be >= Low, Open, Close
- Low should be <= High, Open, Close

**5. Web app won't start**
```bash
# Solution: Check if Streamlit is installed
pip install streamlit
streamlit run app.py
```

**6. Slow performance**
- Use smaller date ranges
- Skip AI insights with --no-ai
- Reduce number of portfolios in efficient frontier

### Debug Mode

```python
# Enable detailed logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Then run your code
```

### Getting Help

1. Check README.md for full documentation
2. Review examples.py for code samples
3. Check PROJECT_SUMMARY.md for overview
4. Review error messages carefully
5. Ensure data format is correct

---

## Best Practices

### 1. Data Quality
- Use clean, validated data
- Check for gaps and outliers
- Ensure sufficient history (1+ years)

### 2. Strategy Selection
- Start with simple strategies
- Compare multiple approaches
- Consider market conditions

### 3. Risk Management
- Set appropriate stop losses
- Monitor drawdowns
- Diversify across strategies
- Don't risk more than you can afford

### 4. Backtesting
- Use out-of-sample testing
- Account for transaction costs
- Consider slippage
- Avoid overfitting

### 5. AI Insights
- Use as guidance, not gospel
- Verify recommendations
- Combine with own analysis
- Consider multiple perspectives

---

## Next Steps

1. ✅ Run first backtest with sample data
2. Try different strategies
3. Upload your own stock data
4. Experiment with parameters
5. Compare multiple time periods
6. Optimize portfolio allocation
7. Review AI insights
8. Implement risk management
9. Forward test strategies
10. Continuously improve

---

## Additional Resources

### Learn More About:

**Trading Strategies:**
- Moving Averages: https://www.investopedia.com/articles/active-trading/052014/how-use-moving-average-buy-stocks.asp
- RSI: https://www.investopedia.com/terms/r/rsi.asp
- Momentum: https://www.investopedia.com/trading/introduction-to-momentum-trading/

**Portfolio Theory:**
- Modern Portfolio Theory: https://www.investopedia.com/terms/m/modernportfoliotheory.asp
- Efficient Frontier: https://www.investopedia.com/terms/e/efficientfrontier.asp
- Sharpe Ratio: https://www.investopedia.com/terms/s/sharperatio.asp

**Risk Management:**
- Value at Risk: https://www.investopedia.com/terms/v/var.asp
- Drawdown: https://www.investopedia.com/terms/d/drawdown.asp
- Risk Metrics: https://www.investopedia.com/terms/r/riskmeasures.asp

---

## Appendix: Complete Command Reference

```bash
# Generate sample data
python generate_sample_data.py

# Basic backtest
python main.py data.csv

# Custom capital
python main.py data.csv --capital 50000

# Custom output directory
python main.py data.csv --output-dir results

# Skip visualizations
python main.py data.csv --no-visuals

# Skip AI insights
python main.py data.csv --no-ai

# Skip export
python main.py data.csv --no-export

# All options
python main.py data.csv --capital 100000 --output-dir my_results --no-ai

# Web interface
streamlit run app.py

# Get help
python main.py --help
```

---

**You're now ready to use the Portfolio Risk Reduction application! Happy backtesting! 📈**
