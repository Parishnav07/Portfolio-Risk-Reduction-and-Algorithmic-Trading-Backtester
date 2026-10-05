"""
Example usage scripts for Portfolio Risk Reduction
"""

# Example 1: Basic Usage
def example_basic():
    """Basic backtesting example"""
    from main import PortfolioBacktester
    
    # Initialize with sample data
    backtester = PortfolioBacktester(
        data_file='sample_data/stock_data.csv',
        initial_capital=100000
    )
    
    # Run complete analysis
    backtester.run_complete_analysis()


# Example 2: Step-by-Step Analysis
def example_step_by_step():
    """Run analysis step by step"""
    from main import PortfolioBacktester
    
    backtester = PortfolioBacktester('sample_data/stock_data.csv')
    
    # Step 1: Load data
    data = backtester.load_and_prepare_data()
    print(f"Loaded {len(data)} rows of data")
    
    # Step 2: Run backtests
    results = backtester.run_backtests()
    
    # Step 3: Generate visualizations
    backtester.generate_visualizations(output_dir='my_results')
    
    # Step 4: Get AI insights
    insights = backtester.generate_ai_insights()
    
    # Step 5: Export results
    backtester.export_results(output_dir='my_results')


# Example 3: Custom Strategy
def example_custom_strategy():
    """Test a specific strategy"""
    from data_loader import DataLoader
    from algorithms import MovingAverageStrategy, MACDStrategy
    
    # Load data
    loader = DataLoader('sample_data/stock_data.csv')
    loader.load_data()
    loader.validate_data()
    data = loader.preprocess_data()
    
    # Create custom moving average strategy
    strategy = MovingAverageStrategy(
        data=data,
        short_window=10,  # Custom short period
        long_window=30    # Custom long period
    )
    
    # Backtest
    results = strategy.backtest(initial_capital=100000)
    
    print(f"Strategy: {results['strategy']}")
    print(f"Total Return: {results['total_return']:.2f}%")
    print(f"Sharpe Ratio: {results['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {results['max_drawdown']:.2f}%")
    
    # Test MACD Strategy
    print("\n" + "="*50)
    macd_strategy = MACDStrategy(
        data=data,
        fast_period=12,
        slow_period=26,
        signal_period=9
    )
    
    macd_results = macd_strategy.backtest(initial_capital=100000)
    
    print(f"Strategy: {macd_results['strategy']}")
    print(f"Total Return: {macd_results['total_return']:.2f}%")
    print(f"Sharpe Ratio: {macd_results['sharpe_ratio']:.2f}")
    print(f"Max Drawdown: {macd_results['max_drawdown']:.2f}%")


# Example 4: Portfolio Optimization
def example_portfolio_optimization():
    """Optimize portfolio across multiple assets"""
    from data_loader import load_multiple_assets
    from backtesting_engine import PortfolioOptimizer
    
    # Load multiple assets
    assets = load_multiple_assets({
        'AAPL': 'sample_data/AAPL_data.csv',
        'GOOGL': 'sample_data/GOOGL_data.csv',
        'MSFT': 'sample_data/MSFT_data.csv',
        'AMZN': 'sample_data/AMZN_data.csv',
    })
    
    # Create optimizer
    optimizer = PortfolioOptimizer(assets)
    
    # Find optimal portfolio (maximum Sharpe ratio)
    optimal = optimizer.optimize_portfolio(method='max_sharpe')
    
    print("\nOptimal Portfolio (Max Sharpe):")
    print("-" * 50)
    for asset, weight in optimal['weights'].items():
        print(f"{asset}: {weight*100:.2f}%")
    print(f"\nExpected Return: {optimal['annual_return']:.2f}%")
    print(f"Volatility: {optimal['annual_volatility']:.2f}%")
    print(f"Sharpe Ratio: {optimal['sharpe_ratio']:.2f}")
    
    # Find minimum volatility portfolio
    min_vol = optimizer.optimize_portfolio(method='min_volatility')
    
    print("\n\nMinimum Volatility Portfolio:")
    print("-" * 50)
    for asset, weight in min_vol['weights'].items():
        print(f"{asset}: {weight*100:.2f}%")
    print(f"\nExpected Return: {min_vol['annual_return']:.2f}%")
    print(f"Volatility: {min_vol['annual_volatility']:.2f}%")
    print(f"Sharpe Ratio: {min_vol['sharpe_ratio']:.2f}")


# Example 5: Risk Analysis
def example_risk_analysis():
    """Detailed risk analysis"""
    from data_loader import DataLoader
    from algorithms import BuyAndHoldStrategy
    from backtesting_engine import RiskAnalyzer
    
    # Load data
    loader = DataLoader('sample_data/stock_data.csv')
    loader.load_data()
    loader.validate_data()
    data = loader.preprocess_data()
    
    # Run simple buy and hold
    strategy = BuyAndHoldStrategy(data)
    results = strategy.backtest(100000)
    
    # Analyze risk
    analyzer = RiskAnalyzer(results['portfolio']['Returns'])
    metrics = analyzer.risk_metrics_summary()
    
    print("\nRisk Metrics:")
    print("-" * 50)
    for metric, value in metrics.items():
        print(f"{metric.replace('_', ' ').title()}: {value:.2f}")


