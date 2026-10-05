"""
Gemini AI Integration Module
Generate insights and explanations using Google's Gemini API
"""
import google.generativeai as genai
from typing import Dict, List, Optional
import pandas as pd
import json
from config import Config


class GeminiInsights:
    """Generate AI-powered insights using Gemini API"""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Gemini Insights
        
        Args:
            api_key: Gemini API key (uses config if not provided)
        """
        self.api_key = api_key or Config.GEMINI_API_KEY
        
        if not self.api_key:
            raise ValueError(
                "Gemini API key not found. Set GEMINI_API_KEY in .env file"
            )
        
        genai.configure(api_key=self.api_key)
        # Using Gemini 2.0 Flash (latest available model)
        self.model = genai.GenerativeModel('gemini-2.5-flash')
        
    def generate_strategy_analysis(self, backtest_results: Dict) -> str:
        """
        Generate analysis of backtesting results
        
        Args:
            backtest_results: Dictionary with backtest results
            
        Returns:
            AI-generated analysis
        """
        prompt = self._create_strategy_analysis_prompt(backtest_results)
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def _create_strategy_analysis_prompt(self, results: Dict) -> str:
        """Create prompt for strategy analysis"""
        
        # Prepare results summary
        summary = []
        for strategy_name, metrics in results.items():
            summary.append(
                f"- {strategy_name}: "
                f"Return: {metrics['total_return']:.2f}%, "
                f"Sharpe: {metrics['sharpe_ratio']:.2f}, "
                f"Max Drawdown: {metrics['max_drawdown']:.2f}%"
            )
        
        prompt = f"""
You are a financial analyst expert specializing in algorithmic trading and portfolio management.

Analyze the following backtesting results from multiple trading strategies:

{chr(10).join(summary)}

Please provide:

1. **Performance Analysis**: Which strategies performed best and why?
2. **Risk Assessment**: Analyze the risk-return profile of each strategy
3. **Comparative Insights**: Compare strategies and their suitability for different market conditions
4. **Recommendations**: Which strategy or combination would you recommend and why?
5. **Market Context**: What market conditions favor each strategy?
6. **Risk Management**: Specific risk management recommendations

Be specific, data-driven, and provide actionable insights. Use clear sections and bullet points.
"""
        return prompt
    
    def generate_portfolio_insights(self, portfolio_data: Dict) -> str:
        """
        Generate insights for portfolio optimization
        
        Args:
            portfolio_data: Portfolio allocation and metrics
            
        Returns:
            AI-generated insights
        """
        prompt = f"""
As a portfolio management expert, analyze this portfolio allocation:

Portfolio Weights:
{json.dumps(portfolio_data.get('weights', {}), indent=2)}

Metrics:
- Annual Return: {portfolio_data.get('annual_return', 0):.2f}%
- Annual Volatility: {portfolio_data.get('annual_volatility', 0):.2f}%
- Sharpe Ratio: {portfolio_data.get('sharpe_ratio', 0):.2f}
- Max Drawdown: {portfolio_data.get('max_drawdown', 0):.2f}%

Provide:
1. **Portfolio Assessment**: Overall portfolio health and balance
2. **Diversification Analysis**: Is the portfolio well-diversified?
3. **Risk-Adjusted Performance**: Evaluate risk-adjusted returns
4. **Optimization Suggestions**: How to improve the portfolio
5. **Rebalancing Recommendations**: When and how to rebalance
6. **Market Outlook Considerations**: Adjustments for different market scenarios

Be specific and actionable.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def generate_risk_analysis(self, risk_metrics: Dict) -> str:
        """
        Generate risk analysis and recommendations
        
        Args:
            risk_metrics: Dictionary with risk metrics
            
        Returns:
            AI-generated risk analysis
        """
        prompt = f"""
As a risk management specialist, analyze these portfolio risk metrics:

{json.dumps(risk_metrics, indent=2)}

Provide comprehensive analysis including:

1. **Risk Profile**: Overall assessment of portfolio risk
2. **Key Risk Indicators**: Interpretation of VaR, CVaR, and drawdown metrics
3. **Volatility Analysis**: Is volatility acceptable for typical investors?
4. **Tail Risk**: Assessment of extreme loss scenarios
5. **Risk Mitigation**: Specific strategies to reduce risk
6. **Position Sizing**: Recommendations for position limits
7. **Stop Loss Levels**: Suggested stop-loss and take-profit levels
8. **Hedging Strategies**: Options or other hedging recommendations

Focus on practical, implementable risk management strategies.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating insights: {str(e)}"
    
    def generate_market_commentary(self, data: pd.DataFrame) -> str:
        """
        Generate market commentary based on price data
        
        Args:
            data: DataFrame with OHLCV data
            
        Returns:
            Market commentary
        """
        # Calculate key statistics
        recent_return = ((data['Close'].iloc[-1] / data['Close'].iloc[-30]) - 1) * 100
        volatility = data['Returns'].tail(30).std() * np.sqrt(252) * 100
        current_price = data['Close'].iloc[-1]
        
        prompt = f"""
As a market analyst, provide commentary on this asset:

Recent Performance (30 days): {recent_return:.2f}%
Current Price: ${current_price:.2f}
Recent Volatility (annualized): {volatility:.2f}%
Price Range: ${data['Low'].tail(30).min():.2f} - ${data['High'].tail(30).max():.2f}

