"""
Data Loader Module
Handles loading and preprocessing of historical stock data
"""
import pandas as pd
import numpy as np
from typing import Optional, Dict, List
from datetime import datetime
import warnings

warnings.filterwarnings('ignore')


class DataLoader:
    """Load and validate stock market data from CSV/Excel files"""
    
    REQUIRED_COLUMNS = ['Timestamp', 'Open', 'High', 'Low', 'Close', 'Volume']
    OPTIONAL_COLUMNS = ['Open Interest']
    
    def __init__(self, file_path: str):
        """
        Initialize DataLoader
        
        Args:
            file_path: Path to CSV or Excel file
        """
        self.file_path = file_path
        self.data = None
        self.symbol = None
        
    def load_data(self) -> pd.DataFrame:
        """
        Load data from file
        
        Returns:
            DataFrame with loaded data
        """
        try:
            if self.file_path.endswith('.csv'):
                self.data = pd.read_csv(self.file_path)
            elif self.file_path.endswith(('.xlsx', '.xls')):
                self.data = pd.read_excel(self.file_path)
            else:
                raise ValueError("Unsupported file format. Use CSV or Excel.")
            
            print(f"✓ Loaded {len(self.data)} rows from {self.file_path}")
            return self.data
            
        except Exception as e:
            raise Exception(f"Error loading data: {str(e)}")
    
    def validate_data(self) -> bool:
        """
        Validate that required columns exist
        
        Returns:
            True if valid
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        # Check required columns
        missing_cols = [col for col in self.REQUIRED_COLUMNS 
                       if col not in self.data.columns]
        
        if missing_cols:
            raise ValueError(f"Missing required columns: {missing_cols}")
        
        # Check for empty data
        if len(self.data) == 0:
            raise ValueError("Dataset is empty")
        
        print("✓ Data validation passed")
        return True
    
    def preprocess_data(self) -> pd.DataFrame:
        """
        Preprocess and clean the data
        
        Returns:
            Cleaned DataFrame
        """
        if self.data is None:
            raise ValueError("No data loaded. Call load_data() first.")
        
        df = self.data.copy()
        
        # Convert Timestamp to datetime
        df['Timestamp'] = pd.to_datetime(df['Timestamp'])
        df = df.sort_values('Timestamp')
        df.set_index('Timestamp', inplace=True)
        
        # Remove duplicates
        df = df[~df.index.duplicated(keep='first')]
        
        # Handle missing values
        df = df.fillna(method='ffill').fillna(method='bfill')
        
        # Validate OHLC relationships
        df = df[(df['High'] >= df['Low']) & 
                (df['High'] >= df['Open']) & 
                (df['High'] >= df['Close']) &
                (df['Low'] <= df['Open']) &
                (df['Low'] <= df['Close'])]
        
        # Calculate additional features
        df['Returns'] = df['Close'].pct_change()
        df['Log_Returns'] = np.log(df['Close'] / df['Close'].shift(1))
        df['Volatility'] = df['Returns'].rolling(window=20).std()
        df['Range'] = df['High'] - df['Low']
        df['Price_Change'] = df['Close'] - df['Open']
        
        # Technical indicators
        df['SMA_20'] = df['Close'].rolling(window=20).mean()
        df['SMA_50'] = df['Close'].rolling(window=50).mean()
        df['SMA_200'] = df['Close'].rolling(window=200).mean()
        
        # Exponential Moving Average
        df['EMA_12'] = df['Close'].ewm(span=12, adjust=False).mean()
        df['EMA_26'] = df['Close'].ewm(span=26, adjust=False).mean()
        df['MACD'] = df['EMA_12'] - df['EMA_26']
        df['MACD_Signal'] = df['MACD'].ewm(span=9, adjust=False).mean()
        
        # Bollinger Bands
        df['BB_Middle'] = df['Close'].rolling(window=20).mean()
        bb_std = df['Close'].rolling(window=20).std()
        df['BB_Upper'] = df['BB_Middle'] + (2 * bb_std)
        df['BB_Lower'] = df['BB_Middle'] - (2 * bb_std)
        
        # RSI (Relative Strength Index)
        delta = df['Close'].diff()
        gain = (delta.where(delta > 0, 0)).rolling(window=14).mean()
        loss = (-delta.where(delta < 0, 0)).rolling(window=14).mean()
        rs = gain / loss
        df['RSI'] = 100 - (100 / (1 + rs))
        
        # Drop NaN values created by technical indicators
        df = df.dropna()
        
        self.data = df
        print(f"✓ Data preprocessed: {len(df)} valid rows")
        print(f"  Date range: {df.index[0]} to {df.index[-1]}")
        
        return df
    
    def get_summary_statistics(self) -> Dict:
        """
        Get summary statistics of the data
        
        Returns:
            Dictionary with statistics
        """
        if self.data is None or len(self.data) == 0:
            raise ValueError("No data available")
        
        # Calculate duration safely
        try:
            duration = (self.data.index[-1] - self.data.index[0]).days
        except AttributeError:
            # If index is not datetime, just use the number of rows
            duration = len(self.data)
        
        stats = {
            'total_rows': len(self.data),
            'start_date': self.data.index[0],
            'end_date': self.data.index[-1],
            'duration_days': duration,
            'mean_close': self.data['Close'].mean(),
            'std_close': self.data['Close'].std(),
            'min_close': self.data['Close'].min(),
            'max_close': self.data['Close'].max(),
            'mean_volume': self.data['Volume'].mean(),
            'mean_returns': self.data['Returns'].mean() * 100,
            'std_returns': self.data['Returns'].std() * 100,
            'total_return': ((self.data['Close'].iloc[-1] / 
                            self.data['Close'].iloc[0]) - 1) * 100
        }
        
        return stats
    
    def split_train_test(self, train_ratio: float = 0.8) -> tuple:
        """
        Split data into training and testing sets
        
        Args:
            train_ratio: Proportion of data for training
            
        Returns:
            Tuple of (train_df, test_df)
        """
        if self.data is None:
            raise ValueError("No data available")
        
        split_idx = int(len(self.data) * train_ratio)
        train_df = self.data.iloc[:split_idx]
        test_df = self.data.iloc[split_idx:]
        
        print(f"✓ Data split: {len(train_df)} train, {len(test_df)} test")
        
        return train_df, test_df
    
    def export_processed_data(self, output_path: str):
        """
        Export processed data to CSV
        
        Args:
            output_path: Path for output file
        """
        if self.data is None:
            raise ValueError("No data to export")
        
        self.data.to_csv(output_path)
        print(f"✓ Data exported to {output_path}")


def load_multiple_assets(file_paths: Dict[str, str]) -> Dict[str, pd.DataFrame]:
    """
    Load multiple asset data files
    
    Args:
        file_paths: Dictionary mapping asset names to file paths
        
    Returns:
        Dictionary mapping asset names to DataFrames
    """
    assets_data = {}
    
    for asset_name, file_path in file_paths.items():
        try:
            loader = DataLoader(file_path)
            loader.load_data()
            loader.validate_data()
            df = loader.preprocess_data()
            assets_data[asset_name] = df
            print(f"✓ Loaded {asset_name}")
        except Exception as e:
            print(f"✗ Error loading {asset_name}: {str(e)}")
    
    return assets_data


if __name__ == "__main__":
    # Test the data loader
    print("DataLoader Module - Ready for use")
