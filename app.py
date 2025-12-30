import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Page config
st.set_page_config(
    page_title="Cash Flow Simulator",
    page_icon="💰",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        color: #1f77b4;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Calculator Functions
def calculate_wealth_projection(income, expenses, savings_rate, years, 
                                investment_return, inflation_rate, income_growth):
    months = years * 12
    wealth = 0
    total_contrib = 0
    current_income = income
    
    monthly_return = investment_return / 12
    monthly_inflation = inflation_rate / 12
    monthly_income_growth = income_growth / 12
    
    data = {
        'month': [],
        'year': [],
        'nominal_wealth': [],
        'real_wealth': [],
        'total_contributions': [],
        'investment_gains': [],
        'income': [],
        'monthly_savings': []
    }
    
    for month in range(1, months + 1):
        if month % 12 == 0:
            current_income *= (1 + income_growth)
        
        monthly_savings = current_income * savings_rate / 12
        wealth = wealth * (1 + monthly_return) + monthly_savings
        total_contrib += monthly_savings
        
        real_wealth = wealth / ((1 + monthly_inflation) ** month)
        investment_gains = wealth - total_contrib
        
        data['month'].append(month)
        data['year'].append(month / 12)
        data['nominal_wealth'].append(wealth)
        data['real_wealth'].append(real_wealth)
        data['total_contributions'].append(total_contrib)
        data['investment_gains'].append(investment_gains)
        data['income'].append(current_income)
        data['monthly_savings'].append(monthly_savings)
    
    return pd.DataFrame(data)

def calculate_fire_number(annual_expenses, withdrawal_rate=0.04):
    return annual_expenses / withdrawal_rate

# Header
st.markdown('<h1 class="main-header">💰 Cash Flow Simulator</h1>', unsafe_allow_html=True)
st.markdown("### Visualize Your Financial Future Through the Power of Compounding")

# Sidebar - Input Parameters
st.sidebar.header("📊 Input Parameters")

with st.sidebar.expander("💵 Income & Expenses", expanded=True):
    annual_income = st.number_input(
        "Annual Income ($)",
        min_value=0,
        value=60000,
        step=5000,
        help="Your gross annual income"
    )
    
    annual_expenses = st.number_input(
        "Annual Expenses ($)",
        min_value=0,
        value=36000,
        step=1000,
        help="Your total annual expenses"
    )
    
    savings_rate = st.slider(
        "Savings Rate (%)",
        min_value=0,
        max_value=100,
        value=30,
        help="Percentage of income you save"
    ) / 100

with st.sidebar.expander("📈 Investment Parameters", expanded=True):
    investment_return = st.slider(
        "Expected Annual Return (%)",
        min_value=0.0,
        max_value=20.0,
        value=7.0,
        step=0.5,
        help="Historical S&P 500: ~10%"
    ) / 100
    
    inflation_rate = st.slider(
        "Annual Inflation Rate (%)",
        min_value=0.0,
        max_value=10.0,
        value=3.0,
        step=0.5
    ) / 100
    
    income_growth = st.slider(
        "Annual Income Growth (%)",
        min_value=0.0,
        max_value=10.0,
        value=3.0,
        step=0.5,
        help="Expected annual salary increases"
    ) / 100

with st.sidebar.expander("⏱️ Time Horizon"):
    years = st.slider(
        "Years to Simulate",
        min_value=5,
        max_value=50,
        value=30,
        help="Investment time horizon"
    )

# Calculate
df = calculate_wealth_projection(
    annual_income, annual_expenses, savings_rate, years,
    investment_return, inflation_rate, income_growth
)

fire_number = calculate_fire_number(annual_expenses)
final_wealth = df['nominal_wealth'].iloc[-1]
final_real_wealth = df['real_wealth'].iloc[-1]
total_contributions = df['total_contributions'].iloc[-1]
total_gains = df['investment_gains'].iloc[-1]

# Key Metrics
st.header("🎯 Key Metrics")
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.metric(
        "Final Wealth (Nominal)",
        f"${final_wealth:,.0f}",
        f"+${final_wealth - total_contributions:,.0f}"
    )

with col2:
    st.metric(
        "Final Wealth (Real)",
        f"${final_real_wealth:,.0f}",
        "Inflation-Adjusted"
    )

with col3:
    st.metric(
        "Total Contributions",
        f"${total_contributions:,.0f}",
        f"{savings_rate*100:.0f}% savings rate"
    )

with col4:
    st.metric(
        "Investment Gains",
        f"${total_gains:,.0f}",
        f"{(total_gains/total_contributions)*100:.1f}% return"
    )

# FIRE Analysis
st.header("🔥 FIRE Analysis")
col1, col2, col3 = st.columns(3)

with col1:
    st.metric("FIRE Number", f"${fire_number:,.0f}")

with col2:
    fire_progress = min((final_real_wealth / fire_number) * 100, 100)
    st.metric("FIRE Progress", f"{fire_progress:.1f}%")

with col3:
    months_to_fire = df[df['real_wealth'] >= fire_number]['month'].min() if any(df['real_wealth'] >= fire_number) else None
    if months_to_fire:
        st.metric("Years to FIRE", f"{months_to_fire/12:.1f} years")
    else:
        st.metric("Years to FIRE", "Not reached")

# Main Visualization
st.header("📈 Wealth Growth Projection")

tab1, tab2, tab3, tab4 = st.tabs(["Wealth Growth", "Contributions vs Gains", "Income & Savings", "Comparison"])

with tab1:
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['nominal_wealth'],
        name='Nominal Wealth',
        line=dict(color='#1f77b4', width=3),
        fill='tozeroy'
    ))
    
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['real_wealth'],
        name='Real Wealth (Inflation-Adjusted)',
        line=dict(color='#ff7f0e', width=3, dash='dash')
    ))
    
    if any(df['real_wealth'] >= fire_number):
        fig.add_hline(
            y=fire_number,
            line_dash="dot",
            line_color="green",
            annotation_text="FIRE Number",
            annotation_position="right"
        )
    
    fig.update_layout(
        title='Wealth Growth Over Time',
        xaxis_title='Years',
        yaxis_title='Wealth ($)',
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['total_contributions'],
        name='Your Contributions',
        fill='tozeroy',
        line=dict(color='#2ca02c', width=2)
    ))
    
    fig.add_trace(go.Scatter(
        x=df['year'],
        y=df['investment_gains'],
        name='Investment Gains',
        fill='tonexty',
        line=dict(color='#9467bd', width=2)
    ))
    
    fig.update_layout(
        title='Contributions vs Investment Gains',
        xaxis_title='Years',
        yaxis_title='Amount ($)',
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Breakdown
    col1, col2 = st.columns(2)
    with col1:
        st.info(f"""
        **Your Contributions:** ${total_contributions:,.0f}  
        ({(total_contributions/final_wealth)*100:.1f}% of final wealth)
        """)
    with col2:
        st.success(f"""
        **Investment Gains:** ${total_gains:,.0f}  
        ({(total_gains/final_wealth)*100:.1f}% of final wealth)
        """)

with tab3:
    fig = make_subplots(
        rows=2, cols=1,
        subplot_titles=('Annual Income Growth', 'Monthly Savings Growth'),
        vertical_spacing=0.15
    )
    
    annual_data = df[df['month'] % 12 == 0]
    
    fig.add_trace(
        go.Scatter(
            x=annual_data['year'],
            y=annual_data['income'],
            name='Annual Income',
            line=dict(color='#1f77b4', width=3)
        ),
        row=1, col=1
    )
    
    fig.add_trace(
        go.Scatter(
            x=df['year'],
            y=df['monthly_savings'],
            name='Monthly Savings',
            line=dict(color='#2ca02c', width=3),
            fill='tozeroy'
        ),
        row=2, col=1
    )
    
    fig.update_xaxes(title_text="Years", row=2, col=1)
    fig.update_yaxes(title_text="Amount ($)", row=1, col=1)
    fig.update_yaxes(title_text="Amount ($)", row=2, col=1)
    
    fig.update_layout(height=700, hovermode='x unified')
    
    st.plotly_chart(fig, use_container_width=True)

with tab4:
    st.subheader("Compare Different Scenarios")
    
    scenarios = []
    scenario_names = []
    
    # Current scenario
    scenarios.append(df['nominal_wealth'].values)
    scenario_names.append(f"Current ({savings_rate*100:.0f}% savings)")
    
    # Higher savings
    if savings_rate < 0.5:
        higher_savings_df = calculate_wealth_projection(
            annual_income, annual_expenses, min(savings_rate + 0.1, 0.5),
            years, investment_return, inflation_rate, income_growth
        )
        scenarios.append(higher_savings_df['nominal_wealth'].values)
        scenario_names.append(f"+10% Savings ({min(savings_rate + 0.1, 0.5)*100:.0f}%)")
    
    # Better returns
    better_return_df = calculate_wealth_projection(
        annual_income, annual_expenses, savings_rate,
        years, investment_return + 0.02, inflation_rate, income_growth
    )
    scenarios.append(better_return_df['nominal_wealth'].values)
    scenario_names.append(f"+2% Returns ({(investment_return + 0.02)*100:.1f}%)")
    
    # Lower savings
    if savings_rate > 0.1:
        lower_savings_df = calculate_wealth_projection(
            annual_income, annual_expenses, max(savings_rate - 0.1, 0.05),
            years, investment_return, inflation_rate, income_growth
        )
        scenarios.append(lower_savings_df['nominal_wealth'].values)
        scenario_names.append(f"-10% Savings ({max(savings_rate - 0.1, 0.05)*100:.0f}%)")
    
    fig = go.Figure()
    
    colors = ['#1f77b4', '#2ca02c', '#ff7f0e', '#d62728']
    for i, (scenario, name) in enumerate(zip(scenarios, scenario_names)):
        fig.add_trace(go.Scatter(
            x=df['year'],
            y=scenario,
            name=name,
            line=dict(color=colors[i], width=3 if i == 0 else 2, dash='solid' if i == 0 else 'dash')
        ))
    
    fig.update_layout(
        title='Scenario Comparison',
        xaxis_title='Years',
        yaxis_title='Wealth ($)',
        hovermode='x unified',
        height=500
    )
    
    st.plotly_chart(fig, use_container_width=True)

# Educational Content
st.header("📚 Why Compounding Beats High Income")

col1, col2 = st.columns(2)

with col1:
    st.subheader("The Power of Compounding")
    st.write("""
    **Compounding is when your returns generate their own returns.** 
    
    Over time, this exponential growth can dramatically outpace linear savings:
    
    - **Year 1-10:** Your contributions dominate
    - **Year 10-20:** Returns start catching up
    - **Year 20+:** Returns often exceed contributions
    
    This is why starting early matters more than earning more.
    """)
    
    # Calculate the crossover point
    crossover = df[df['investment_gains'] > df['total_contributions']]['year'].min()
    if pd.notna(crossover):
        st.success(f"✨ In your scenario, investment gains surpass contributions at year {crossover:.1f}")

with col2:
    st.subheader("Key Insights from Your Simulation")
    
    gain_ratio = total_gains / total_contributions if total_contributions > 0 else 0
    
    st.write(f"""
    **Your Numbers:**
    
    - You contribute: **${total_contributions:,.0f}**
    - Your money earns: **${total_gains:,.0f}**
    - **That's {gain_ratio:.2f}x your contributions!**
    
    **What This Means:**
    
    For every dollar you save, compounding adds **${gain_ratio:.2f}** more.
    
    **The Formula:**
    
    ```
    Final Wealth = Contributions × (1 + Time × Return Rate)^Time
    ```
    
    Time is your most valuable asset in investing.
    """)

# Download Data
st.header("💾 Export Your Data")
col1, col2 = st.columns(2)

with col1:
    csv = df.to_csv(index=False)
    st.download_button(
        label="📥 Download CSV",
        data=csv,
        file_name="cash_flow_projection.csv",
        mime="text/csv"
    )

with col2:
    summary = f"""
Cash Flow Simulation Summary
================================
Annual Income: ${annual_income:,.0f}
Annual Expenses: ${annual_expenses:,.0f}
Savings Rate: {savings_rate*100:.1f}%
Investment Return: {investment_return*100:.1f}%
Time Horizon: {years} years

Results:
--------
Final Wealth (Nominal): ${final_wealth:,.0f}
Final Wealth (Real): ${final_real_wealth:,.0f}
Total Contributions: ${total_contributions:,.0f}
Investment Gains: ${total_gains:,.0f}
Gain Ratio: {gain_ratio:.2f}x

FIRE Analysis:
--------------
FIRE Number: ${fire_number:,.0f}
FIRE Progress: {fire_progress:.1f}%
    """
    
    st.download_button(
        label="📥 Download Summary",
        data=summary,
        file_name="cash_flow_summary.txt",
        mime="text/plain"
    )

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666;'>
    <p>💡 This simulator uses historical market data and inflation rates. Past performance doesn't guarantee future results.</p>
    <p>Built with Streamlit • Made for financial education</p>
</div>
""", unsafe_allow_html=True)