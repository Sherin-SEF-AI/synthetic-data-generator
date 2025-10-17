"""
Numeric Data Generator

Generates various types of numeric data including integers, floats, percentages, etc.
"""

import random
import numpy as np
from typing import Any, Dict, List, Optional, Union
from .base_generator import BaseGenerator


class NumericGenerator(BaseGenerator):
    """Generator for numeric data types."""
    
    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed)
        self.numeric_types = {
            'integer': self._generate_integer,
            'float': self._generate_float,
            'percentage': self._generate_percentage,
            'currency': self._generate_currency,
            'id': self._generate_id,
            'transaction_amount': self._generate_transaction_amount,
            'salary': self._generate_salary,
            'age': self._generate_age,
            'temperature': self._generate_temperature,
            'humidity': self._generate_humidity,
            'latitude': self._generate_latitude,
            'longitude': self._generate_longitude,
            'rating': self._generate_rating,
            'score': self._generate_score
        }
    
    def generate(self, count: int, numeric_type: str = 'integer', **kwargs) -> List[Union[int, float]]:
        """Generate numeric data of specified type."""
        if numeric_type not in self.numeric_types:
            raise ValueError(f"Unknown numeric type: {numeric_type}")
        
        generator_func = self.numeric_types[numeric_type]
        data = []
        
        for _ in range(count):
            try:
                value = generator_func(**kwargs)
                data.append(value)
            except Exception as e:
                # Fallback to basic integer generation
                data.append(random.randint(1, 100))
        
        # Apply constraints
        data = self.apply_constraints(data, kwargs)
        
        # Apply outliers if specified
        if 'outlier_percentage' in kwargs:
            data = self.introduce_outliers(data, kwargs['outlier_percentage'])
        
        return data
    
    def _generate_integer(self, min_val: int = 0, max_val: int = 100, **kwargs) -> int:
        """Generate a random integer within range."""
        return random.randint(min_val, max_val)
    
    def _generate_float(self, min_val: float = 0.0, max_val: float = 100.0, 
                       decimal_places: int = 2, **kwargs) -> float:
        """Generate a random float within range."""
        value = random.uniform(min_val, max_val)
        return round(value, decimal_places)
    
    def _generate_percentage(self, min_val: float = 0.0, max_val: float = 100.0, **kwargs) -> float:
        """Generate a percentage value."""
        return round(random.uniform(min_val, max_val), 2)
    
    def _generate_currency(self, min_val: float = 0.0, max_val: float = 10000.0, **kwargs) -> float:
        """Generate a currency amount."""
        return round(random.uniform(min_val, max_val), 2)
    
    def _generate_id(self, prefix: str = '', min_val: int = 1, max_val: int = 999999, **kwargs) -> int:
        """Generate a numeric ID."""
        return random.randint(min_val, max_val)
    
    def _generate_transaction_amount(self, min_val: float = 0.01, max_val: float = 10000.0, **kwargs) -> float:
        """Generate a transaction amount."""
        # Use log-normal distribution for more realistic transaction amounts
        mu = np.log(100)  # Mean of log
        sigma = 1.0       # Standard deviation of log
        value = np.random.lognormal(mu, sigma)
        return round(min(max(value, min_val), max_val), 2)
    
    def _generate_salary(self, min_val: float = 30000.0, max_val: float = 200000.0, **kwargs) -> float:
        """Generate a salary amount."""
        # Use normal distribution for salaries
        mean = (min_val + max_val) / 2
        std = (max_val - min_val) / 6
        value = np.random.normal(mean, std)
        return round(max(min(value, max_val), min_val), 2)
    
    def _generate_age(self, min_val: int = 18, max_val: int = 80, **kwargs) -> int:
        """Generate an age value."""
        # Use normal distribution centered around 35
        mean = 35
        std = 15
        value = int(np.random.normal(mean, std))
        return max(min(value, max_val), min_val)
    
    def _generate_temperature(self, min_val: float = -10.0, max_val: float = 40.0, **kwargs) -> float:
        """Generate a temperature value."""
        return round(random.uniform(min_val, max_val), 1)
    
    def _generate_humidity(self, min_val: float = 0.0, max_val: float = 100.0, **kwargs) -> float:
        """Generate a humidity percentage."""
        return round(random.uniform(min_val, max_val), 1)
    
    def _generate_latitude(self, min_val: float = -90.0, max_val: float = 90.0, **kwargs) -> float:
        """Generate a latitude value."""
        return round(random.uniform(min_val, max_val), 6)
    
    def _generate_longitude(self, min_val: float = -180.0, max_val: float = 180.0, **kwargs) -> float:
        """Generate a longitude value."""
        return round(random.uniform(min_val, max_val), 6)
    
    def _generate_rating(self, min_val: float = 1.0, max_val: float = 5.0, **kwargs) -> float:
        """Generate a rating value."""
        return round(random.uniform(min_val, max_val), 1)
    
    def _generate_score(self, min_val: float = 0.0, max_val: float = 100.0, **kwargs) -> float:
        """Generate a score value."""
        # Use normal distribution for scores
        mean = (min_val + max_val) / 2
        std = (max_val - min_val) / 6
        value = np.random.normal(mean, std)
        return round(max(min(value, max_val), min_val), 1)
