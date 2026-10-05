"""
Trading Algorithms Module
Implementation of various trading strategies including Markowitz Model, 
Moving Averages, Mean Reversion, Momentum, and Options strategies
"""
import numpy as np
import pandas as pd
from scipy.optimize import minimize
from typing import Dict, List, Tuple, Optional
import warnings

warnings.filterwarnings('ignore')


class MarkowitzOptimizer:
    """Modern Portfolio Theory - Markowitz Mean-Variance Optimization"""
    
    def __init__(self, returns_data: pd.DataFrame, risk_free_rate: float = 0.03):
        """
        Initialize Markowitz Optimizer
        
        Args:
            returns_data: DataFrame with returns for multiple assets
            risk_free_rate: Risk-free rate for Sharpe ratio calculation
        """
        self.returns = returns_data
        self.risk_free_rate = risk_free_rate
        self.mean_returns = returns_data.mean()
        self.cov_matrix = returns_data.cov()
        self.num_assets = len(returns_data.columns)
        
    def portfolio_stats(self, weights: np.ndarray) -> Tuple[float, float, float]:
        """
        Calculate portfolio statistics
        
        Args:
            weights: Array of portfolio weights
            
        Returns:
            Tuple of (returns, volatility, sharpe_ratio)
        """
        portfolio_return = np.sum(self.mean_returns * weights) * 252
        portfolio_volatility = np.sqrt(
            np.dot(weights.T, np.dot(self.cov_matrix * 252, weights))
        )
        sharpe_ratio = (portfolio_return - self.risk_free_rate) / portfolio_volatility
        
        return portfolio_return, portfolio_volatility, sharpe_ratio
    
    def negative_sharpe(self, weights: np.ndarray) -> float:
        """Negative Sharpe ratio for minimization"""
        return -self.portfolio_stats(weights)[2]
    
    def max_sharpe_ratio(self) -> Dict:
        """
        Find portfolio with maximum Sharpe ratio
        
        Returns:
            Dictionary with optimal weights and statistics
        """
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for _ in range(self.num_assets))
        initial_weights = np.array([1/self.num_assets] * self.num_assets)
        
        result = minimize(
            self.negative_sharpe,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        optimal_weights = result.x
        ret, vol, sharpe = self.portfolio_stats(optimal_weights)
        
        return {
            'weights': dict(zip(self.returns.columns, optimal_weights)),
            'expected_return': ret,
            'volatility': vol,
            'sharpe_ratio': sharpe
        }
    
    def min_volatility(self) -> Dict:
        """
        Find minimum volatility portfolio
        
        Returns:
            Dictionary with optimal weights and statistics
        """
        def portfolio_volatility(weights):
            return self.portfolio_stats(weights)[1]
        
        constraints = {'type': 'eq', 'fun': lambda x: np.sum(x) - 1}
        bounds = tuple((0, 1) for _ in range(self.num_assets))
        initial_weights = np.array([1/self.num_assets] * self.num_assets)
        
        result = minimize(
            portfolio_volatility,
            initial_weights,
            method='SLSQP',
            bounds=bounds,
            constraints=constraints
        )
        
        optimal_weights = result.x
        ret, vol, sharpe = self.portfolio_stats(optimal_weights)
        
        return {
            'weights': dict(zip(self.returns.columns, optimal_weights)),
            'expected_return': ret,
            'volatility': vol,
            'sharpe_ratio': sharpe
        }
    
    def efficient_frontier(self, num_portfolios: int = 50) -> pd.DataFrame:
        """
        Generate efficient frontier
        
        Args:
            num_portfolios: Number of portfolios to generate
            
        Returns:
            DataFrame with efficient frontier portfolios
        """
        results = []
        target_returns = np.linspace(
            self.mean_returns.min() * 252,
            self.mean_returns.max() * 252,
            num_portfolios
        )
        
        for target in target_returns:
            constraints = [
                {'type': 'eq', 'fun': lambda x: np.sum(x) - 1},
                {'type': 'eq', 'fun': lambda x: 
                 np.sum(self.mean_returns * x) * 252 - target}
            ]
            bounds = tuple((0, 1) for _ in range(self.num_assets))
            initial_weights = np.array([1/self.num_assets] * self.num_assets)
            
            result = minimize(
                lambda x: self.portfolio_stats(x)[1],
                initial_weights,
                method='SLSQP',
                bounds=bounds,
                constraints=constraints
            )
            
            if result.success:
                ret, vol, sharpe = self.portfolio_stats(result.x)
                results.append({
                    'Return': ret,
                    'Volatility': vol,
                    'Sharpe': sharpe
                })
        
        return pd.DataFrame(results)


class MovingAverageStrategy:
    """Moving Average Crossover Strategy"""
    
    def __init__(self, data: pd.DataFrame, short_window: int = 20, 
                 long_window: int = 50):
        """
        Initialize Moving Average Strategy
        
        Args:
            data: DataFrame with OHLCV data
            short_window: Short MA period
            long_window: Long MA period
        """
        self.data = data.copy()
        self.short_window = short_window
        self.long_window = long_window
        
    def generate_signals(self) -> pd.DataFrame:
        """
        Generate buy/sell signals
        
        Returns:
            DataFrame with signals
        """
        df = self.data.copy()
        
        # Calculate moving averages
        df['SMA_Short'] = df['Close'].rolling(window=self.short_window).mean()
        df['SMA_Long'] = df['Close'].rolling(window=self.long_window).mean()
        
        # Generate signals
        df['Signal'] = 0
        df.loc[df['SMA_Short'] > df['SMA_Long'], 'Signal'] = 1  # Buy
        df.loc[df['SMA_Short'] < df['SMA_Long'], 'Signal'] = -1  # Sell
        
        # Position changes
        df['Position'] = df['Signal'].diff()
        
        return df.dropna()
    
    def backtest(self, initial_capital: float = 100000) -> Dict:
        """
        Backtest the strategy
        
        Args:
            initial_capital: Starting capital
            
        Returns:
            Dictionary with backtest results
        """
        df = self.generate_signals()
        
        # Proper portfolio tracking
        portfolio = pd.DataFrame(index=df.index)
        portfolio['Position'] = df['Signal']
        portfolio['Price'] = df['Close']
        
        # Calculate strategy returns
        portfolio['Strategy_Returns'] = portfolio['Position'].shift(1) * portfolio['Price'].pct_change()
        portfolio['Strategy_Returns'] = portfolio['Strategy_Returns'].fillna(0)
        
        # Calculate cumulative returns
        portfolio['Cumulative_Returns'] = (1 + portfolio['Strategy_Returns']).cumprod()
        portfolio['Total'] = initial_capital * portfolio['Cumulative_Returns']
        
        # Calculate metrics
        total_return = (portfolio['Total'].iloc[-1] / initial_capital - 1) * 100
        returns_std = portfolio['Strategy_Returns'].std()
        sharpe_ratio = (portfolio['Strategy_Returns'].mean() / returns_std * np.sqrt(252)) if returns_std > 0 else 0
        max_drawdown = ((portfolio['Total'] / portfolio['Total'].cummax()) - 1).min() * 100
        
        return {
            'strategy': 'Moving Average Crossover',
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'final_value': portfolio['Total'].iloc[-1],
            'portfolio': portfolio,
            'signals': df
        }


class MomentumStrategy:
    """Momentum-based Trading Strategy"""
    
    def __init__(self, data: pd.DataFrame, lookback_period: int = 20):
        """
        Initialize Momentum Strategy
        
        Args:
            data: DataFrame with OHLCV data
            lookback_period: Period for momentum calculation
        """
        self.data = data.copy()
        self.lookback_period = lookback_period
        
    def generate_signals(self) -> pd.DataFrame:
        """Generate momentum-based signals"""
        df = self.data.copy()
        
        # Calculate momentum
        df['Momentum'] = df['Close'].pct_change(periods=self.lookback_period)
        
        # Generate signals based on momentum
        df['Signal'] = 0
        df.loc[df['Momentum'] > 0.05, 'Signal'] = 1  #  positive 
        df.loc[df['Momentum'] < -0.05, 'Signal'] = -1  # 
        
        df['Position'] = df['Signal'].diff()
        
        return df.dropna()
    
    def backtest(self, initial_capital: float = 100000) -> Dict:
        """Backtest momentum strategy"""
        df = self.generate_signals()
        
        # Proper portfolio tracking
        portfolio = pd.DataFrame(index=df.index)
        portfolio['Position'] = df['Signal']
        portfolio['Price'] = df['Close']
        
        # Calculate strategy returns
        portfolio['Strategy_Returns'] = portfolio['Position'].shift(1) * portfolio['Price'].pct_change()
        portfolio['Strategy_Returns'] = portfolio['Strategy_Returns'].fillna(0)
        
        # Calculate cumulative returns
        portfolio['Cumulative_Returns'] = (1 + portfolio['Strategy_Returns']).cumprod()
        portfolio['Total'] = initial_capital * portfolio['Cumulative_Returns']
        
        # Calculate metrics
        total_return = (portfolio['Total'].iloc[-1] / initial_capital - 1) * 100
        returns_std = portfolio['Strategy_Returns'].std()
        sharpe_ratio = (portfolio['Strategy_Returns'].mean() / returns_std * np.sqrt(252)) if returns_std > 0 else 0
        max_drawdown = ((portfolio['Total'] / portfolio['Total'].cummax()) - 1).min() * 100
        
        return {
            'strategy': 'Momentum',
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'final_value': portfolio['Total'].iloc[-1],
            'portfolio': portfolio,
            'signals': df
        }


class MeanReversionStrategy:
    """Mean Reversion Strategy using Bollinger Bands"""
    
    def __init__(self, data: pd.DataFrame, window: int = 20, num_std: float = 2.0):
        """
        Initialize Mean Reversion Strategy
        
        Args:
            data: DataFrame with OHLCV data
            window: Window for moving average
            num_std: Number of standard deviations for bands
        """
        self.data = data.copy()
        self.window = window
        self.num_std = num_std
        
    def generate_signals(self) -> pd.DataFrame:
        """Generate mean reversion signals"""
        df = self.data.copy()
        
        # Calculate Bollinger Bands
        df['MA'] = df['Close'].rolling(window=self.window).mean()
        df['STD'] = df['Close'].rolling(window=self.window).std()
        df['Upper_Band'] = df['MA'] + (self.num_std * df['STD'])
        df['Lower_Band'] = df['MA'] - (self.num_std * df['STD'])
        
        # Generate signals
        df['Signal'] = 0
        df.loc[df['Close'] < df['Lower_Band'], 'Signal'] = 1  # Oversold - Buy
        df.loc[df['Close'] > df['Upper_Band'], 'Signal'] = -1  # Overbought - Sell
        
        df['Position'] = df['Signal'].diff()
        
        return df.dropna()
    
    def backtest(self, initial_capital: float = 100000) -> Dict:
        """Backtest mean reversion strategy"""
        df = self.generate_signals()
        
        # Proper portfolio tracking
        portfolio = pd.DataFrame(index=df.index)
        portfolio['Position'] = df['Signal']
        portfolio['Price'] = df['Close']
        
        # Calculate strategy returns
        portfolio['Strategy_Returns'] = portfolio['Position'].shift(1) * portfolio['Price'].pct_change()
        portfolio['Strategy_Returns'] = portfolio['Strategy_Returns'].fillna(0)
        
        # Calculate cumulative returns
        portfolio['Cumulative_Returns'] = (1 + portfolio['Strategy_Returns']).cumprod()
        portfolio['Total'] = initial_capital * portfolio['Cumulative_Returns']
        
        # Calculate metrics
        total_return = (portfolio['Total'].iloc[-1] / initial_capital - 1) * 100
        returns_std = portfolio['Strategy_Returns'].std()
        sharpe_ratio = (portfolio['Strategy_Returns'].mean() / returns_std * np.sqrt(252)) if returns_std > 0 else 0
        max_drawdown = ((portfolio['Total'] / portfolio['Total'].cummax()) - 1).min() * 100
        
        return {
            'strategy': 'Mean Reversion',
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'final_value': portfolio['Total'].iloc[-1],
            'portfolio': portfolio,
            'signals': df
        }


class RSIStrategy:
    """Relative Strength Index (RSI) Strategy"""
    
    def __init__(self, data: pd.DataFrame, period: int = 14, 
                 oversold: int = 30, overbought: int = 70):
        """
        Initialize RSI Strategy
        
        Args:
            data: DataFrame with OHLCV data
            period: RSI calculation period
            oversold: Oversold threshold
            overbought: Overbought threshold
        """
        self.data = data.copy()
        self.period = period
        self.oversold = oversold
        self.overbought = overbought
        
    def calculate_rsi(self, prices: pd.Series) -> pd.Series:
        """Calculate RSI"""
        delta = prices.diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=self.period).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=self.period).mean()
        rs = gain / loss
        rsi = 100 - (100 / (1 + rs))
        return rsi
    
    def generate_signals(self) -> pd.DataFrame:
        """Generate RSI-based signals"""
        df = self.data.copy()
        
        df['RSI'] = self.calculate_rsi(df['Close'])
        
        # Generate signals
        df['Signal'] = 0
        df.loc[df['RSI'] < self.oversold, 'Signal'] = 1  # Oversold - Buy
        df.loc[df['RSI'] > self.overbought, 'Signal'] = -1  # Overbought - Sell
        
        df['Position'] = df['Signal'].diff()
        
        return df.dropna()
    
    def backtest(self, initial_capital: float = 100000) -> Dict:
        """Backtest RSI strategy"""
        df = self.generate_signals()
        
        # Proper portfolio tracking
        portfolio = pd.DataFrame(index=df.index)
        portfolio['Position'] = df['Signal']
        portfolio['Price'] = df['Close']
        
        # Calculate strategy returns
        portfolio['Strategy_Returns'] = portfolio['Position'].shift(1) * portfolio['Price'].pct_change()
        portfolio['Strategy_Returns'] = portfolio['Strategy_Returns'].fillna(0)
        
        # Calculate cumulative returns
        portfolio['Cumulative_Returns'] = (1 + portfolio['Strategy_Returns']).cumprod()
        portfolio['Total'] = initial_capital * portfolio['Cumulative_Returns']
        
        # Calculate metrics
        total_return = (portfolio['Total'].iloc[-1] / initial_capital - 1) * 100
        returns_std = portfolio['Strategy_Returns'].std()
        sharpe_ratio = (portfolio['Strategy_Returns'].mean() / returns_std * np.sqrt(252)) if returns_std > 0 else 0
        max_drawdown = ((portfolio['Total'] / portfolio['Total'].cummax()) - 1).min() * 100
        
        return {
            'strategy': 'RSI',
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'final_value': portfolio['Total'].iloc[-1],
            'portfolio': portfolio,
            'signals': df
        }