# Example 6: AI Insights Only
def example_ai_insights():
    """Generate AI insights from results"""
    from main import PortfolioBacktester
    from gemini_insights import GeminiInsights
    
    # Run backtest
    backtester = PortfolioBacktester('sample_data/stock_data.csv')
    backtester.load_and_prepare_data()
    results = backtester.run_backtests()
    
    # Generate various AI insights
    gemini = GeminiInsights()
    
    print("\n" + "="*60)
    print("STRATEGY ANALYSIS")
    print("="*60)
    analysis = gemini.generate_strategy_analysis(results)
    print(analysis)
    
    print("\n" + "="*60)
    print("MARKET COMMENTARY")
    print("="*60)
    commentary = gemini.generate_market_commentary(backtester.data)
    print(commentary)


# Example 7: Compare Multiple Strategies
def example_strategy_comparison():
    """Compare all strategies"""
    from data_loader import DataLoader
    from backtesting_engine import BacktestEngine
    from visualization import Visualizer
    
    # Load data
    loader = DataLoader('sample_data/stock_data.csv')
    loader.load_data()
    loader.validate_data()
    data = loader.preprocess_data()
    
    # Run all strategies
    engine = BacktestEngine(data, initial_capital=100000)
    results = engine.run_all_strategies()
    
    # Get comparison
    comparison = engine.get_comparison_table()
    print("\n" + comparison.to_string())
    
    # Visualize
    vis = Visualizer()
    vis.plot_strategy_comparison(comparison, save_path='comparison.png')
    
    # Get best strategy
    best_name, best_result = engine.get_best_strategy()
    print(f"\n🏆 Winner: {best_name}")
    print(f"   Return: {best_result['total_return']:.2f}%")


# Example 8: Efficient Frontier
def example_efficient_frontier():
    """Plot efficient frontier for portfolio"""
    from data_loader import load_multiple_assets
    from algorithms import MarkowitzOptimizer
    from visualization import Visualizer
    
    # Load assets
    assets = load_multiple_assets({
        'AAPL': 'sample_data/AAPL_data.csv',
        'GOOGL': 'sample_data/GOOGL_data.csv',
        'MSFT': 'sample_data/MSFT_data.csv',
    })
    
    # Create returns dataframe
    import pandas as pd
    returns_dict = {name: df['Returns'] for name, df in assets.items()}
    returns_df = pd.DataFrame(returns_dict).dropna()
    
    # Calculate efficient frontier
    optimizer = MarkowitzOptimizer(returns_df)
    frontier = optimizer.efficient_frontier(num_portfolios=50)
    optimal = optimizer.max_sharpe_ratio()
    
    # Visualize
    vis = Visualizer()
    vis.plot_efficient_frontier(
        frontier,
        optimal_portfolio={
            'annual_return': optimal['expected_return'] * 100,
            'annual_volatility': optimal['volatility'] * 100
        },
        save_path='efficient_frontier.png'
    )


# Example 9: Custom AI Prompt
def example_custom_ai_prompt():
    """Use custom AI prompts"""
    from gemini_insights import GeminiInsights, PromptLibrary
    from main import PortfolioBacktester
    
    # Run backtest
    backtester = PortfolioBacktester('sample_data/stock_data.csv')
    backtester.load_and_prepare_data()
    results = backtester.run_backtests()
    
    # Initialize Gemini
    gemini = GeminiInsights()
    
    # Custom question
    custom_analysis = gemini.generate_custom_analysis(
        custom_prompt="What's the best strategy for a risk-averse investor?",
        context_data=str(results)
    )
    
    print("\nCustom AI Analysis:")
    print("="*60)
    print(custom_analysis)
    
    # Use prompt templates
    templates = PromptLibrary.get_prompt_templates()
    print("\n\nAvailable templates:")
    for name in templates.keys():
        print(f"  - {name}")


# Example 10: Data Preprocessing Only
def example_data_preprocessing():
    """Just load and preprocess data"""
    from data_loader import DataLoader
    
    loader = DataLoader('sample_data/stock_data.csv')
    
    # Load
    raw_data = loader.load_data()
    print(f"Raw data shape: {raw_data.shape}")
    
    # Validate
    loader.validate_data()
    
    # Preprocess
    processed_data = loader.preprocess_data()
    print(f"Processed data shape: {processed_data.shape}")
    
    # Get statistics
    stats = loader.get_summary_statistics()
    print("\nSummary Statistics:")
    for key, value in stats.items():
        print(f"  {key}: {value}")
    
    # Split train/test
    train, test = loader.split_train_test(train_ratio=0.8)
    print(f"\nTrain size: {len(train)}, Test size: {len(test)}")
    
    # Export processed data
    loader.export_processed_data('processed_data.csv')


if __name__ == "__main__":
    print("Portfolio Risk Reduction - Example Scripts")
    print("=" * 60)
    print("\nAvailable examples:")
    print("  1. example_basic()")
    print("  2. example_step_by_step()")
    print("  3. example_custom_strategy()")
    print("  4. example_portfolio_optimization()")
    print("  5. example_risk_analysis()")
    print("  6. example_ai_insights()")
    print("  7. example_strategy_comparison()")
    print("  8. example_efficient_frontier()")
    print("  9. example_custom_ai_prompt()")
    print("  10. example_data_preprocessing()")
    print("\nUsage:")
    print("  python -c 'from examples import example_basic; example_basic()'")
    print("\nOr run in interactive Python:")
    print("  >>> from examples import *")
    print("  >>> example_basic()")
