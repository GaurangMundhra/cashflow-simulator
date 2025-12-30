# 💰 Cash Flow Simulator

A powerful financial planning tool that demonstrates the power of compounding over high income through interactive visualizations.

## 🎯 What It Does

- Simulates wealth accumulation over 5-50 years
- Shows inflation-adjusted (real) vs nominal wealth
- Calculates FIRE (Financial Independence, Retire Early) numbers
- Compares different savings and investment scenarios
- Visualizes contributions vs investment gains

## 🚀 Quick Start

```bash
# Clone repository
git clone https://github.com/yourusername/cash-flow-simulator.git
cd cash-flow-simulator

# Install dependencies
pip install -r requirements.txt

# Run the app
streamlit run app.py
```

## 📊 Features

### Core Calculations

- Compound interest with regular contributions
- Inflation adjustment
- Income growth modeling
- Investment returns simulation

### Visualizations

- Interactive wealth growth charts
- Contributions vs gains breakdown
- Scenario comparisons
- FIRE progress tracking

### Educational Content

- Why compounding beats income
- The math behind exponential growth
- Time value of money demonstrations

## 🧮 The Math

**Why Compounding Wins:**

Starting with $10,000 salary and 20% savings rate:

- **High Income, Low Savings:** $100k income, 10% saved = $833/month
- **Moderate Income, High Savings:** $50k income, 30% saved = $1,250/month

After 30 years at 7% returns:

- High income scenario: ~$1M
- High savings scenario: ~$1.5M

**The savings rate matters more than the income!**

## 🛠️ Tech Stack

- **Streamlit** - Interactive web dashboard
- **Pandas** - Data manipulation
- **Plotly** - Interactive visualizations
- **NumPy** - Numerical calculations

## 📁 Project Structure

```
cash-flow-simulator/
├── app.py                 # Main Streamlit application
├── requirements.txt       # Python dependencies
├── src/
│   ├── calculator/        # Financial calculations
│   ├── visualizer/        # Plotting functions
│   └── utils/            # Helper functions
└── tests/                # Unit tests
```

## 🎓 Educational Value

This project teaches:

1. **Compound Interest:** Money earning money
2. **Time Value:** Starting early >> earning more
3. **Consistency:** Regular investing beats timing
4. **Real Returns:** Why inflation matters
5. **FIRE Concepts:** Financial independence math

## 📈 Example Scenarios

**Scenario 1:** College Graduate

- Income: $50k → grows 3%/year
- Savings: 20%
- Returns: 7%
- Result: $1.2M in 30 years

**Scenario 2:** Late Starter

- Income: $80k → grows 2%/year
- Savings: 30%
- Returns: 7%
- Starting 10 years later
- Result: $700k in 20 years

**Lesson:** Early start beats higher income!

## 🤝 Contributing

Contributions welcome! Areas for improvement:

- Add tax calculations
- Monte Carlo simulations
- Multiple account types
- Historical market data
- Mobile responsiveness

## 📄 License

MIT License - feel free to use for learning!

## 🙏 Acknowledgments

- Historical return data from S&P 500
- FIRE concepts from r/financialindependence
- Inspiration from Mr. Money Mustache

---

**Remember:** This is an educational tool. Consult with financial advisors for personalized advice.