class MACDStrategy:
    """Moving Average Convergence Divergence (MACD) Strategy"""
    
    def __init__(self, data: pd.DataFrame, fast_period: int = 12, 
                 slow_period: int = 26, signal_period: int = 9):
        """
        Initialize MACD Strategy
        
        Args:
            data: DataFrame with OHLCV data
            fast_period: Fast EMA period (default: 12)
            slow_period: Slow EMA period (default: 26)
            signal_period: Signal line EMA period (default: 9)
        """
        self.data = data.copy()
        self.fast_period = fast_period
        self.slow_period = slow_period
        self.signal_period = signal_period
        
    def calculate_macd(self, prices: pd.Series) -> Tuple[pd.Series, pd.Series, pd.Series]:
        """
        Calculate MACD, Signal line, and Histogram
        
        Args:
            prices: Price series
            
        Returns:
            Tuple of (MACD line, Signal line, Histogram)
        """
        # Calculate EMAs
        ema_fast = prices.ewm(span=self.fast_period, adjust=False).mean()
        ema_slow = prices.ewm(span=self.slow_period, adjust=False).mean()
        
        # MACD line
        macd_line = ema_fast - ema_slow
        
        # Signal line (EMA of MACD)
        signal_line = macd_line.ewm(span=self.signal_period, adjust=False).mean()
        
        # Histogram (difference between MACD and Signal)
        histogram = macd_line - signal_line
        
        return macd_line, signal_line, histogram
    
    def generate_signals(self) -> pd.DataFrame:
        """
        Generate MACD-based trading signals
        
        Returns:
            DataFrame with signals and MACD indicators
        """
        df = self.data.copy()
        
        # Calculate MACD components
        df['MACD'], df['MACD_Signal'], df['MACD_Histogram'] = self.calculate_macd(df['Close'])
        
        # Generate signals
        df['Signal'] = 0
        
        # Buy signal: MACD crosses above Signal line (bullish crossover)
        df.loc[df['MACD'] > df['MACD_Signal'], 'Signal'] = 1
        
        # Sell signal: MACD crosses below Signal line (bearish crossover)
        df.loc[df['MACD'] < df['MACD_Signal'], 'Signal'] = -1
        
        # Track position changes (actual crossovers)
        df['Position'] = df['Signal'].diff()
        
        return df.dropna()
    
    def backtest(self, initial_capital: float = 100000) -> Dict:
        """
        Backtest MACD strategy
        
        Args:
            initial_capital: Starting capital
            
        Returns:
            Dictionary with backtest results
        """
        df = self.generate_signals()
        
        # Proper portfolio tracking
        portfolio = pd.DataFrame(index=df.index)
        portfolio['Position'] = df['Signal']
        portfolio['Price'] = df['Close']
        
        # Calculate strategy returns
        portfolio['Strategy_Returns'] = portfolio['Position'].shift(1) * portfolio['Price'].pct_change()
        portfolio['Strategy_Returns'] = portfolio['Strategy_Returns'].fillna(0)
        
        # Calculate cumulative returns
        portfolio['Cumulative_Returns'] = (1 + portfolio['Strategy_Returns']).cumprod()
        portfolio['Total'] = initial_capital * portfolio['Cumulative_Returns']
        
        # Calculate metrics
        total_return = (portfolio['Total'].iloc[-1] / initial_capital - 1) * 100
        returns_std = portfolio['Strategy_Returns'].std()
        sharpe_ratio = (portfolio['Strategy_Returns'].mean() / returns_std * np.sqrt(252)) if returns_std > 0 else 0
        max_drawdown = ((portfolio['Total'] / portfolio['Total'].cummax()) - 1).min() * 100
        
        return {
            'strategy': 'MACD',
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'final_value': portfolio['Total'].iloc[-1],
            'portfolio': portfolio,
            'signals': df
        }


