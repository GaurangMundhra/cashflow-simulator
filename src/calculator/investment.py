import numpy as np
import pandas as pd
from typing import List, Dict

class InvestmentAnalyzer:
    @staticmethod
    def compound_interest(
        principal: float,
        rate: float,
        time: int,
        contribution: float = 0,
        frequency: int = 12
    ) -> float:
        """Calculate compound interest with regular contributions."""
        if contribution == 0:
            return principal * (1 + rate/frequency) ** (frequency * time)
        
        # Future value of contributions
        fv_contributions = contribution * (
            ((1 + rate/frequency) ** (frequency * time) - 1) / (rate/frequency)
        )
        
        # Future value of principal
        fv_principal = principal * (1 + rate/frequency) ** (frequency * time)
        
        return fv_principal + fv_contributions
    
    @staticmethod
    def calculate_returns_breakdown(
        monthly_contribution: float,
        years: int,
        annual_return: float
    ) -> Dict[str, float]:
        """Break down total wealth into contributions vs returns."""
        total_contributions = monthly_contribution * 12 * years
        
        final_wealth = InvestmentAnalyzer.compound_interest(
            0, annual_return, years, monthly_contribution, 12
        )
        
        investment_gains = final_wealth - total_contributions
        
        return {
            'total_wealth': final_wealth,
            'contributions': total_contributions,
            'gains': investment_gains,
            'gain_percentage': (investment_gains / total_contributions * 100) if total_contributions > 0 else 0
        }
    
    @staticmethod
    def compare_scenarios(
        base_savings: float,
        years: int,
        scenarios: List[Dict]
    ) -> pd.DataFrame:
        """Compare different investment scenarios."""
        results = []
        
        for scenario in scenarios:
            name = scenario['name']
            rate = scenario['rate']
            contribution = scenario.get('contribution', base_savings)
            
            final = InvestmentAnalyzer.compound_interest(
                0, rate, years, contribution, 12
            )
            
            results.append({
                'Scenario': name,
                'Monthly Contribution': contribution,
                'Annual Return': f"{rate*100:.1f}%",
                'Final Wealth': final,
                'Total Contributions': contribution * 12 * years,
                'Investment Gains': final - (contribution * 12 * years)
            })
        
        return pd.DataFrame(results)