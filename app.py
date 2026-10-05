
import streamlit as st
import pandas as pd
import numpy as np
from pathlib import Path
import io

from data_loader import DataLoader
from backtesting_engine import BacktestEngine, RiskAnalyzer
from visualization import Visualizer
from gemini_insights import GeminiInsights
from config import Config


# Page configuration
st.set_page_config(
    page_title="Portfolio Risk Reduction",
    page_icon="📈",
    layout="wide",
    initial_sidebar_state="expanded"
)


def main():
    """Main Streamlit application"""
    
    # Title
    st.title("📈 Portfolio Management Risk Reduction")
    st.markdown("**Backtest trading algorithms and optimize your portfolio**")
    st.divider()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Configuration")
        
        # File upload
        uploaded_file = st.file_uploader(
            "Upload Stock Data CSV",
            type=['csv', 'xlsx', 'xls'],
            help="Upload CSV or Excel file with Timestamp, Open, High, Low, Close, Volume columns"
        )
        
        # Initial capital
        initial_capital = st.number_input(
            "Initial Capital ($)",
            min_value=1000,
            max_value=10000000,
            value=int(Config.DEFAULT_INITIAL_CAPITAL),
            step=10000
        )
        
        # Strategy selection
        st.subheader("Strategies to Run")
        run_ma = st.checkbox("Moving Average", value=True)
        run_momentum = st.checkbox("Momentum", value=True)
        run_mean_reversion = st.checkbox("Mean Reversion", value=True)
        run_rsi = st.checkbox("RSI", value=True)
        run_buy_hold = st.checkbox("Buy & Hold", value=True)
        
        # AI insights
        enable_ai = st.checkbox(
            "Generate AI Insights",
            value=True,
            help="Uses Gemini API for strategy analysis"
        )
        
        # Run button
        run_backtest = st.button("🚀 Run Backtest", type="primary", use_container_width=True)
    
    # Main content area
    if uploaded_file is not None:
        
        if run_backtest:
            run_analysis(
                uploaded_file, 
                initial_capital,
                enable_ai,
                {
                    'ma': run_ma,
                    'momentum': run_momentum,
                    'mean_reversion': run_mean_reversion,
                    'rsi': run_rsi,
                    'buy_hold': run_buy_hold
                }
            )
        else:
            # Preview data
            st.info("👆 Configure settings and click 'Run Backtest' to start")
            preview_data(uploaded_file)
    
    else:
        # Welcome screen
        st.info("👈 Upload a CSV file with historical stock data to begin")
        
        st.markdown("""
        ### 📋 Required Data Format
        
        Your CSV file should contain the following columns:
        - **Timestamp**: Date/time of the data point
        - **Open**: Opening price
        - **High**: Highest price
        - **Low**: Lowest price
        - **Close**: Closing price
        - **Volume**: Trading volume
        - **Open Interest** (optional): Options open interest
        
        ### 🎯 Available Strategies
        
        - **Moving Average Crossover**: Buy when short MA crosses above long MA
        - **Momentum**: Trade based on price momentum
        - **Mean Reversion**: Trade when price deviates from mean (Bollinger Bands)
        - **RSI**: Trade based on Relative Strength Index
        - **Buy & Hold**: Baseline comparison strategy
        
        ### 🤖 AI-Powered Insights
        
        Get intelligent analysis using Google's Gemini API:
        - Strategy performance analysis
        - Risk assessment and recommendations
        - Market commentary
        - Portfolio optimization suggestions
        """)
        
        # Sample data download
        if st.button("📥 Download Sample Data"):
            sample_data = create_sample_data()
            csv = sample_data.to_csv(index=True)
            st.download_button(
                "Download sample_stock_data.csv",
                csv,
                "sample_stock_data.csv",
                "text/csv"
            )


def preview_data(uploaded_file):
    """Preview uploaded data"""
    try:
        # Save to temp file
        temp_path = Path("temp_data.csv")
        with open(temp_path, 'wb') as f:
            f.write(uploaded_file.getbuffer())
        
        # Load data
        loader = DataLoader(str(temp_path))
        loader.load_data()
        loader.validate_data()
        
        st.success("✅ Data loaded successfully!")
        
        # Show data preview
        with st.expander("📊 Data Preview", expanded=True):
            st.dataframe(loader.data.head(20), use_container_width=True)
        
        # Show statistics
        stats = loader.get_summary_statistics()
        
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Rows", f"{stats['total_rows']:,}")
        with col2:
            st.metric("Duration", f"{stats['duration_days']} days")
        with col3:
            st.metric("Mean Close", f"${stats['mean_close']:.2f}")
        with col4:
            st.metric("Total Return", f"{stats['total_return']:.2f}%")
        
    except Exception as e:
        st.error(f"Error loading data: {str(e)}")


