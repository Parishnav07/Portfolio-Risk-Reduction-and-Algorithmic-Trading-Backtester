"""
Backtesting Engine
Comprehensive backtesting framework for evaluating trading strategies
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
from algorithms import (
    MovingAverageStrategy, MomentumStrategy, MeanReversionStrategy,
    RSIStrategy, MACDStrategy, BuyAndHoldStrategy
)
from config import Config


class BacktestEngine:
    """Engine for running and comparing multiple trading strategies"""
    
    def __init__(self, data: pd.DataFrame, initial_capital: float = None):
        """
        Initialize Backtesting Engine
        
        Args:
            data: DataFrame with OHLCV data
            initial_capital: Starting capital for backtesting
        """
        self.data = data
        self.initial_capital = initial_capital or Config.DEFAULT_INITIAL_CAPITAL
        self.results = {}
        
    def run_all_strategies(self) -> Dict:
        """
        Run all available strategies
        
        Returns:
            Dictionary with results for all strategies
        """
        strategies = [
            ('Moving Average (20/50)', MovingAverageStrategy(self.data, 20, 50)),
            ('Moving Average (50/200)', MovingAverageStrategy(self.data, 50, 200)),
            ('Momentum (20)', MomentumStrategy(self.data, 20)),
            ('Mean Reversion', MeanReversionStrategy(self.data)),
            ('RSI', RSIStrategy(self.data)),
            ('MACD (12/26/9)', MACDStrategy(self.data, 12, 26, 9)),
            ('Buy and Hold', BuyAndHoldStrategy(self.data))
        ]
        
        print("=" * 60)
        print("Running Backtests...")
        print("=" * 60)
        
        for name, strategy in strategies:
            try:
                result = strategy.backtest(self.initial_capital)
                self.results[name] = result
                print(f"✓ {name}: Return={result['total_return']:.2f}%, "
                      f"Sharpe={result['sharpe_ratio']:.2f}")
            except Exception as e:
                print(f"✗ {name}: Error - {str(e)}")
        
        return self.results
    
    def get_comparison_table(self) -> pd.DataFrame:
        """
        Create comparison table of all strategies
        
        Returns:
            DataFrame with strategy metrics
        """
        if not self.results:
            raise ValueError("No results available. Run backtests first.")
        
        comparison = []
        for name, result in self.results.items():
            comparison.append({
                'Strategy': name,
                'Total Return (%)': round(result['total_return'], 2),
                'Sharpe Ratio': round(result['sharpe_ratio'], 2),
                'Max Drawdown (%)': round(result['max_drawdown'], 2),
                'Final Value ($)': round(result['final_value'], 2)
            })
        
        df = pd.DataFrame(comparison)
        df = df.sort_values('Total Return (%)', ascending=False)
        
        return df
    
    def get_best_strategy(self) -> tuple:
        """
        Get best performing strategy
        
        Returns:
            Tuple of (strategy_name, results)
        """
        if not self.results:
            raise ValueError("No results available. Run backtests first.")
        
        best_name = max(self.results, key=lambda k: self.results[k]['total_return'])
        return best_name, self.results[best_name]
    
    def calculate_risk_metrics(self, returns: pd.Series) -> Dict:
        """
        Calculate comprehensive risk metrics
        
        Args:
            returns: Series of returns
            
        Returns:
            Dictionary with risk metrics
        """
        metrics = {
            'volatility': returns.std() * np.sqrt(252) * 100,
            'downside_volatility': returns[returns < 0].std() * np.sqrt(252) * 100,
            'var_95': np.percentile(returns, 5) * 100,
            'cvar_95': returns[returns <= np.percentile(returns, 5)].mean() * 100,
            'skewness': returns.skew(),
            'kurtosis': returns.kurtosis(),
            'win_rate': (returns > 0).sum() / len(returns) * 100,
            'avg_win': returns[returns > 0].mean() * 100,
            'avg_loss': returns[returns < 0].mean() * 100
        }
        
        return metrics
    
    def generate_summary_report(self) -> str:
        """
        Generate text summary report
        
        Returns:
            Formatted report string
        """
        if not self.results:
            return "No backtest results available."
        
        report = []
        report.append("\n" + "=" * 80)
        report.append("PORTFOLIO BACKTESTING SUMMARY REPORT")
        report.append("=" * 80)
        report.append(f"Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        report.append(f"Initial Capital: ${self.initial_capital:,.2f}")
        report.append(f"Data Period: {self.data.index[0]} to {self.data.index[-1]}")
        report.append(f"Total Days: {len(self.data)}")
        report.append("=" * 80)
        
        # Strategy Performance
        report.append("\nSTRATEGY PERFORMANCE:")
        report.append("-" * 80)
        
        comparison_df = self.get_comparison_table()
        report.append(comparison_df.to_string(index=False))
        
        # Best Strategy
        best_name, best_result = self.get_best_strategy()
        report.append("\n" + "=" * 80)
        report.append(f"BEST PERFORMING STRATEGY: {best_name}")
        report.append("=" * 80)
        report.append(f"Total Return: {best_result['total_return']:.2f}%")
        report.append(f"Sharpe Ratio: {best_result['sharpe_ratio']:.2f}")
        report.append(f"Max Drawdown: {best_result['max_drawdown']:.2f}%")
        report.append(f"Final Portfolio Value: ${best_result['final_value']:,.2f}")
        
        # Risk Metrics
        if 'portfolio' in best_result:
            report.append("\nRISK METRICS:")
            report.append("-" * 80)
            risk_metrics = self.calculate_risk_metrics(best_result['portfolio']['Returns'].dropna())
            for key, value in risk_metrics.items():
                report.append(f"{key.replace('_', ' ').title()}: {value:.2f}")
        
        report.append("\n" + "=" * 80)
        
        return "\n".join(report)
    
    def export_results(self, output_path: str):
        """
        Export results to CSV
        
        Args:
            output_path: Path for output file
        """
        if not self.results:
            raise ValueError("No results to export")
        
        comparison_df = self.get_comparison_table()
        comparison_df.to_csv(output_path, index=False)
        print(f"✓ Results exported to {output_path}")


class PortfolioOptimizer:
    """Portfolio optimization using multiple assets"""
    
    def __init__(self, assets_data: Dict[str, pd.DataFrame], 
                 risk_free_rate: float = None):
        """
        Initialize Portfolio Optimizer
        
        Args:
            assets_data: Dictionary mapping asset names to DataFrames
            risk_free_rate: Risk-free rate
        """
        self.assets_data = assets_data
        self.risk_free_rate = risk_free_rate or Config.RISK_FREE_RATE
        
        # Create returns DataFrame
        returns_dict = {}
        for name, df in assets_data.items():
            returns_dict[name] = df['Returns']
        
        self.returns_df = pd.DataFrame(returns_dict).dropna()
        
    def equal_weight_portfolio(self) -> Dict:
        """
        Create equal-weight portfolio
        
        Returns:
            Portfolio allocation dictionary
        """
        n_assets = len(self.assets_data)
        weights = {asset: 1/n_assets for asset in self.assets_data.keys()}
        
        return self._calculate_portfolio_metrics(weights)
    
    def _calculate_portfolio_metrics(self, weights: Dict) -> Dict:
        """Calculate portfolio metrics given weights"""
        weights_array = np.array([weights[asset] for asset in self.returns_df.columns])
        
        # Portfolio returns
        portfolio_returns = (self.returns_df * weights_array).sum(axis=1)
        
        # Metrics
        annual_return = portfolio_returns.mean() * 252 * 100
        annual_volatility = portfolio_returns.std() * np.sqrt(252) * 100
        sharpe_ratio = (annual_return/100 - self.risk_free_rate) / (annual_volatility/100)
        
        cumulative_returns = (1 + portfolio_returns).cumprod()
        max_drawdown = ((cumulative_returns / cumulative_returns.cummax()) - 1).min() * 100
        
        return {
            'weights': weights,
            'annual_return': annual_return,
            'annual_volatility': annual_volatility,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'portfolio_returns': portfolio_returns
        }
    
    def optimize_portfolio(self, method: str = 'max_sharpe') -> Dict:
        """
        Optimize portfolio allocation
        
        Args:
            method: 'max_sharpe' or 'min_volatility'
            
        Returns:
            Optimized portfolio dictionary
        """
        from algorithms import MarkowitzOptimizer
        
        optimizer = MarkowitzOptimizer(self.returns_df, self.risk_free_rate)
        
        if method == 'max_sharpe':
            result = optimizer.max_sharpe_ratio()
        elif method == 'min_volatility':
            result = optimizer.min_volatility()
        else:
            raise ValueError("Method must be 'max_sharpe' or 'min_volatility'")
        
        return {
            'weights': result['weights'],
            'annual_return': result['expected_return'] * 100,
            'annual_volatility': result['volatility'] * 100,
            'sharpe_ratio': result['sharpe_ratio']
        }


class RiskAnalyzer:
    """Advanced risk analysis for portfolios"""
    
    def __init__(self, portfolio_returns: pd.Series):
        """
        Initialize Risk Analyzer
        
        Args:
            portfolio_returns: Series of portfolio returns
        """
        self.returns = portfolio_returns.dropna()
        
    def value_at_risk(self, confidence: float = 0.95) -> float:
        """
        Calculate Value at Risk (VaR)
        
        Args:
            confidence: Confidence level
            
        Returns:
            VaR value
        """
        return np.percentile(self.returns, (1 - confidence) * 100)
    
    def conditional_var(self, confidence: float = 0.95) -> float:
        """
        Calculate Conditional VaR (CVaR/Expected Shortfall)
        
        Args:
            confidence: Confidence level
            
        Returns:
            CVaR value
        """
        var = self.value_at_risk(confidence)
        return self.returns[self.returns <= var].mean()
    
    def maximum_drawdown(self) -> Dict:
        """
        Calculate maximum drawdown and related metrics
        
        Returns:
            Dictionary with drawdown metrics
        """
        cumulative = (1 + self.returns).cumprod()
        running_max = cumulative.cummax()
        drawdown = (cumulative - running_max) / running_max
        
        max_dd = drawdown.min()
        max_dd_duration = 0
        current_dd_duration = 0
        
        for dd in drawdown:
            if dd < 0:
                current_dd_duration += 1
                max_dd_duration = max(max_dd_duration, current_dd_duration)
            else:
                current_dd_duration = 0
        
        return {
            'max_drawdown': max_dd * 100,
            'max_drawdown_duration': max_dd_duration,
            'current_drawdown': drawdown.iloc[-1] * 100
        }
    
    def risk_metrics_summary(self) -> Dict:
        """
        Comprehensive risk metrics
        
        Returns:
            Dictionary with all risk metrics
        """
        metrics = {
            'var_95': self.value_at_risk(0.95) * 100,
            'var_99': self.value_at_risk(0.99) * 100,
            'cvar_95': self.conditional_var(0.95) * 100,
            'cvar_99': self.conditional_var(0.99) * 100,
            'volatility': self.returns.std() * np.sqrt(252) * 100,
            'downside_volatility': self.returns[self.returns < 0].std() * np.sqrt(252) * 100,
            'skewness': self.returns.skew(),
            'kurtosis': self.returns.kurtosis()
        }
        
        metrics.update(self.maximum_drawdown())
        
        return metrics


if __name__ == "__main__":
    print("Backtesting Engine Module - Ready for use")
