import pytest
import sys
sys.path.append('..')
from src.calculator.cash_flow import CashFlowCalculator

def test_basic_calculation():
    calc = CashFlowCalculator(income=50000, expenses=30000, savings_rate=0.2)
    df = calc.calculate_wealth_projection(10, 0.07, 0.03)
    
    assert len(df) == 120  # 10 years * 12 months
    assert df['nominal_wealth'].iloc[-1] > 0
    assert df['real_wealth'].iloc[-1] > 0

def test_fire_number():
    calc = CashFlowCalculator(income=50000, expenses=30000, savings_rate=0.2)
    fire_num = calc.calculate_fire_number(30000)
    
    assert fire_num == 750000  # 30k / 0.04

# Run with: pytest tests/