def run_analysis(uploaded_file, initial_capital, enable_ai, strategies):
    """Run complete backtest analysis"""
    
    with st.spinner("🔄 Processing data..."):
        try:
            # Save to temp file
            temp_path = Path("temp_data.csv")
            with open(temp_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            # Load and prepare data
            loader = DataLoader(str(temp_path))
            loader.load_data()
            loader.validate_data()
            data = loader.preprocess_data()
            
            st.success("✅ Data processed successfully!")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            return
    
    # Run backtests
    with st.spinner("🔄 Running backtests..."):
        try:
            engine = BacktestEngine(data, initial_capital)
            results = engine.run_all_strategies()
            
            st.success("✅ Backtests completed!")
            
        except Exception as e:
            st.error(f"❌ Error: {str(e)}")
            return
    
    # Display results
    display_results(engine, results, data, enable_ai)


def display_results(engine, results, data, enable_ai):
    """Display backtest results"""
    
    st.header("📊 Backtest Results")
    
    # Strategy comparison
    comparison_df = engine.get_comparison_table()
    
    st.subheader("Strategy Performance Comparison")
    st.dataframe(
        comparison_df.style.background_gradient(cmap='RdYlGn', subset=['Total Return (%)', 'Sharpe Ratio']),
        use_container_width=True
    )
    
    # Metrics
    best_name, best_result = engine.get_best_strategy()
    
    st.subheader(f"🏆 Best Strategy: {best_name}")
    
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Return", f"{best_result['total_return']:.2f}%")
    with col2:
        st.metric("Sharpe Ratio", f"{best_result['sharpe_ratio']:.2f}")
    with col3:
        st.metric("Max Drawdown", f"{best_result['max_drawdown']:.2f}%")
    with col4:
        st.metric("Final Value", f"${best_result['final_value']:,.2f}")
    
    # Visualizations
    st.divider()
    st.subheader("📈 Visualizations")
    
    vis = Visualizer()
    
    # Create tabs for different charts
    tab1, tab2, tab3, tab4 = st.tabs([
        "Portfolio Value", 
        "Returns Distribution", 
        "Drawdown", 
        "Technical Indicators"
    ])
    
    with tab1:
        if 'portfolio' in best_result:
            st.line_chart(best_result['portfolio']['Total'], use_container_width=True)
    
    with tab2:
        if 'portfolio' in best_result:
            # Use Strategy_Returns if available, otherwise use Returns
            returns_col = 'Strategy_Returns' if 'Strategy_Returns' in best_result['portfolio'].columns else 'Returns'
            returns = best_result['portfolio'][returns_col].dropna()
            st.bar_chart(pd.Series(returns).value_counts().sort_index(), use_container_width=True)
    
    with tab3:
        if 'portfolio' in best_result:
            portfolio_values = best_result['portfolio']['Total']
            drawdown = (portfolio_values / portfolio_values.cummax() - 1) * 100
            st.area_chart(drawdown, use_container_width=True)
    
    with tab4:
        st.line_chart(data[['Close', 'SMA_20', 'SMA_50']], use_container_width=True)
    
    # AI Insights
    if enable_ai:
        st.divider()
        st.subheader("🤖 AI-Powered Insights")
        
        try:
            with st.spinner("🔄 Generating AI insights..."):
                gemini = GeminiInsights()
                
                # Strategy analysis
                with st.expander("📊 Strategy Analysis", expanded=True):
                    strategy_insights = gemini.generate_strategy_analysis(results)
                    st.markdown(strategy_insights)
                
                # Risk analysis
                if 'portfolio' in best_result:
                    with st.expander("⚠️ Risk Analysis", expanded=False):
                        # Use Strategy_Returns if available, otherwise use Returns
                        returns_col = 'Strategy_Returns' if 'Strategy_Returns' in best_result['portfolio'].columns else 'Returns'
                        risk_analyzer = RiskAnalyzer(best_result['portfolio'][returns_col])
                        risk_metrics = risk_analyzer.risk_metrics_summary()
                        risk_insights = gemini.generate_risk_analysis(risk_metrics)
                        st.markdown(risk_insights)
                
                # Market commentary
                with st.expander("📰 Market Commentary", expanded=False):
                    market_commentary = gemini.generate_market_commentary(data)
                    st.markdown(market_commentary)
                
        except Exception as e:
            st.warning(f"⚠️ AI insights unavailable: {str(e)}")
    
    # Download results
    st.divider()
    st.subheader("💾 Download Results")
    
    col1, col2 = st.columns(2)
    
    with col1:
        csv = comparison_df.to_csv(index=False)
        st.download_button(
            "📥 Download Comparison (CSV)",
            csv,
            "strategy_comparison.csv",
            "text/csv",
            use_container_width=True
        )
    
    with col2:
        report = engine.generate_summary_report()
        st.download_button(
            "📥 Download Full Report (TXT)",
            report,
            "backtest_report.txt",
            "text/plain",
            use_container_width=True
        )


def create_sample_data():
    """Create sample stock data"""
    np.random.seed(42)
    dates = pd.date_range('2022-01-01', '2024-01-01', freq='D')
    
    # Generate realistic stock prices
    returns = np.random.normal(0.0005, 0.02, len(dates))
    price = 100 * (1 + returns).cumprod()
    
    data = pd.DataFrame({
        'Timestamp': dates,
        'Open': price * np.random.uniform(0.99, 1.01, len(dates)),
        'High': price * np.random.uniform(1.00, 1.03, len(dates)),
        'Low': price * np.random.uniform(0.97, 1.00, len(dates)),
        'Close': price,
        'Volume': np.random.randint(1000000, 10000000, len(dates)),
        'Open Interest': np.random.randint(10000, 100000, len(dates))
    })
    
    data.set_index('Timestamp', inplace=True)
    return data


if __name__ == "__main__":
    main()
