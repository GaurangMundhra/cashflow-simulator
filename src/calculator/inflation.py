import numpy as np
import pandas as pd

class InflationCalculator:
    @staticmethod
    def adjust_for_inflation(
        amount: float,
        years: float,
        inflation_rate: float
    ) -> float:
        """Calculate inflation-adjusted value."""
        return amount / ((1 + inflation_rate) ** years)
    
    @staticmethod
    def calculate_purchasing_power(
        amounts: np.array,
        inflation_rate: float
    ) -> np.array:
        """Calculate purchasing power over time."""
        years = np.arange(len(amounts)) / 12  # Assuming monthly data
        return amounts / ((1 + inflation_rate) ** years)
    
    @staticmethod
    def real_vs_nominal_comparison(
        nominal_values: np.array,
        inflation_rate: float
    ) -> pd.DataFrame:
        """Create comparison dataframe."""
        real_values = InflationCalculator.calculate_purchasing_power(
            nominal_values, inflation_rate
        )
        
        return pd.DataFrame({
            'Nominal': nominal_values,
            'Real (Inflation-Adjusted)': real_values,
            'Inflation_Impact': nominal_values - real_values
        })