class BuyAndHoldStrategy:
    """Simple Buy and Hold Strategy for comparison"""
    
    def __init__(self, data: pd.DataFrame):
        """
        Initialize Buy and Hold Strategy
        
        Args:
            data: DataFrame with OHLCV data
        """
        self.data = data.copy()
        
    def backtest(self, initial_capital: float = 100000) -> Dict:
        """Backtest buy and hold strategy"""
        df = self.data.copy()
        
        # Buy on first day, hold till end
        shares = initial_capital / df['Close'].iloc[0]
        
        portfolio = pd.DataFrame(index=df.index)
        portfolio['Holdings'] = shares * df['Close']
        portfolio['Cash'] = 0
        portfolio['Total'] = portfolio['Holdings']
        portfolio['Strategy_Returns'] = portfolio['Total'].pct_change()
        portfolio['Strategy_Returns'] = portfolio['Strategy_Returns'].fillna(0)
        
        total_return = (portfolio['Total'].iloc[-1] / initial_capital - 1) * 100
        returns_std = portfolio['Strategy_Returns'].std()
        sharpe_ratio = (portfolio['Strategy_Returns'].mean() / returns_std * np.sqrt(252)) if returns_std > 0 else 0
        max_drawdown = ((portfolio['Total'] / portfolio['Total'].cummax()) - 1).min() * 100
        
        return {
            'strategy': 'Buy and Hold',
            'total_return': total_return,
            'sharpe_ratio': sharpe_ratio,
            'max_drawdown': max_drawdown,
            'final_value': portfolio['Total'].iloc[-1],
            'portfolio': portfolio
        }


if __name__ == "__main__":
    print("Trading Algorithms Module - Ready for use")
