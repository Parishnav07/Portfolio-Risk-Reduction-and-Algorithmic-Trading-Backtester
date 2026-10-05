"""
Generate sample stock data for testing
"""
import pandas as pd
import numpy as np
from datetime import datetime, timedelta


def generate_sample_stock_data(
    start_date: str = '2022-01-01',
    end_date: str = '2024-01-01',
    initial_price: float = 100.0,
    volatility: float = 0.02,
    trend: float = 0.0005,
    output_file: str = 'sample_data/stock_data.csv'
):
    """
    Generate realistic sample stock data
    
    Args:
        start_date: Start date for data
        end_date: End date for data
        initial_price: Starting price
        volatility: Daily volatility
        trend: Daily trend (drift)
        output_file: Output file path
    """
    np.random.seed(42)
    
    # Generate date range
    dates = pd.date_range(start_date, end_date, freq='D')
    
    # Generate returns with trend and volatility
    returns = np.random.normal(trend, volatility, len(dates))
    
    # Calculate prices
    price = initial_price * (1 + returns).cumprod()
    
    # Add some realistic noise and patterns
    noise = np.random.normal(0, 0.005, len(dates))
    price = price * (1 + noise)
    
    # Generate OHLC data
    data = pd.DataFrame({
        'Timestamp': dates,
        'Open': price * np.random.uniform(0.99, 1.01, len(dates)),
        'Close': price,
    })
    
    # Calculate High and Low
    data['High'] = data[['Open', 'Close']].max(axis=1) * np.random.uniform(1.00, 1.02, len(dates))
    data['Low'] = data[['Open', 'Close']].min(axis=1) * np.random.uniform(0.98, 1.00, len(dates))
    
    # Generate volume (correlated with price changes)
    base_volume = 5000000
    volatility_factor = np.abs(data['Close'].pct_change()).fillna(0) * 10
    data['Volume'] = (base_volume * (1 + volatility_factor) * 
                     np.random.uniform(0.5, 1.5, len(dates))).astype(int)
    
    # Generate Open Interest (for options)
    data['Open Interest'] = np.random.randint(50000, 200000, len(dates))
    
    # Reorder columns
    data = data[['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume', 'Open Interest']]
    
    # Save to file
    import os
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    data.to_csv(output_file, index=False)
    
    print(f"✓ Sample data generated: {output_file}")
    print(f"  Rows: {len(data)}")
    print(f"  Date range: {data['Timestamp'].min()} to {data['Timestamp'].max()}")
    print(f"  Price range: ${data['Low'].min():.2f} - ${data['High'].max():.2f}")
    
    return data


def generate_multiple_assets():
    """Generate sample data for multiple assets"""
    
    assets = {
        'AAPL': {'initial_price': 150, 'volatility': 0.025, 'trend': 0.0008},
        'GOOGL': {'initial_price': 2800, 'volatility': 0.022, 'trend': 0.0006},
        'MSFT': {'initial_price': 300, 'volatility': 0.020, 'trend': 0.0007},
        'AMZN': {'initial_price': 3300, 'volatility': 0.030, 'trend': 0.0005},
        'TSLA': {'initial_price': 800, 'volatility': 0.040, 'trend': 0.0010},
    }
    
    for symbol, params in assets.items():
        generate_sample_stock_data(
            initial_price=params['initial_price'],
            volatility=params['volatility'],
            trend=params['trend'],
            output_file=f'sample_data/{symbol}_data.csv'
        )
    
    print("\n✓ Generated data for all assets")


if __name__ == "__main__":
    print("Generating sample stock data...")
    print("="*60)
    
    # Generate single asset
    generate_sample_stock_data()
    
    print("\n" + "="*60)
    print("Generating multiple assets...")
    print("="*60)
    
    # Generate multiple assets
    generate_multiple_assets()
    
    print("\n✓ All sample data generated successfully!")
