# Portfolio Management Risk Reduction

A comprehensive Python application for backtesting stock market algorithms, optimizing portfolio allocation, and generating AI-powered insights using the Gemini API.

## 🎯 Features

### Trading Strategies
- **Markowitz Mean-Variance Optimization**: Modern Portfolio Theory implementation
- **Moving Average Crossover**: Multiple timeframe options (20/50, 50/200)
- **Momentum Strategy**: Trade based on price momentum
- **Mean Reversion**: Bollinger Bands-based strategy
- **RSI Strategy**: Relative Strength Index signals
- **Buy & Hold**: Baseline comparison

### Risk Analysis
- Value at Risk (VaR) and Conditional VaR (CVaR)
- Maximum Drawdown analysis
- Sharpe Ratio calculation
- Volatility metrics
- Downside risk assessment

### AI-Powered Insights
- Strategy performance analysis using Gemini API
- Risk assessment and recommendations
- Market commentary and outlook
- Portfolio optimization suggestions
- Comparative strategy analysis

### Visualization
- Interactive Plotly dashboards
- Portfolio value tracking
- Drawdown charts
- Returns distribution
- Technical indicators
- Strategy comparison charts

### Web Interface
- Streamlit-based interactive web application
- Real-time backtesting
- Data upload and preview
- Interactive visualizations
- AI insights generation
- Results export

## 📋 Requirements

- Python 3.8+
- See `requirements.txt` for dependencies

## 🚀 Installation

1. **Clone or download this repository**

2. **Create a virtual environment** (recommended):
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies**:
```bash
pip install -r requirements.txt
```

4. **Configure environment variables**:
```bash
cp .env.example .env
```

Edit `.env` and add your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

Get your Gemini API key from: https://makersuite.google.com/app/apikey

## 📊 Data Format

Your CSV file should contain these columns:
- `Timestamp`: Date/time (e.g., "2023-01-01" or "2023-01-01 09:30:00")
- `Open`: Opening price
- `High`: Highest price
- `Low`: Lowest price
- `Close`: Closing price
- `Volume`: Trading volume
- `Open Interest`: (Optional) Options open interest

Example:
```csv
Timestamp,Open,High,Low,Close,Volume,Open Interest
2023-01-01,100.5,102.3,99.8,101.2,5000000,150000
2023-01-02,101.2,103.5,100.5,102.8,5500000,155000
```

## 🎮 Usage

### Option 1: Command Line Interface

Generate sample data:
```bash
python generate_sample_data.py
```

Run backtesting:
```bash
python main.py sample_data/stock_data.csv --capital 100000
```

Available options:
```bash
python main.py --help
```

### Option 2: Web Interface (Recommended)

Launch the Streamlit app:
```bash
streamlit run app.py
```

Then open your browser to `http://localhost:8501`

### Option 3: Python API

```python
from main import PortfolioBacktester

# Initialize backtester
backtester = PortfolioBacktester(
    data_file='sample_data/stock_data.csv',
    initial_capital=100000
)

# Run complete analysis
backtester.run_complete_analysis()

# Or run individual steps
backtester.load_and_prepare_data()
backtester.run_backtests()
backtester.generate_visualizations()
backtester.generate_ai_insights()
backtester.export_results()
```

## 📁 Project Structure

```
portfolio-risk-reduction/
├── config.py                 # Configuration settings
├── data_loader.py            # Data loading and preprocessing
├── algorithms.py             # Trading strategies implementation
├── backtesting_engine.py     # Backtesting framework
├── gemini_insights.py        # AI insights generation
├── visualization.py          # Plotting and charts
├── main.py                   # CLI application
├── app.py                    # Streamlit web app
├── generate_sample_data.py   # Sample data generator
├── requirements.txt          # Python dependencies
├── .env.example              # Environment variables template
├── README.md                 # This file
└── sample_data/              # Sample datasets
    ├── stock_data.csv
    ├── AAPL_data.csv
    ├── GOOGL_data.csv
    └── ...
```

## 🔧 Configuration

Edit `config.py` to customize:
- Risk-free rate
- Initial capital
- Transaction costs
- Moving average periods
- Risk management thresholds
- Visualization settings

## 📈 Example Output

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
           Strategy  Total Return (%)  Sharpe Ratio  Max Drawdown (%)  Final Value ($)
  Moving Average...              23.45          1.85            -12.34        123,450.00
          Momentum              18.92          1.52            -15.67        118,920.00
   Mean Reversion              15.34          1.23            -10.45        115,340.00
               RSI              21.56          1.67            -13.89        121,560.00
      Buy and Hold              19.45          1.42            -18.23        119,450.00

