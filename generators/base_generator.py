"""
Base Generator Class

Abstract base class for all data generators with common functionality.
"""

from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Union
import random
import numpy as np
from faker import Faker


class BaseGenerator(ABC):
    """Base class for all data generators."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize the generator with optional seed for reproducibility."""
        self.seed = seed
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
        self.fake = Faker()
        if seed is not None:
            Faker.seed(seed)
    
    @abstractmethod
    def generate(self, count: int, **kwargs) -> List[Any]:
        """Generate synthetic data of the specified type."""
        pass
    
    def apply_constraints(self, data: List[Any], constraints: Dict[str, Any]) -> List[Any]:
        """Apply constraints to generated data."""
        if not constraints:
            return data
        
        # Apply null percentage
        if 'null_percentage' in constraints:
            null_pct = constraints['null_percentage']
            if null_pct > 0:
                null_indices = random.sample(
                    range(len(data)), 
                    int(len(data) * null_pct / 100)
                )
                for idx in null_indices:
                    data[idx] = None
        
        # Apply unique constraint
        if constraints.get('unique', False):
            data = list(set(data))
            # If we lost data due to uniqueness, regenerate
            while len(data) < len(data):
                new_data = self.generate(1, **{k: v for k, v in constraints.items() if k not in ['unique', 'null_percentage']})
                if new_data[0] not in data:
                    data.append(new_data[0])
        
        return data
    
    def introduce_outliers(self, data: List[Any], outlier_percentage: float) -> List[Any]:
        """Introduce outliers into numeric data."""
        if outlier_percentage <= 0 or not data:
            return data
        
        outlier_count = int(len(data) * outlier_percentage / 100)
        outlier_indices = random.sample(range(len(data)), outlier_count)
        
        for idx in outlier_indices:
            if isinstance(data[idx], (int, float)) and data[idx] is not None:
                # Create outlier by multiplying by random factor
                factor = random.choice([0.1, 10, 100])
                data[idx] = data[idx] * factor
        
        return data
    
    def create_duplicates(self, data: List[Any], duplicate_percentage: float) -> List[Any]:
        """Create duplicates in the data."""
        if duplicate_percentage <= 0 or not data:
            return data
        
        duplicate_count = int(len(data) * duplicate_percentage / 100)
        duplicates = random.choices(data, k=duplicate_count)
        
        return data + duplicates
