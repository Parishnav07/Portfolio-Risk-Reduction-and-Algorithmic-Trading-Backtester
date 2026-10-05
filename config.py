"""
Configuration settings for Portfolio Risk Reduction Application
"""
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Application configuration"""
    
    # API Keys
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    
    # Financial Parameters
    RISK_FREE_RATE = float(os.getenv('RISK_FREE_RATE', 0.03))
    DEFAULT_INITIAL_CAPITAL = float(os.getenv('DEFAULT_INITIAL_CAPITAL', 100000))
    
    # Backtesting Parameters
    TRANSACTION_COST = 0.001  # 0.1% per trade
    SLIPPAGE = 0.0005  # 0.05% slippage
    
    # Moving Average Periods
    MA_SHORT_PERIOD = 20
    MA_MEDIUM_PERIOD = 50
    MA_LONG_PERIOD = 200
    
    # Portfolio Optimization
    MAX_WEIGHT = 0.30  # Maximum 30% allocation per asset
    MIN_WEIGHT = 0.05  # Minimum 5% allocation per asset
    
    # Risk Management
    MAX_DRAWDOWN_THRESHOLD = 0.20  # 20% max drawdown alert
    STOP_LOSS = 0.10  # 10% stop loss
    TAKE_PROFIT = 0.25  # 25% take profit
    
    # Visualization
    PLOT_STYLE = 'seaborn-v0_8-darkgrid'
    FIGURE_SIZE = (14, 8)
    
    @classmethod
    def validate(cls):
        """Validate configuration"""
        if not cls.GEMINI_API_KEY:
            print("WARNING: GEMINI_API_KEY not set. AI insights will not be available.")
        return True

# Validate on import
Config.validate()
