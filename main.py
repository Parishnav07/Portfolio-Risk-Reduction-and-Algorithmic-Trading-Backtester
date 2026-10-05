
import sys
import pandas as pd
from typing import Optional
from pathlib import Path

from data_loader import DataLoader
from backtesting_engine import BacktestEngine, RiskAnalyzer
from visualization import Visualizer
from gemini_insights import GeminiInsights
from config import Config


class PortfolioBacktester:
    """Main application class for portfolio backtesting"""
    
    def __init__(self, data_file: str, initial_capital: float = None):
        """
        Initialize Portfolio Backtester
        
        Args:
            data_file: Path to CSV file with stock data
            initial_capital: Initial capital for backtesting
        """
        self.data_file = data_file
        self.initial_capital = initial_capital or Config.DEFAULT_INITIAL_CAPITAL
        self.data = None
        self.results = None
        self.visualizer = Visualizer()
        
        try:
            self.gemini = GeminiInsights()
            self.ai_enabled = True
        except Exception as e:
            print(f"⚠ AI insights disabled: {str(e)}")
            self.ai_enabled = False
    
    def load_and_prepare_data(self):
        """Load and preprocess data"""
        print("\n" + "="*60)
        print("LOADING DATA")
        print("="*60)
        
        loader = DataLoader(self.data_file)
        loader.load_data()
        loader.validate_data()
        self.data = loader.preprocess_data()
        
        # Print summary statistics
        stats = loader.get_summary_statistics()
        print(f"\nData Summary:")
        print(f"  Period: {stats['start_date'].date()} to {stats['end_date'].date()}")
        print(f"  Duration: {stats['duration_days']} days")
        print(f"  Total Return: {stats['total_return']:.2f}%")
        print(f"  Mean Daily Return: {stats['mean_returns']:.4f}%")
        print(f"  Volatility: {stats['std_returns']:.4f}%")
        
        return self.data
    
    def run_backtests(self):
        """Run all backtesting strategies"""
        if self.data is None:
            raise ValueError("Data not loaded. Call load_and_prepare_data() first.")
        
        print("\n" + "="*60)
        print("RUNNING BACKTESTS")
        print("="*60)
        
        engine = BacktestEngine(self.data, self.initial_capital)
        self.results = engine.run_all_strategies()
        
        # Print summary
        print("\n" + engine.generate_summary_report())
        
        return self.results
    
    def generate_visualizations(self, output_dir: str = "output"):
        """Generate all visualizations"""
        if self.results is None:
            raise ValueError("No results. Run backtests first.")
        
        print("\n" + "="*60)
        print("GENERATING VISUALIZATIONS")
        print("="*60)
        
        # Create output directory
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Strategy comparison
        engine = BacktestEngine(self.data, self.initial_capital)
        engine.results = self.results
        comparison_df = engine.get_comparison_table()
        
        self.visualizer.plot_strategy_comparison(
            comparison_df,
            save_path=str(output_path / "strategy_comparison.png")
        )
        
        # Best strategy details
        best_name, best_result = engine.get_best_strategy()
        
        if 'portfolio' in best_result:
            self.visualizer.plot_portfolio_value(
                best_result,
                save_path=str(output_path / "portfolio_value.png")
            )
            
            self.visualizer.plot_drawdown_chart(
                best_result['portfolio']['Total'],
                save_path=str(output_path / "drawdown_chart.png")
            )
            
            self.visualizer.plot_returns_distribution(
                best_result,
                save_path=str(output_path / "returns_distribution.png")
            )
        
        # Technical indicators
        self.visualizer.plot_technical_indicators(
            self.data,
            save_path=str(output_path / "technical_indicators.png")
        )
        
        # Interactive dashboard
        self.visualizer.create_interactive_dashboard(
            self.results,
            save_path=str(output_path / "dashboard.html")
        )
        
        print(f"\n✓ Visualizations saved to '{output_dir}' directory")
    
    def generate_ai_insights(self):
        """Generate AI-powered insights"""
        if not self.ai_enabled:
            print("\n⚠ AI insights not available (Gemini API key not configured)")
            return
        
        if self.results is None:
            raise ValueError("No results. Run backtests first.")
        
        print("\n" + "="*60)
        print("GENERATING AI INSIGHTS")
        print("="*60)
        
        # Strategy analysis
        print("\n📊 Analyzing strategy performance...")
        strategy_insights = self.gemini.generate_strategy_analysis(self.results)
        
        print("\n" + "="*60)
        print("AI STRATEGY ANALYSIS")
        print("="*60)
        print(strategy_insights)
        
        # Risk analysis
        engine = BacktestEngine(self.data, self.initial_capital)
        engine.results = self.results
        best_name, best_result = engine.get_best_strategy()
        
        if 'portfolio' in best_result:
            risk_analyzer = RiskAnalyzer(best_result['portfolio']['Returns'])
            risk_metrics = risk_analyzer.risk_metrics_summary()
            
            print("\n📊 Analyzing risk metrics...")
            risk_insights = self.gemini.generate_risk_analysis(risk_metrics)
            
            print("\n" + "="*60)
            print("AI RISK ANALYSIS")
            print("="*60)
            print(risk_insights)
        
        # Market commentary
        print("\n📊 Generating market commentary...")
        market_commentary = self.gemini.generate_market_commentary(self.data)
        
        print("\n" + "="*60)
        print("AI MARKET COMMENTARY")
        print("="*60)
        print(market_commentary)
        
        return {
            'strategy_insights': strategy_insights,
            'risk_insights': risk_insights if 'portfolio' in best_result else None,
            'market_commentary': market_commentary
        }
    
    def export_results(self, output_dir: str = "output"):
        """Export results to files"""
        if self.results is None:
            raise ValueError("No results to export")
        
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)
        
        # Export comparison table
        engine = BacktestEngine(self.data, self.initial_capital)
        engine.results = self.results
        comparison_df = engine.get_comparison_table()
        comparison_df.to_csv(output_path / "strategy_comparison.csv", index=False)
        
        # Export summary report
        report = engine.generate_summary_report()
        with open(output_path / "summary_report.txt", 'w') as f:
            f.write(report)
        
        print(f"\n✓ Results exported to '{output_dir}' directory")
    
    def run_complete_analysis(self, generate_visuals: bool = True, 
                             generate_ai: bool = True,
                             export: bool = True):
        """
        Run complete analysis pipeline
        
        Args:
            generate_visuals: Generate visualizations
            generate_ai: Generate AI insights
            export: Export results
        """
        print("\n" + "="*60)
        print("PORTFOLIO RISK REDUCTION - BACKTESTING")
        print("="*60)
        
        # Load data
        self.load_and_prepare_data()
        
        # Run backtests
        self.run_backtests()
        
        # Generate visualizations
        if generate_visuals:
            self.generate_visualizations()
        
        # Generate AI insights
        if generate_ai and self.ai_enabled:
            self.generate_ai_insights()
        
        # Export results
        if export:
            self.export_results()
        
        print("\n" + "="*60)
        print("✓ ANALYSIS COMPLETE")
        print("="*60)


