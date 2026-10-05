"""
Visualization Module
Create charts, plots, and visual reports for backtesting results
"""
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import plotly.express as px
from config import Config

# Set style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")


class Visualizer:
    """Generate visualizations for backtesting results"""
    
    def __init__(self, figsize: tuple = None):
        """
        Initialize Visualizer
        
        Args:
            figsize: Figure size (width, height)
        """
        self.figsize = figsize or Config.FIGURE_SIZE
        
    def plot_price_and_signals(self, data: pd.DataFrame, strategy_name: str,
                               save_path: Optional[str] = None):
        """
        Plot price with buy/sell signals
        
        Args:
            data: DataFrame with price and signals
            strategy_name: Name of strategy
            save_path: Path to save figure
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figsize, 
                                       height_ratios=[3, 1])
        
        # Price plot
        ax1.plot(data.index, data['Close'], label='Price', linewidth=2)
        
        if 'SMA_Short' in data.columns:
            ax1.plot(data.index, data['SMA_Short'], 
                    label=f'SMA Short', alpha=0.7)
        if 'SMA_Long' in data.columns:
            ax1.plot(data.index, data['SMA_Long'], 
                    label=f'SMA Long', alpha=0.7)
        
        # Buy signals
        buy_signals = data[data['Position'] == 2]
        ax1.scatter(buy_signals.index, buy_signals['Close'], 
                   color='green', marker='^', s=100, label='Buy', zorder=5)
        
        # Sell signals
        sell_signals = data[data['Position'] == -2]
        ax1.scatter(sell_signals.index, sell_signals['Close'], 
                   color='red', marker='v', s=100, label='Sell', zorder=5)
        
        ax1.set_title(f'{strategy_name} - Price and Trading Signals', 
                     fontsize=14, fontweight='bold')
        ax1.set_ylabel('Price ($)', fontsize=12)
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        
        # Volume plot
        ax2.bar(data.index, data['Volume'], alpha=0.5, color='blue')
        ax2.set_ylabel('Volume', fontsize=12)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Chart saved to {save_path}")
        
        plt.show()
    
    def plot_portfolio_value(self, results: Dict, save_path: Optional[str] = None):
        """
        Plot portfolio value over time
        
        Args:
            results: Dictionary with backtest results
            save_path: Path to save figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        if 'portfolio' in results:
            portfolio = results['portfolio']
            ax.plot(portfolio.index, portfolio['Total'], 
                   linewidth=2, label='Portfolio Value')
            
            # Add horizontal line for initial capital
            initial_value = portfolio['Total'].iloc[0]
            ax.axhline(y=initial_value, color='gray', 
                      linestyle='--', alpha=0.5, label='Initial Capital')
            
            # Highlight drawdown periods
            cummax = portfolio['Total'].cummax()
            drawdown = (portfolio['Total'] - cummax) / cummax
            ax.fill_between(portfolio.index, portfolio['Total'], cummax, 
                           where=drawdown < 0, alpha=0.3, 
                           color='red', label='Drawdown')
        
        ax.set_title(f"{results['strategy']} - Portfolio Value Over Time", 
                    fontsize=14, fontweight='bold')
        ax.set_xlabel('Date', fontsize=12)
        ax.set_ylabel('Portfolio Value ($)', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Format y-axis as currency
        ax.yaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, p: f'${x:,.0f}'))
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Chart saved to {save_path}")
        
        plt.show()
    
    def plot_returns_distribution(self, results: Dict, 
                                  save_path: Optional[str] = None):
        """
        Plot returns distribution
        
        Args:
            results: Dictionary with backtest results
            save_path: Path to save figure
        """
        if 'portfolio' not in results:
            print("No portfolio data available")
            return
        
        returns = results['portfolio']['Returns'].dropna()
        
        fig, (ax1, ax2) = plt.subplots(1, 2, figsize=self.figsize)
        
        # Histogram
        ax1.hist(returns, bins=50, alpha=0.7, color='blue', edgecolor='black')
        ax1.axvline(returns.mean(), color='red', linestyle='--', 
                   linewidth=2, label=f'Mean: {returns.mean()*100:.2f}%')
        ax1.set_title('Returns Distribution', fontsize=12, fontweight='bold')
        ax1.set_xlabel('Returns', fontsize=10)
        ax1.set_ylabel('Frequency', fontsize=10)
        ax1.legend()
        ax1.grid(True, alpha=0.3)
        
        # Q-Q plot
        from scipy import stats
        stats.probplot(returns, dist="norm", plot=ax2)
        ax2.set_title('Q-Q Plot (Normality Test)', fontsize=12, fontweight='bold')
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Chart saved to {save_path}")
        
        plt.show()
    
    def plot_strategy_comparison(self, comparison_df: pd.DataFrame, 
                                save_path: Optional[str] = None):
        """
        Plot comparison of multiple strategies
        
        Args:
            comparison_df: DataFrame with strategy comparison
            save_path: Path to save figure
        """
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Total Return
        axes[0, 0].barh(comparison_df['Strategy'], 
                       comparison_df['Total Return (%)'], 
                       color='steelblue')
        axes[0, 0].set_title('Total Return Comparison', 
                            fontsize=12, fontweight='bold')
        axes[0, 0].set_xlabel('Return (%)')
        axes[0, 0].grid(True, alpha=0.3, axis='x')
        
        # Sharpe Ratio
        axes[0, 1].barh(comparison_df['Strategy'], 
                       comparison_df['Sharpe Ratio'], 
                       color='green')
        axes[0, 1].set_title('Sharpe Ratio Comparison', 
                            fontsize=12, fontweight='bold')
        axes[0, 1].set_xlabel('Sharpe Ratio')
        axes[0, 1].axvline(x=1, color='red', linestyle='--', alpha=0.5)
        axes[0, 1].grid(True, alpha=0.3, axis='x')
        
        # Max Drawdown
        axes[1, 0].barh(comparison_df['Strategy'], 
                       comparison_df['Max Drawdown (%)'], 
                       color='red')
        axes[1, 0].set_title('Maximum Drawdown Comparison', 
                            fontsize=12, fontweight='bold')
        axes[1, 0].set_xlabel('Max Drawdown (%)')
        axes[1, 0].grid(True, alpha=0.3, axis='x')
        
        # Risk-Return Scatter
        axes[1, 1].scatter(comparison_df['Max Drawdown (%)'].abs(), 
                          comparison_df['Total Return (%)'], 
                          s=200, alpha=0.6, c=comparison_df['Sharpe Ratio'],
                          cmap='RdYlGn')
        
        for idx, row in comparison_df.iterrows():
            axes[1, 1].annotate(row['Strategy'], 
                              (abs(row['Max Drawdown (%)']), 
                               row['Total Return (%)']),
                              fontsize=8, alpha=0.7)
        
        axes[1, 1].set_title('Risk vs Return', fontsize=12, fontweight='bold')
        axes[1, 1].set_xlabel('Max Drawdown (%) - Risk')
        axes[1, 1].set_ylabel('Total Return (%)')
        axes[1, 1].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Chart saved to {save_path}")
        
        plt.show()
    
    def plot_drawdown_chart(self, portfolio_values: pd.Series, 
                           save_path: Optional[str] = None):
        """
        Plot drawdown chart
        
        Args:
            portfolio_values: Series of portfolio values
            save_path: Path to save figure
        """
        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=self.figsize, 
                                       height_ratios=[2, 1], sharex=True)
        
        # Portfolio value
        ax1.plot(portfolio_values.index, portfolio_values, 
                linewidth=2, label='Portfolio Value')
        ax1.plot(portfolio_values.index, portfolio_values.cummax(), 
                linewidth=1, linestyle='--', alpha=0.5, 
                color='gray', label='Peak Value')
        ax1.set_title('Portfolio Value and Drawdown', 
                     fontsize=14, fontweight='bold')
        ax1.set_ylabel('Portfolio Value ($)', fontsize=12)
        ax1.legend(loc='best')
        ax1.grid(True, alpha=0.3)
        ax1.yaxis.set_major_formatter(plt.FuncFormatter(
            lambda x, p: f'${x:,.0f}'))
        
        # Drawdown
        drawdown = (portfolio_values / portfolio_values.cummax() - 1) * 100
        ax2.fill_between(drawdown.index, drawdown, 0, 
                        alpha=0.5, color='red')
        ax2.set_ylabel('Drawdown (%)', fontsize=12)
        ax2.set_xlabel('Date', fontsize=12)
        ax2.grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Chart saved to {save_path}")
        
        plt.show()
    
    def plot_efficient_frontier(self, efficient_frontier_df: pd.DataFrame,
                               optimal_portfolio: Optional[Dict] = None,
                               save_path: Optional[str] = None):
        """
        Plot efficient frontier
        
        Args:
            efficient_frontier_df: DataFrame with efficient frontier data
            optimal_portfolio: Dictionary with optimal portfolio data
            save_path: Path to save figure
        """
        fig, ax = plt.subplots(figsize=self.figsize)
        
        # Plot efficient frontier
        scatter = ax.scatter(efficient_frontier_df['Volatility'], 
                           efficient_frontier_df['Return'],
                           c=efficient_frontier_df['Sharpe'], 
                           cmap='viridis', s=50)
        
        # Mark optimal portfolio
        if optimal_portfolio:
            ax.scatter(optimal_portfolio['annual_volatility'], 
                      optimal_portfolio['annual_return'],
                      color='red', s=200, marker='*', 
                      label='Optimal Portfolio', zorder=5)
        
        ax.set_title('Efficient Frontier', fontsize=14, fontweight='bold')
        ax.set_xlabel('Volatility (Risk)', fontsize=12)
        ax.set_ylabel('Expected Return', fontsize=12)
        ax.legend(loc='best')
        ax.grid(True, alpha=0.3)
        
        # Add colorbar
        cbar = plt.colorbar(scatter, ax=ax)
        cbar.set_label('Sharpe Ratio', fontsize=10)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Chart saved to {save_path}")
        
        plt.show()
    
    def create_interactive_dashboard(self, results_dict: Dict, 
                                    save_path: Optional[str] = None):
        """
        Create interactive Plotly dashboard
        
        Args:
            results_dict: Dictionary with all results
            save_path: Path to save HTML file
        """
        # Create subplots
        fig = make_subplots(
            rows=2, cols=2,
            subplot_titles=('Portfolio Value', 'Returns Distribution',
                          'Drawdown', 'Strategy Comparison'),
            specs=[[{'type': 'scatter'}, {'type': 'histogram'}],
                   [{'type': 'scatter'}, {'type': 'bar'}]]
        )
        
        # Get first strategy for detailed plots
        first_strategy = list(results_dict.keys())[0]
        result = results_dict[first_strategy]
        
        if 'portfolio' in result:
            portfolio = result['portfolio']
            
            # Portfolio value
            fig.add_trace(
                go.Scatter(x=portfolio.index, y=portfolio['Total'],
                          mode='lines', name='Portfolio Value'),
                row=1, col=1
            )
            
            # Returns distribution
            fig.add_trace(
                go.Histogram(x=portfolio['Returns'].dropna(),
                           name='Returns', nbinsx=50),
                row=1, col=2
            )
            
            # Drawdown
            drawdown = (portfolio['Total'] / portfolio['Total'].cummax() - 1) * 100
            fig.add_trace(
                go.Scatter(x=drawdown.index, y=drawdown,
                          fill='tozeroy', name='Drawdown'),
                row=2, col=1
            )
        
        # Strategy comparison
        strategies = list(results_dict.keys())
        returns = [results_dict[s]['total_return'] for s in strategies]
        
        fig.add_trace(
            go.Bar(x=strategies, y=returns, name='Total Return'),
            row=2, col=2
        )
        
        fig.update_layout(
            title_text="Portfolio Backtesting Dashboard",
            height=800,
            showlegend=True
        )
        
        if save_path:
            fig.write_html(save_path)
            print(f"✓ Interactive dashboard saved to {save_path}")
        else:
            fig.show()
    
    def plot_technical_indicators(self, data: pd.DataFrame, 
                                  save_path: Optional[str] = None):
        """
        Plot technical indicators
        
        Args:
            data: DataFrame with technical indicators
            save_path: Path to save figure
        """
        fig, axes = plt.subplots(4, 1, figsize=(14, 12), sharex=True)
        
        # Price with Bollinger Bands
        axes[0].plot(data.index, data['Close'], label='Close', linewidth=2)
        if 'BB_Upper' in data.columns:
            axes[0].plot(data.index, data['BB_Upper'], 
                        label='BB Upper', linestyle='--', alpha=0.7)
            axes[0].plot(data.index, data['BB_Middle'], 
                        label='BB Middle', linestyle='--', alpha=0.7)
            axes[0].plot(data.index, data['BB_Lower'], 
                        label='BB Lower', linestyle='--', alpha=0.7)
            axes[0].fill_between(data.index, data['BB_Upper'], data['BB_Lower'],
                               alpha=0.1)
        axes[0].set_title('Price with Bollinger Bands', fontweight='bold')
        axes[0].set_ylabel('Price ($)')
        axes[0].legend(loc='best')
        axes[0].grid(True, alpha=0.3)
        
        # MACD
        if 'MACD' in data.columns:
            axes[1].plot(data.index, data['MACD'], label='MACD', linewidth=2)
            axes[1].plot(data.index, data['MACD_Signal'], 
                        label='Signal', linewidth=2)
            axes[1].bar(data.index, data['MACD'] - data['MACD_Signal'],
                       label='Histogram', alpha=0.3)
            axes[1].axhline(y=0, color='black', linestyle='-', linewidth=0.5)
            axes[1].set_title('MACD', fontweight='bold')
            axes[1].set_ylabel('MACD')
            axes[1].legend(loc='best')
            axes[1].grid(True, alpha=0.3)
        
        # RSI
        if 'RSI' in data.columns:
            axes[2].plot(data.index, data['RSI'], 
                        label='RSI', linewidth=2, color='purple')
            axes[2].axhline(y=70, color='red', linestyle='--', 
                          alpha=0.5, label='Overbought')
            axes[2].axhline(y=30, color='green', linestyle='--', 
                          alpha=0.5, label='Oversold')
            axes[2].fill_between(data.index, 30, 70, alpha=0.1)
            axes[2].set_title('RSI', fontweight='bold')
            axes[2].set_ylabel('RSI')
            axes[2].set_ylim(0, 100)
            axes[2].legend(loc='best')
            axes[2].grid(True, alpha=0.3)
        
        # Volume
        axes[3].bar(data.index, data['Volume'], alpha=0.5, color='blue')
        axes[3].set_title('Volume', fontweight='bold')
        axes[3].set_ylabel('Volume')
        axes[3].set_xlabel('Date')
        axes[3].grid(True, alpha=0.3)
        
        plt.tight_layout()
        
        if save_path:
            plt.savefig(save_path, dpi=300, bbox_inches='tight')
            print(f"✓ Chart saved to {save_path}")
        
        plt.show()


if __name__ == "__main__":
    print("Visualization Module - Ready for use")