Technical Indicators:
- RSI: {data['RSI'].iloc[-1]:.2f}
- Price vs SMA(50): {((current_price / data['SMA_50'].iloc[-1]) - 1) * 100:.2f}%
- MACD Signal: {'Bullish' if data['MACD'].iloc[-1] > data['MACD_Signal'].iloc[-1] else 'Bearish'}

Provide:
1. **Technical Analysis**: Current technical picture
2. **Trend Assessment**: Short-term and medium-term trends
3. **Support/Resistance**: Key price levels
4. **Trading Opportunities**: Potential entry/exit points
5. **Market Sentiment**: Likely market sentiment
6. **Outlook**: Short-term price forecast

Keep it concise and actionable.
"""
        
        try:
            import numpy as np
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating commentary: {str(e)}"
    
    def generate_comparative_report(self, comparison_df: pd.DataFrame) -> str:
        """
        Generate comparative analysis of strategies
        
        Args:
            comparison_df: DataFrame with strategy comparison
            
        Returns:
            Comparative analysis
        """
        prompt = f"""
Analyze these trading strategy comparison results:

{comparison_df.to_string()}

Provide detailed analysis:

1. **Top Performers**: Identify and explain top 3 strategies
2. **Risk-Adjusted Winners**: Best strategies by Sharpe ratio
3. **Consistency Analysis**: Which strategies are most consistent?
4. **Market Condition Suitability**: Which strategies for trending vs ranging markets?
5. **Strategy Combinations**: How to combine strategies for better results?
6. **Implementation Priority**: Which strategy to implement first and why?
7. **Expected Returns**: Realistic return expectations going forward
8. **Warning Signs**: Red flags or concerns with any strategy

Provide actionable, specific recommendations for a trader/investor.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating report: {str(e)}"
    
    def generate_custom_analysis(self, custom_prompt: str, context_data: str = "") -> str:
        """
        Generate custom analysis with user-defined prompt
        
        Args:
            custom_prompt: User's custom question/prompt
            context_data: Additional context data
            
        Returns:
            AI-generated response
        """
        full_prompt = f"""
You are an expert financial analyst and trading strategist.

Context Data:
{context_data}

User Question:
{custom_prompt}

Provide a comprehensive, data-driven answer with specific recommendations.
"""
        
        try:
            response = self.model.generate_content(full_prompt)
            return response.text
        except Exception as e:
            return f"Error generating analysis: {str(e)}"
    
    def generate_executive_summary(self, all_results: Dict) -> str:
        """
        Generate executive summary of entire analysis
        
        Args:
            all_results: Dictionary with all analysis results
            
        Returns:
            Executive summary
        """
        prompt = f"""
Create an executive summary for a Portfolio Risk Reduction backtesting report.

Data Summary:
{json.dumps(all_results, indent=2, default=str)}

Provide a concise executive summary (500-700 words) including:

1. **Overview**: What was tested and key findings
2. **Best Strategy**: Top performing approach with key metrics
3. **Risk Assessment**: Overall risk level and management
4. **Key Insights**: 3-5 most important discoveries
5. **Recommendations**: Clear action items for implementation
6. **Next Steps**: What to do with these results

Write in professional, business-appropriate language suitable for stakeholders.
Focus on actionable insights and clear decision-making guidance.
"""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            return f"Error generating summary: {str(e)}"


class PromptLibrary:
    """Pre-built prompts for common analysis tasks"""
    
    @staticmethod
    def get_prompt_templates() -> Dict[str, str]:
        """
        Get library of prompt templates
        
        Returns:
            Dictionary of prompt templates
        """
        return {
            'strategy_optimization': """
                Analyze backtesting results and suggest optimizations for:
                - Entry/exit timing
                - Position sizing
                - Risk management rules
                - Strategy parameters
            """,
            
            'portfolio_rebalancing': """
                Based on current portfolio performance, recommend:
                - Rebalancing frequency
                - Target allocations
                - Tax-efficient rebalancing strategies
                - Threshold-based vs time-based rebalancing
            """,
            
            'market_regime_analysis': """
                Identify market regimes (trending, ranging, volatile) and suggest:
                - Best strategies for each regime
                - Regime detection indicators
                - Strategy switching rules
            """,
            
            'drawdown_recovery': """
                For portfolios in drawdown, recommend:
                - Recovery strategies
                - Risk reduction measures
                - Capital preservation techniques
                - Timeline for recovery
            """,
            
            'scenario_analysis': """
                Analyze portfolio behavior under scenarios:
                - Market crash (20%+ decline)
                - High inflation environment
                - Rising interest rates
                - Economic recession
            """
        }
    
    @staticmethod
    def build_custom_prompt(template_name: str, data: Dict) -> str:
        """
        Build custom prompt from template
        
        Args:
            template_name: Name of template
            data: Data to include in prompt
            
        Returns:
            Formatted prompt
        """
        templates = PromptLibrary.get_prompt_templates()
        
        if template_name not in templates:
            raise ValueError(f"Template '{template_name}' not found")
        
        template = templates[template_name]
        data_str = json.dumps(data, indent=2, default=str)
        
        return f"{template}\n\nData:\n{data_str}"


if __name__ == "__main__":
    print("Gemini Insights Module - Ready for use")
    print("\nAvailable prompt templates:")
    for name in PromptLibrary.get_prompt_templates().keys():
        print(f"  - {name}")
