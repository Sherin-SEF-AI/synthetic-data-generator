"""
Text Data Generator

Generates various types of text data including names, emails, addresses, etc.
"""

import re
import random
from typing import Any, Dict, List, Optional
from .base_generator import BaseGenerator


class TextGenerator(BaseGenerator):
    """Generator for text-based data types."""
    
    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed)
        self.text_types = {
            'name': self._generate_name,
            'email': self._generate_email,
            'address': self._generate_address,
            'phone': self._generate_phone,
            'company': self._generate_company,
            'job_title': self._generate_job_title,
            'description': self._generate_description,
            'sentence': self._generate_sentence,
            'paragraph': self._generate_paragraph,
            'url': self._generate_url,
            'user_agent': self._generate_user_agent,
            'mac_address': self._generate_mac_address,
            'credit_card': self._generate_credit_card,
            'bank_account': self._generate_bank_account,
            'patient_id': self._generate_patient_id,
            'medical_record': self._generate_medical_record,
            'diagnosis_code': self._generate_diagnosis_code,
            'medication': self._generate_medication,
            'country': self._generate_country,
            'city': self._generate_city,
            'zip_code': self._generate_zip_code,
            'ipv4': self._generate_ipv4,
            'ipv6': self._generate_ipv6,
            'custom': self._generate_custom_text
        }
    
    def generate(self, count: int, text_type: str = 'name', **kwargs) -> List[str]:
        """Generate text data of specified type."""
        if text_type not in self.text_types:
            raise ValueError(f"Unknown text type: {text_type}")
        
        generator_func = self.text_types[text_type]
        data = []
        
        for _ in range(count):
            try:
                value = generator_func(**kwargs)
                data.append(value)
            except Exception as e:
                # Fallback to basic text generation
                data.append(f"Generated_{random.randint(1000, 9999)}")
        
        # Apply constraints
        data = self.apply_constraints(data, kwargs)
        
        return data
    
    def _generate_name(self, **kwargs) -> str:
        """Generate a person's name."""
        return self.fake.name()
    
    def _generate_email(self, **kwargs) -> str:
        """Generate an email address."""
        return self.fake.email()
    
    def _generate_address(self, **kwargs) -> str:
        """Generate a street address."""
        return self.fake.street_address()
    
    def _generate_phone(self, **kwargs) -> str:
        """Generate a phone number."""
        return self.fake.phone_number()
    
    def _generate_company(self, **kwargs) -> str:
        """Generate a company name."""
        return self.fake.company()
    
    def _generate_job_title(self, **kwargs) -> str:
        """Generate a job title."""
        return self.fake.job()
    
    def _generate_description(self, **kwargs) -> str:
        """Generate a product description."""
        return self.fake.text(max_nb_chars=200)
    
    def _generate_sentence(self, **kwargs) -> str:
        """Generate a sentence."""
        return self.fake.sentence()
    
    def _generate_paragraph(self, **kwargs) -> str:
        """Generate a paragraph."""
        return self.fake.paragraph()
    
    def _generate_url(self, **kwargs) -> str:
        """Generate a URL."""
        return self.fake.url()
    
    def _generate_user_agent(self, **kwargs) -> str:
        """Generate a user agent string."""
        return self.fake.user_agent()
    
    def _generate_mac_address(self, **kwargs) -> str:
        """Generate a MAC address."""
        return self.fake.mac_address()
    
    def _generate_credit_card(self, **kwargs) -> str:
        """Generate a credit card number."""
        return self.fake.credit_card_number()
    
    def _generate_bank_account(self, **kwargs) -> str:
        """Generate a bank account number."""
        return self.fake.bban()
    
    def _generate_patient_id(self, **kwargs) -> str:
        """Generate a patient ID."""
        return f"PAT{random.randint(100000, 999999)}"
    
    def _generate_medical_record(self, **kwargs) -> str:
        """Generate a medical record number."""
        return f"MR{random.randint(1000000, 9999999)}"
    
    def _generate_diagnosis_code(self, **kwargs) -> str:
        """Generate an ICD-10 diagnosis code."""
        codes = ['A00', 'B00', 'C00', 'D00', 'E00', 'F00', 'G00', 'H00', 'I00', 'J00']
        return f"{random.choice(codes)}.{random.randint(0, 9)}"
    
    def _generate_medication(self, **kwargs) -> str:
        """Generate a medication name."""
        medications = [
            'Acetaminophen', 'Ibuprofen', 'Aspirin', 'Lisinopril', 'Metformin',
            'Amlodipine', 'Omeprazole', 'Simvastatin', 'Losartan', 'Albuterol'
        ]
        return random.choice(medications)
    
    def _generate_country(self, **kwargs) -> str:
        """Generate a country name."""
        return self.fake.country()
    
    def _generate_city(self, **kwargs) -> str:
        """Generate a city name."""
        return self.fake.city()
    
    def _generate_zip_code(self, **kwargs) -> str:
        """Generate a ZIP code."""
        return self.fake.zipcode()
    
    def _generate_ipv4(self, **kwargs) -> str:
        """Generate an IPv4 address."""
        return self.fake.ipv4()
    
    def _generate_ipv6(self, **kwargs) -> str:
        """Generate an IPv6 address."""
        return self.fake.ipv6()
    
    def _generate_custom_text(self, pattern: str = None, **kwargs) -> str:
        """Generate custom text based on pattern."""
        if pattern:
            try:
                # Simple pattern matching for common cases
                if '{name}' in pattern:
                    pattern = pattern.replace('{name}', self.fake.name())
                if '{email}' in pattern:
                    pattern = pattern.replace('{email}', self.fake.email())
                if '{company}' in pattern:
                    pattern = pattern.replace('{company}', self.fake.company())
                return pattern
            except:
                pass
        
        # Fallback to random text
        return self.fake.word()