==============================================================
BEST PERFORMING STRATEGY: Moving Average (20/50)
==============================================================
Total Return: 23.45%
Sharpe Ratio: 1.85
Max Drawdown: -12.34%
Final Portfolio Value: $123,450.00
```

### Generated Files
- `output/strategy_comparison.csv` - Strategy metrics
- `output/summary_report.txt` - Detailed text report
- `output/portfolio_value.png` - Portfolio value chart
- `output/drawdown_chart.png` - Drawdown visualization
- `output/returns_distribution.png` - Returns histogram
- `output/technical_indicators.png` - Technical analysis charts
- `output/dashboard.html` - Interactive dashboard

## 🤖 AI Prompts Usage

The application uses sophisticated prompts to generate insights:

### Strategy Analysis
```python
gemini = GeminiInsights()
insights = gemini.generate_strategy_analysis(backtest_results)
```

### Risk Analysis
```python
risk_insights = gemini.generate_risk_analysis(risk_metrics)
```

### Market Commentary
```python
commentary = gemini.generate_market_commentary(stock_data)
```

### Custom Analysis
```python
custom_insights = gemini.generate_custom_analysis(
    custom_prompt="What's the best strategy for volatile markets?",
    context_data=str(backtest_results)
)
```

## 📚 Advanced Usage

### Portfolio Optimization

```python
from backtesting_engine import PortfolioOptimizer
from data_loader import load_multiple_assets

# Load multiple assets
assets_data = load_multiple_assets({
    'AAPL': 'sample_data/AAPL_data.csv',
    'GOOGL': 'sample_data/GOOGL_data.csv',
    'MSFT': 'sample_data/MSFT_data.csv'
})

# Optimize portfolio
optimizer = PortfolioOptimizer(assets_data)
optimal_weights = optimizer.optimize_portfolio(method='max_sharpe')

print(f"Optimal Weights: {optimal_weights['weights']}")
print(f"Expected Return: {optimal_weights['annual_return']:.2f}%")
print(f"Volatility: {optimal_weights['annual_volatility']:.2f}%")
print(f"Sharpe Ratio: {optimal_weights['sharpe_ratio']:.2f}")
```

### Custom Strategy

```python
from algorithms import MovingAverageStrategy

# Create custom strategy
strategy = MovingAverageStrategy(
    data=stock_data,
    short_window=10,
    long_window=30
)

# Generate signals
signals = strategy.generate_signals()

# Backtest
results = strategy.backtest(initial_capital=100000)
```

## 🔍 Troubleshooting

### Gemini API Issues
- Ensure your API key is correctly set in `.env`
- Check API quota limits
- Verify internet connection

### Data Loading Errors
- Ensure CSV format matches required columns
- Check for missing or invalid data
- Verify date format in Timestamp column

### Performance Issues
- Reduce date range for faster processing
- Disable AI insights for quicker results
- Use smaller datasets for testing

## 🤝 Contributing

Contributions are welcome! Areas for improvement:
- Additional trading strategies
- More technical indicators
- Enhanced risk metrics
- Machine learning integration
- Real-time data feeds
- Options pricing models

## 📝 License

This project is open source and available for educational and personal use.

## ⚠️ Disclaimer

This software is for educational and research purposes only. It should not be used as financial advice. Always conduct your own research and consult with financial professionals before making investment decisions. Past performance does not guarantee future results.

## 📧 Support

For issues, questions, or suggestions, please create an issue in the project repository.

## 🎓 Learning Resources

- [Modern Portfolio Theory](https://en.wikipedia.org/wiki/Modern_portfolio_theory)
- [Technical Analysis](https://www.investopedia.com/terms/t/technicalanalysis.asp)
- [Quantitative Trading](https://www.quantstart.com/)
- [Python for Finance](https://www.oreilly.com/library/view/python-for-finance/9781492024323/)

## 🚀 Next Steps

After running your first backtest:

1. **Experiment with different strategies**
2. **Optimize strategy parameters**
3. **Analyze AI insights carefully**
4. **Compare multiple time periods**
5. **Test with different assets**
6. **Implement risk management rules**
7. **Consider transaction costs**
8. **Validate on out-of-sample data**

Happy backtesting! 📈