def main():
    """Main entry point"""
    import argparse
    
    parser = argparse.ArgumentParser(
        description='Portfolio Risk Reduction - Backtesting Application'
    )
    parser.add_argument(
        'data_file',
        help='Path to CSV file with historical stock data'
    )
    parser.add_argument(
        '--capital',
        type=float,
        default=Config.DEFAULT_INITIAL_CAPITAL,
        help=f'Initial capital (default: ${Config.DEFAULT_INITIAL_CAPITAL:,.0f})'
    )
    parser.add_argument(
        '--no-visuals',
        action='store_true',
        help='Skip visualization generation'
    )
    parser.add_argument(
        '--no-ai',
        action='store_true',
        help='Skip AI insights generation'
    )
    parser.add_argument(
        '--no-export',
        action='store_true',
        help='Skip results export'
    )
    parser.add_argument(
        '--output-dir',
        default='output',
        help='Output directory for results (default: output)'
    )
    
    args = parser.parse_args()
    
    # Check if data file exists
    if not Path(args.data_file).exists():
        print(f"Error: Data file '{args.data_file}' not found")
        sys.exit(1)
    
    # Run analysis
    backtester = PortfolioBacktester(args.data_file, args.capital)
    backtester.run_complete_analysis(
        generate_visuals=not args.no_visuals,
        generate_ai=not args.no_ai,
        export=not args.no_export
    )


if __name__ == "__main__":
    # Example usage
    print("Portfolio Risk Reduction - Backtesting Application")
    print("\nUsage:")
    print("  python main.py <data_file.csv>")
    print("\nExample:")
    print("  python main.py sample_data/stock_data.csv --capital 100000")
    print("\nFor help:")
    print("  python main.py --help")
    
    # Uncomment to run directly
    # main()
