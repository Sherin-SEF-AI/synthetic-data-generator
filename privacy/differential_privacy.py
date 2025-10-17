"""
Differential Privacy Module

Implements differential privacy techniques for data generation.
"""

import random
import numpy as np
from typing import Any, Dict, List, Optional, Union
from scipy import stats


class DifferentialPrivacy:
    """Implements differential privacy mechanisms."""
    
    def __init__(self, epsilon: float = 1.0, seed: Optional[int] = None):
        """Initialize differential privacy with privacy parameter epsilon."""
        self.epsilon = epsilon
        self.seed = seed
        if seed is not None:
            random.seed(seed)
            np.random.seed(seed)
    
    def add_laplace_noise(self, data: List[Union[int, float]], 
                         sensitivity: float = 1.0) -> List[Union[int, float]]:
        """Add Laplace noise for differential privacy."""
        if self.epsilon <= 0:
            return data
        
        scale = sensitivity / self.epsilon
        noisy_data = []
        
        for value in data:
            if value is None:
                noisy_data.append(None)
                continue
            
            # Generate Laplace noise
            noise = np.random.laplace(0, scale)
            noisy_value = value + noise
            
            # Round to appropriate precision
            if isinstance(value, int):
                noisy_data.append(int(round(noisy_value)))
            else:
                noisy_data.append(round(noisy_value, 2))
        
        return noisy_data
    
    def add_gaussian_noise(self, data: List[Union[int, float]], 
                          sensitivity: float = 1.0, delta: float = 1e-5) -> List[Union[int, float]]:
        """Add Gaussian noise for differential privacy."""
        if self.epsilon <= 0:
            return data
        
        # Calculate noise scale for Gaussian mechanism
        scale = sensitivity * np.sqrt(2 * np.log(1.25 / delta)) / self.epsilon
        noisy_data = []
        
        for value in data:
            if value is None:
                noisy_data.append(None)
                continue
            
            # Generate Gaussian noise
            noise = np.random.normal(0, scale)
            noisy_value = value + noise
            
            # Round to appropriate precision
            if isinstance(value, int):
                noisy_data.append(int(round(noisy_value)))
            else:
                noisy_data.append(round(noisy_value, 2))
        
        return noisy_data
    
    def apply_private_histogram(self, data: List[Any], bins: int = 10) -> Dict[str, Any]:
        """Create a differentially private histogram."""
        if not data:
            return {'bins': [], 'counts': [], 'privacy_budget_used': 0}
        
        # Remove None values
        clean_data = [x for x in data if x is not None]
        if not clean_data:
            return {'bins': [], 'counts': [], 'privacy_budget_used': 0}
        
        # Create histogram
        if isinstance(clean_data[0], (int, float)):
            # Numeric data
            hist, bin_edges = np.histogram(clean_data, bins=bins)
            bin_centers = [(bin_edges[i] + bin_edges[i+1]) / 2 for i in range(len(bin_edges)-1)]
        else:
            # Categorical data
            unique_values, counts = np.unique(clean_data, return_counts=True)
            hist = counts
            bin_centers = unique_values.tolist()
        
        # Add Laplace noise to counts
        sensitivity = 1.0  # Adding/removing one record changes count by at most 1
        noisy_counts = []
        
        for count in hist:
            noise = np.random.laplace(0, sensitivity / self.epsilon)
            noisy_count = max(0, int(round(count + noise)))  # Ensure non-negative
            noisy_counts.append(noisy_count)
        
        return {
            'bins': bin_centers,
            'counts': noisy_counts,
            'privacy_budget_used': self.epsilon
        }
    
    def private_mean(self, data: List[Union[int, float]], 
                    sensitivity: float = 1.0) -> float:
        """Compute differentially private mean."""
        if not data:
            return 0.0
        
        clean_data = [x for x in data if x is not None]
        if not clean_data:
            return 0.0
        
        # Calculate true mean
        true_mean = np.mean(clean_data)
        
        # Add noise
        noise = np.random.laplace(0, sensitivity / self.epsilon)
        private_mean = true_mean + noise
        
        return round(private_mean, 2)
    
    def private_median(self, data: List[Union[int, float]], 
                      sensitivity: float = 1.0) -> float:
        """Compute differentially private median."""
        if not data:
            return 0.0
        
        clean_data = [x for x in data if x is not None]
        if not clean_data:
            return 0.0
        
        # Calculate true median
        true_median = np.median(clean_data)
        
        # Add noise
        noise = np.random.laplace(0, sensitivity / self.epsilon)
        private_median = true_median + noise
        
        return round(private_median, 2)
    
    def private_std(self, data: List[Union[int, float]], 
                   sensitivity: float = 1.0) -> float:
        """Compute differentially private standard deviation."""
        if not data:
            return 0.0
        
        clean_data = [x for x in data if x is not None]
        if not clean_data:
            return 0.0
        
        # Calculate true standard deviation
        true_std = np.std(clean_data)
        
        # Add noise
        noise = np.random.laplace(0, sensitivity / self.epsilon)
        private_std = max(0, true_std + noise)  # Ensure non-negative
        
        return round(private_std, 2)
    
    def apply_private_aggregation(self, data: List[Union[int, float]]) -> Dict[str, Any]:
        """Apply differential privacy to common aggregations."""
        if not data:
            return {
                'mean': 0.0,
                'median': 0.0,
                'std': 0.0,
                'min': 0.0,
                'max': 0.0,
                'privacy_budget_used': 0
            }
        
        clean_data = [x for x in data if x is not None]
        if not clean_data:
            return {
                'mean': 0.0,
                'median': 0.0,
                'std': 0.0,
                'min': 0.0,
                'max': 0.0,
                'privacy_budget_used': 0
            }
        
        # Calculate range for sensitivity
        data_range = max(clean_data) - min(clean_data)
        sensitivity = data_range / len(clean_data) if len(clean_data) > 0 else 1.0
        
        # Apply differential privacy to statistics
        private_stats = {
            'mean': self.private_mean(clean_data, sensitivity),
            'median': self.private_median(clean_data, sensitivity),
            'std': self.private_std(clean_data, sensitivity),
            'min': min(clean_data),  # Min/max are less sensitive
            'max': max(clean_data),
            'privacy_budget_used': self.epsilon
        }
        
        return private_stats
    
    def check_k_anonymity(self, data: List[Dict[str, Any]], 
                         quasi_identifiers: List[str], k: int = 3) -> Dict[str, Any]:
        """Check k-anonymity property of the dataset."""
        if not data or not quasi_identifiers:
            return {
                'k_anonymity_satisfied': True,
                'min_group_size': float('inf'),
                'violations': 0,
                'total_groups': 0
            }
        
        # Group records by quasi-identifiers
        groups = {}
        for record in data:
            key = tuple(record.get(qi, '') for qi in quasi_identifiers)
            if key not in groups:
                groups[key] = []
            groups[key].append(record)
        
        # Check k-anonymity
        violations = 0
        min_group_size = float('inf')
        
        for group_key, group_records in groups.items():
            group_size = len(group_records)
            min_group_size = min(min_group_size, group_size)
            if group_size < k:
                violations += 1
        
        return {
            'k_anonymity_satisfied': violations == 0,
            'min_group_size': min_group_size if min_group_size != float('inf') else 0,
            'violations': violations,
            'total_groups': len(groups),
            'k': k
        }
