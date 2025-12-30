import numpy as np
import pandas as pd
from typing import Dict, List, Tuple

class CashFlowCalculator:
    def __init__(self, income: float, expenses: float, savings_rate: float):
        self.income = income
        self.expenses = expenses
        self.savings_rate = savings_rate
        self.monthly_savings = income * savings_rate / 12
    
    def calculate_wealth_projection(
        self, 
        years: int, 
        investment_return: float,
        inflation_rate: float,
        income_growth: float = 0.03
    ) -> pd.DataFrame:
        """
        Calculate wealth over time with various factors.
        """
        months = years * 12
        data = {
            'month': range(1, months + 1),
            'nominal_wealth': [],
            'real_wealth': [],
            'total_contributions': [],
            'investment_gains': [],
            'income': [],
            'expenses': []
        }
        
        wealth = 0
        total_contrib = 0
        current_income = self.income
        
        monthly_return = investment_return / 12
        monthly_inflation = inflation_rate / 12
        monthly_income_growth = income_growth / 12
        
        for month in range(1, months + 1):
            # Update income annually
            if month % 12 == 0:
                current_income *= (1 + income_growth)
            
            monthly_savings = current_income * self.savings_rate / 12
            
            # Investment growth
            wealth = wealth * (1 + monthly_return) + monthly_savings
            total_contrib += monthly_savings
            
            # Calculate real (inflation-adjusted) wealth
            real_wealth = wealth / ((1 + monthly_inflation) ** month)
            investment_gains = wealth - total_contrib
            
            # Store data
            data['nominal_wealth'].append(wealth)
            data['real_wealth'].append(real_wealth)
            data['total_contributions'].append(total_contrib)
            data['investment_gains'].append(investment_gains)
            data['income'].append(current_income)
            data['expenses'].append(self.expenses)
        
        return pd.DataFrame(data)
    
    def calculate_fire_number(self, annual_expenses: float, withdrawal_rate: float = 0.04) -> float:
        """Calculate Financial Independence, Retire Early (FIRE) number."""
        return annual_expenses / withdrawal_rate
    
    def time_to_fire(
        self, 
        target_wealth: float, 
        investment_return: float
    ) -> Tuple[int, pd.DataFrame]:
        """Calculate months needed to reach FIRE number."""
        wealth = 0
        month = 0
        monthly_return = investment_return / 12
        
        while wealth < target_wealth and month < 600:  # Max 50 years
            wealth = wealth * (1 + monthly_return) + self.monthly_savings
            month += 1
        
        years = month / 12
        return years, self.calculate_wealth_projection(int(years) + 1, investment_return, 0.03)