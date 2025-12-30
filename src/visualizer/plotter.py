import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd

class FinancialPlotter:
    def __init__(self, style='seaborn-v0_8-darkgrid'):
        plt.style.use(style)
        sns.set_palette("husl")
    
    @staticmethod
    def plot_wealth_growth(df: pd.DataFrame, show_real: bool = True):
        """Create interactive wealth growth chart."""
        fig = go.Figure()
        
        years = df['month'] / 12
        
        fig.add_trace(go.Scatter(
            x=years,
            y=df['nominal_wealth'],
            name='Nominal Wealth',
            line=dict(color='#1f77b4', width=3)
        ))
        
        if show_real:
            fig.add_trace(go.Scatter(
                x=years,
                y=df['real_wealth'],
                name='Real Wealth (Inflation-Adjusted)',
                line=dict(color='#ff7f0e', width=3, dash='dash')
            ))
        
        fig.update_layout(
            title='Wealth Growth Over Time',
            xaxis_title='Years',
            yaxis_title='Wealth ($)',
            hovermode='x unified',
            height=500
        )
        
        return fig
    
    @staticmethod
    def plot_contributions_vs_gains(df: pd.DataFrame):
        """Create stacked area chart."""
        fig = go.Figure()
        
        years = df['month'] / 12
        
        fig.add_trace(go.Scatter(
            x=years,
            y=df['total_contributions'],
            name='Contributions',
            fill='tozeroy',
            line=dict(color='#2ca02c')
        ))
        
        fig.add_trace(go.Scatter(
            x=years,
            y=df['investment_gains'],
            name='Investment Gains',
            fill='tonexty',
            line=dict(color='#9467bd')
        ))
        
        fig.update_layout(
            title='Contributions vs Investment Gains',
            xaxis_title='Years',
            yaxis_title='Amount ($)',
            hovermode='x unified',
            height=500
        )
        
        return fig
    
    @staticmethod
    def plot_milestone_progress(current_wealth: float, fire_number: float):
        """Create gauge chart for FIRE progress."""
        fig = go.Figure(go.Indicator(
            mode="gauge+number+delta",
            value=current_wealth,
            domain={'x': [0, 1], 'y': [0, 1]},
            title={'text': "FIRE Progress"},
            delta={'reference': fire_number},
            gauge={
                'axis': {'range': [None, fire_number]},
                'bar': {'color': "darkblue"},
                'steps': [
                    {'range': [0, fire_number * 0.5], 'color': "lightgray"},
                    {'range': [fire_number * 0.5, fire_number * 0.75], 'color': "gray"}
                ],
                'threshold': {
                    'line': {'color': "red", 'width': 4},
                    'thickness': 0.75,
                    'value': fire_number
                }
            }
        ))
        
        fig.update_layout(height=400)
        return fig