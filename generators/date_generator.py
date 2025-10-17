"""
Date Data Generator

Generates various types of date and time data.
"""

import random
from datetime import datetime, timedelta, date, time
from typing import Any, Dict, List, Optional, Union
from .base_generator import BaseGenerator


class DateGenerator(BaseGenerator):
    """Generator for date and time data types."""
    
    def __init__(self, seed: Optional[int] = None):
        super().__init__(seed)
        self.date_types = {
            'date': self._generate_date,
            'datetime': self._generate_datetime,
            'time': self._generate_time,
            'date_range': self._generate_date_range,
            'signup_date': self._generate_signup_date,
            'transaction_date': self._generate_transaction_date,
            'hire_date': self._generate_hire_date,
            'visit_date': self._generate_visit_date,
            'post_date': self._generate_post_date,
            'sensor_timestamp': self._generate_sensor_timestamp
        }
    
    def generate(self, count: int, date_type: str = 'date', **kwargs) -> List[Union[date, datetime, time, str]]:
        """Generate date/time data of specified type."""
        if date_type not in self.date_types:
            raise ValueError(f"Unknown date type: {date_type}")
        
        generator_func = self.date_types[date_type]
        data = []
        
        for _ in range(count):
            try:
                value = generator_func(**kwargs)
                data.append(value)
            except Exception as e:
                # Fallback to current date
                data.append(datetime.now())
        
        # Apply constraints
        data = self.apply_constraints(data, kwargs)
        
        return data
    
    def _generate_date(self, start_date: str = '2020-01-01', end_date: str = '2024-12-31', **kwargs) -> date:
        """Generate a random date within range."""
        start = datetime.strptime(start_date, '%Y-%m-%d').date()
        end = datetime.strptime(end_date, '%Y-%m-%d').date()
        
        time_between = end - start
        days_between = time_between.days
        random_days = random.randint(0, days_between)
        
        return start + timedelta(days=random_days)
    
    def _generate_datetime(self, start_date: str = '2020-01-01', end_date: str = '2024-12-31', **kwargs) -> datetime:
        """Generate a random datetime within range."""
        start = datetime.strptime(start_date, '%Y-%m-%d')
        end = datetime.strptime(end_date, '%Y-%m-%d')
        
        time_between = end - start
        seconds_between = time_between.total_seconds()
        random_seconds = random.randint(0, int(seconds_between))
        
        return start + timedelta(seconds=random_seconds)
    
    def _generate_time(self, start_time: str = '00:00:00', end_time: str = '23:59:59', **kwargs) -> time:
        """Generate a random time within range."""
        start = datetime.strptime(start_time, '%H:%M:%S').time()
        end = datetime.strptime(end_time, '%H:%M:%S').time()
        
        start_seconds = start.hour * 3600 + start.minute * 60 + start.second
        end_seconds = end.hour * 3600 + end.minute * 60 + end.second
        
        random_seconds = random.randint(start_seconds, end_seconds)
        
        hours = random_seconds // 3600
        minutes = (random_seconds % 3600) // 60
        seconds = random_seconds % 60
        
        return time(hours, minutes, seconds)
    
    def _generate_date_range(self, start_date: str = '2020-01-01', end_date: str = '2024-12-31', **kwargs) -> str:
        """Generate a date range as string."""
        start = self._generate_date(start_date, end_date)
        end = start + timedelta(days=random.randint(1, 30))
        return f"{start} to {end}"
    
    def _generate_signup_date(self, start_date: str = '2020-01-01', end_date: str = '2024-12-31', **kwargs) -> datetime:
        """Generate a signup date with realistic patterns."""
        # More signups on weekdays
        if random.random() < 0.7:  # 70% chance of weekday
            # Generate weekday date
            base_date = self._generate_datetime(start_date, end_date)
            # Adjust to nearest weekday if needed
            while base_date.weekday() >= 5:  # Saturday = 5, Sunday = 6
                base_date += timedelta(days=1)
        else:
            base_date = self._generate_datetime(start_date, end_date)
        
        return base_date
    
    def _generate_transaction_date(self, start_date: str = '2020-01-01', end_date: str = '2024-12-31', **kwargs) -> datetime:
        """Generate a transaction date with realistic patterns."""
        # More transactions during business hours
        base_date = self._generate_datetime(start_date, end_date)
        
        # Adjust to business hours (9 AM - 5 PM)
        if random.random() < 0.6:  # 60% during business hours
            hour = random.randint(9, 17)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            base_date = base_date.replace(hour=hour, minute=minute, second=second)
        
        return base_date
    
    def _generate_hire_date(self, start_date: str = '2020-01-01', end_date: str = '2024-12-31', **kwargs) -> date:
        """Generate a hire date."""
        return self._generate_date(start_date, end_date)
    
    def _generate_visit_date(self, start_date: str = '2020-01-01', end_date: str = '2024-12-31', **kwargs) -> datetime:
        """Generate a medical visit date."""
        return self._generate_datetime(start_date, end_date)
    
    def _generate_post_date(self, start_date: str = '2020-01-01', end_date: str = '2024-12-31', **kwargs) -> datetime:
        """Generate a social media post date."""
        # More posts during evening hours
        base_date = self._generate_datetime(start_date, end_date)
        
        if random.random() < 0.4:  # 40% during evening (6 PM - 11 PM)
            hour = random.randint(18, 23)
            minute = random.randint(0, 59)
            second = random.randint(0, 59)
            base_date = base_date.replace(hour=hour, minute=minute, second=second)
        
        return base_date
    
    def _generate_sensor_timestamp(self, start_date: str = '2020-01-01', end_date: str = '2024-12-31', **kwargs) -> datetime:
        """Generate a sensor timestamp with regular intervals."""
        base_date = self._generate_datetime(start_date, end_date)
        
        # Round to nearest minute for sensor data
        base_date = base_date.replace(second=0, microsecond=0)
        
        return base_date
