"""
Data Anonymization Module

Provides various anonymization techniques for protecting sensitive data.
"""

import re
import hashlib
import random
from typing import Any, Dict, List, Optional, Union
from datetime import datetime, timedelta


class DataAnonymizer:
    """Handles data anonymization and privacy protection."""
    
    def __init__(self, seed: Optional[int] = None):
        """Initialize the anonymizer with optional seed."""
        self.seed = seed
        if seed is not None:
            random.seed(seed)
    
    def anonymize_data(self, data: List[Any], field_type: str, 
                      anonymization_level: str = "medium", **kwargs) -> List[Any]:
        """Anonymize data based on field type and privacy level."""
        if anonymization_level == "low":
            return data  # No anonymization
        elif anonymization_level == "medium":
            return self._medium_anonymization(data, field_type, **kwargs)
        elif anonymization_level == "high":
            return self._high_anonymization(data, field_type, **kwargs)
        else:
            return data
    
    def _medium_anonymization(self, data: List[Any], field_type: str, **kwargs) -> List[Any]:
        """Apply medium-level anonymization."""
        if field_type in ['email', 'name', 'phone', 'address']:
            return self._mask_pii(data, field_type)
        elif field_type in ['date', 'datetime']:
            return self._fuzz_dates(data, days_range=30)
        elif field_type in ['integer', 'float']:
            return self._add_noise(data, noise_level=0.1)
        else:
            return data
    
    def _high_anonymization(self, data: List[Any], field_type: str, **kwargs) -> List[Any]:
        """Apply high-level anonymization."""
        if field_type in ['email', 'name', 'phone', 'address']:
            return self._pseudonymize(data, field_type)
        elif field_type in ['date', 'datetime']:
            return self._fuzz_dates(data, days_range=365)
        elif field_type in ['integer', 'float']:
            return self._add_noise(data, noise_level=0.2)
        else:
            return self._generalize_data(data, field_type)
    
    def _mask_pii(self, data: List[Any], field_type: str) -> List[Any]:
        """Mask personally identifiable information."""
        anonymized = []
        
        for item in data:
            if item is None:
                anonymized.append(None)
                continue
                
            item_str = str(item)
            
            if field_type == 'email':
                # Mask email: j***@example.com
                if '@' in item_str:
                    parts = item_str.split('@')
                    if len(parts[0]) > 1:
                        masked = parts[0][0] + '*' * (len(parts[0]) - 1)
                        anonymized.append(f"{masked}@{parts[1]}")
                    else:
                        anonymized.append(f"*@{parts[1]}")
                else:
                    anonymized.append(item_str)
            
            elif field_type == 'name':
                # Mask name: J*** S***
                words = item_str.split()
                masked_words = []
                for word in words:
                    if len(word) > 1:
                        masked_words.append(word[0] + '*' * (len(word) - 1))
                    else:
                        masked_words.append(word)
                anonymized.append(' '.join(masked_words))
            
            elif field_type == 'phone':
                # Mask phone: ***-***-1234
                digits = re.sub(r'\D', '', item_str)
                if len(digits) >= 4:
                    masked = '*' * (len(digits) - 4) + digits[-4:]
                    # Restore original format
                    if '-' in item_str:
                        masked = masked[:3] + '-' + masked[3:6] + '-' + masked[6:]
                    elif '(' in item_str:
                        masked = '(' + masked[:3] + ') ' + masked[3:6] + '-' + masked[6:]
                    anonymized.append(masked)
                else:
                    anonymized.append('***-***-****')
            
            elif field_type == 'address':
                # Mask address: 123 *** St
                words = item_str.split()
                if words:
                    # Keep first part (number) and mask the rest
                    masked_words = [words[0]]
                    for word in words[1:]:
                        if len(word) > 2:
                            masked_words.append(word[0] + '*' * (len(word) - 1))
                        else:
                            masked_words.append('**')
                    anonymized.append(' '.join(masked_words))
                else:
                    anonymized.append('*** *** ***')
            
            else:
                anonymized.append(item_str)
        
        return anonymized
    
    def _pseudonymize(self, data: List[Any], field_type: str) -> List[Any]:
        """Replace data with pseudonyms."""
        anonymized = []
        pseudonym_map = {}
        
        for item in data:
            if item is None:
                anonymized.append(None)
                continue
            
            item_str = str(item)
            
            if item_str not in pseudonym_map:
                if field_type == 'email':
                    pseudonym_map[item_str] = f"user{len(pseudonym_map)+1}@example.com"
                elif field_type == 'name':
                    pseudonym_map[item_str] = f"Person {len(pseudonym_map)+1}"
                elif field_type == 'phone':
                    pseudonym_map[item_str] = f"555-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
                elif field_type == 'address':
                    pseudonym_map[item_str] = f"{random.randint(100, 9999)} Anonymized St"
                else:
                    pseudonym_map[item_str] = f"Pseudonym_{len(pseudonym_map)+1}"
            
            anonymized.append(pseudonym_map[item_str])
        
        return anonymized
    
    def _fuzz_dates(self, data: List[Any], days_range: int = 30) -> List[Any]:
        """Add random noise to dates."""
        anonymized = []
        
        for item in data:
            if item is None:
                anonymized.append(None)
                continue
            
            try:
                if isinstance(item, datetime):
                    # Add random days
                    random_days = random.randint(-days_range, days_range)
                    anonymized.append(item + timedelta(days=random_days))
                elif isinstance(item, str):
                    # Try to parse as date
                    try:
                        date_obj = datetime.strptime(item, '%Y-%m-%d')
                        random_days = random.randint(-days_range, days_range)
                        new_date = date_obj + timedelta(days=random_days)
                        anonymized.append(new_date.strftime('%Y-%m-%d'))
                    except:
                        anonymized.append(item)
                else:
                    anonymized.append(item)
            except:
                anonymized.append(item)
        
        return anonymized
    
    def _add_noise(self, data: List[Any], noise_level: float = 0.1) -> List[Any]:
        """Add random noise to numeric data."""
        anonymized = []
        
        for item in data:
            if item is None:
                anonymized.append(None)
                continue
            
            try:
                if isinstance(item, (int, float)):
                    # Add percentage-based noise
                    noise = random.uniform(-noise_level, noise_level)
                    new_value = item * (1 + noise)
                    
                    if isinstance(item, int):
                        anonymized.append(int(round(new_value)))
                    else:
                        anonymized.append(round(new_value, 2))
                else:
                    anonymized.append(item)
            except:
                anonymized.append(item)
        
        return anonymized
    
    def _generalize_data(self, data: List[Any], field_type: str) -> List[Any]:
        """Generalize data to reduce specificity."""
        anonymized = []
        
        for item in data:
            if item is None:
                anonymized.append(None)
                continue
            
            item_str = str(item)
            
            if field_type == 'city':
                # Generalize to state/region
                anonymized.append("Generalized Location")
            elif field_type == 'zip_code':
                # Generalize to first 3 digits
                if len(item_str) >= 3:
                    anonymized.append(item_str[:3] + "**")
                else:
                    anonymized.append("***")
            elif field_type == 'age':
                # Generalize to age ranges
                try:
                    age = int(item_str)
                    if age < 18:
                        anonymized.append("Under 18")
                    elif age < 25:
                        anonymized.append("18-24")
                    elif age < 35:
                        anonymized.append("25-34")
                    elif age < 50:
                        anonymized.append("35-49")
                    else:
                        anonymized.append("50+")
                except:
                    anonymized.append("Unknown")
            else:
                anonymized.append("Generalized")
        
        return anonymized
    
    def detect_pii(self, data: List[Any], field_name: str) -> Dict[str, Any]:
        """Detect potential PII in data."""
        pii_patterns = {
            'email': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'phone': r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            'ssn': r'\b\d{3}-\d{2}-\d{4}\b',
            'credit_card': r'\b\d{4}[-\s]?\d{4}[-\s]?\d{4}[-\s]?\d{4}\b',
            'ip_address': r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b'
        }
        
        detection_results = {
            'field_name': field_name,
            'total_records': len(data),
            'pii_detected': False,
            'pii_types': [],
            'risk_level': 'low'
        }
        
        for pii_type, pattern in pii_patterns.items():
            matches = 0
            for item in data:
                if item and re.search(pattern, str(item)):
                    matches += 1
            
            if matches > 0:
                detection_results['pii_detected'] = True
                detection_results['pii_types'].append({
                    'type': pii_type,
                    'matches': matches,
                    'percentage': (matches / len(data)) * 100
                })
        
        # Determine risk level
        if detection_results['pii_detected']:
            high_risk_types = ['ssn', 'credit_card']
            if any(pii['type'] in high_risk_types for pii in detection_results['pii_types']):
                detection_results['risk_level'] = 'high'
            else:
                detection_results['risk_level'] = 'medium'
        
        return detection_results
