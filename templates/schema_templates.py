"""
Schema Templates

Pre-built schema templates for common data generation use cases.
"""

from typing import Dict, List, Any


class SchemaTemplates:
    """Collection of pre-built schema templates."""
    
    @staticmethod
    def get_all_templates() -> Dict[str, Dict[str, Any]]:
        """Get all available templates."""
        return {
            'customer_database': SchemaTemplates.customer_database(),
            'ecommerce_transactions': SchemaTemplates.ecommerce_transactions(),
            'employee_records': SchemaTemplates.employee_records(),
            'healthcare_records': SchemaTemplates.healthcare_records(),
            'social_media_posts': SchemaTemplates.social_media_posts(),
            'iot_sensor_data': SchemaTemplates.iot_sensor_data(),
            'financial_transactions': SchemaTemplates.financial_transactions(),
            'user_clickstream': SchemaTemplates.user_clickstream(),
            'product_catalog': SchemaTemplates.product_catalog(),
            'marketing_campaigns': SchemaTemplates.marketing_campaigns()
        }
    
    @staticmethod
    def customer_database() -> Dict[str, Any]:
        """Customer database template."""
        return {
            'name': 'Customer Database',
            'description': 'Complete customer information with demographics and preferences',
            'fields': [
                {
                    'name': 'customer_id',
                    'type': 'integer',
                    'subtype': 'id',
                    'description': 'Unique customer identifier',
                    'constraints': {'unique': True, 'min_val': 1, 'max_val': 999999}
                },
                {
                    'name': 'first_name',
                    'type': 'text',
                    'subtype': 'name',
                    'description': 'Customer first name',
                    'constraints': {'null_percentage': 2}
                },
                {
                    'name': 'last_name',
                    'type': 'text',
                    'subtype': 'name',
                    'description': 'Customer last name',
                    'constraints': {'null_percentage': 2}
                },
                {
                    'name': 'email',
                    'type': 'text',
                    'subtype': 'email',
                    'description': 'Customer email address',
                    'constraints': {'unique': True, 'null_percentage': 1}
                },
                {
                    'name': 'phone',
                    'type': 'text',
                    'subtype': 'phone',
                    'description': 'Customer phone number',
                    'constraints': {'null_percentage': 5}
                },
                {
                    'name': 'address',
                    'type': 'text',
                    'subtype': 'address',
                    'description': 'Customer street address',
                    'constraints': {'null_percentage': 3}
                },
                {
                    'name': 'city',
                    'type': 'text',
                    'subtype': 'city',
                    'description': 'Customer city',
                    'constraints': {'null_percentage': 3}
                },
                {
                    'name': 'country',
                    'type': 'text',
                    'subtype': 'country',
                    'description': 'Customer country',
                    'constraints': {'null_percentage': 1}
                },
                {
                    'name': 'zip_code',
                    'type': 'text',
                    'subtype': 'zip_code',
                    'description': 'Customer ZIP code',
                    'constraints': {'null_percentage': 3}
                },
                {
                    'name': 'age',
                    'type': 'integer',
                    'subtype': 'age',
                    'description': 'Customer age',
                    'constraints': {'min_val': 18, 'max_val': 80, 'null_percentage': 2}
                },
                {
                    'name': 'signup_date',
                    'type': 'date',
                    'subtype': 'signup_date',
                    'description': 'Customer signup date',
                    'constraints': {'start_date': '2020-01-01', 'end_date': '2024-12-31'}
                },
                {
                    'name': 'lifetime_value',
                    'type': 'float',
                    'subtype': 'currency',
                    'description': 'Customer lifetime value',
                    'constraints': {'min_val': 0.0, 'max_val': 50000.0, 'null_percentage': 1}
                }
            ]
        }
    
    @staticmethod
    def ecommerce_transactions() -> Dict[str, Any]:
        """E-commerce transactions template."""
        return {
            'name': 'E-commerce Transactions',
            'description': 'Online purchase transactions with product and customer details',
            'fields': [
                {
                    'name': 'transaction_id',
                    'type': 'integer',
                    'subtype': 'id',
                    'description': 'Unique transaction identifier',
                    'constraints': {'unique': True, 'min_val': 1000000, 'max_val': 9999999}
                },
                {
                    'name': 'customer_id',
                    'type': 'integer',
                    'subtype': 'id',
                    'description': 'Customer identifier',
                    'constraints': {'min_val': 1, 'max_val': 100000}
                },
                {
                    'name': 'product_name',
                    'type': 'text',
                    'subtype': 'custom',
                    'description': 'Product name',
                    'constraints': {'pattern': '{company} {product_type}'}
                },
                {
                    'name': 'product_category',
                    'type': 'categorical',
                    'subtype': 'custom',
                    'description': 'Product category',
                    'constraints': {'categories': ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Beauty', 'Toys']}
                },
                {
                    'name': 'quantity',
                    'type': 'integer',
                    'subtype': 'integer',
                    'description': 'Quantity purchased',
                    'constraints': {'min_val': 1, 'max_val': 10}
                },
                {
                    'name': 'unit_price',
                    'type': 'float',
                    'subtype': 'currency',
                    'description': 'Price per unit',
                    'constraints': {'min_val': 0.01, 'max_val': 1000.0}
                },
                {
                    'name': 'total_amount',
                    'type': 'float',
                    'subtype': 'currency',
                    'description': 'Total transaction amount',
                    'constraints': {'min_val': 0.01, 'max_val': 10000.0}
                },
                {
                    'name': 'transaction_date',
                    'type': 'date',
                    'subtype': 'transaction_date',
                    'description': 'Transaction date and time',
                    'constraints': {'start_date': '2023-01-01', 'end_date': '2024-12-31'}
                },
                {
                    'name': 'payment_method',
                    'type': 'categorical',
                    'subtype': 'custom',
                    'description': 'Payment method used',
                    'constraints': {'categories': ['Credit Card', 'Debit Card', 'PayPal', 'Apple Pay', 'Google Pay', 'Bank Transfer']}
                },
                {
                    'name': 'shipping_address',
                    'type': 'text',
                    'subtype': 'address',
                    'description': 'Shipping address',
                    'constraints': {'null_percentage': 2}
                }
            ]
        }
    
    @staticmethod
    def employee_records() -> Dict[str, Any]:
        """Employee records template."""
        return {
            'name': 'Employee Records',
            'description': 'HR employee database with job and salary information',
            'fields': [
                {
                    'name': 'employee_id',
                    'type': 'integer',
                    'subtype': 'id',
                    'description': 'Unique employee identifier',
                    'constraints': {'unique': True, 'min_val': 1000, 'max_val': 99999}
                },
                {
                    'name': 'first_name',
                    'type': 'text',
                    'subtype': 'name',
                    'description': 'Employee first name',
                    'constraints': {'null_percentage': 1}
                },
                {
                    'name': 'last_name',
                    'type': 'text',
                    'subtype': 'name',
                    'description': 'Employee last name',
                    'constraints': {'null_percentage': 1}
                },
                {
                    'name': 'email',
                    'type': 'text',
                    'subtype': 'email',
                    'description': 'Employee email address',
                    'constraints': {'unique': True, 'null_percentage': 1}
                },
                {
                    'name': 'department',
                    'type': 'categorical',
                    'subtype': 'custom',
                    'description': 'Employee department',
                    'constraints': {'categories': ['Engineering', 'Marketing', 'Sales', 'HR', 'Finance', 'Operations', 'Customer Support']}
                },
                {
                    'name': 'job_title',
                    'type': 'text',
                    'subtype': 'job_title',
                    'description': 'Employee job title',
                    'constraints': {'null_percentage': 2}
                },
                {
                    'name': 'salary',
                    'type': 'float',
                    'subtype': 'salary',
                    'description': 'Annual salary',
                    'constraints': {'min_val': 30000.0, 'max_val': 200000.0, 'null_percentage': 1}
                },
                {
                    'name': 'hire_date',
                    'type': 'date',
                    'subtype': 'hire_date',
                    'description': 'Employee hire date',
                    'constraints': {'start_date': '2015-01-01', 'end_date': '2024-12-31'}
                },
                {
                    'name': 'manager_id',
                    'type': 'integer',
                    'subtype': 'id',
                    'description': 'Manager employee ID',
                    'constraints': {'min_val': 1000, 'max_val': 99999, 'null_percentage': 20}
                },
                {
                    'name': 'location',
                    'type': 'text',
                    'subtype': 'city',
                    'description': 'Work location',
                    'constraints': {'null_percentage': 3}
                }
            ]
        }
    
    @staticmethod
    def healthcare_records() -> Dict[str, Any]:
        """Healthcare records template."""
        return {
            'name': 'Healthcare Records',
            'description': 'Medical patient records with diagnoses and treatments',
            'fields': [
                {
                    'name': 'patient_id',
                    'type': 'text',
                    'subtype': 'patient_id',
                    'description': 'Unique patient identifier',
                    'constraints': {'unique': True}
                },
                {
                    'name': 'first_name',
                    'type': 'text',
                    'subtype': 'name',
                    'description': 'Patient first name',
                    'constraints': {'null_percentage': 1}
                },
                {
                    'name': 'last_name',
                    'type': 'text',
                    'subtype': 'name',
                    'description': 'Patient last name',
                    'constraints': {'null_percentage': 1}
                },
                {
                    'name': 'age',
                    'type': 'integer',
                    'subtype': 'age',
                    'description': 'Patient age',
                    'constraints': {'min_val': 0, 'max_val': 100, 'null_percentage': 1}
                },
                {
                    'name': 'gender',
                    'type': 'categorical',
                    'subtype': 'custom',
                    'description': 'Patient gender',
                    'constraints': {'categories': ['Male', 'Female', 'Other', 'Prefer not to say']}
                },
                {
                    'name': 'diagnosis_code',
                    'type': 'text',
                    'subtype': 'diagnosis_code',
                    'description': 'ICD-10 diagnosis code',
                    'constraints': {'null_percentage': 2}
                },
                {
                    'name': 'diagnosis_description',
                    'type': 'text',
                    'subtype': 'description',
                    'description': 'Diagnosis description',
                    'constraints': {'null_percentage': 2}
                },
                {
                    'name': 'medication',
                    'type': 'text',
                    'subtype': 'medication',
                    'description': 'Prescribed medication',
                    'constraints': {'null_percentage': 10}
                },
                {
                    'name': 'visit_date',
                    'type': 'date',
                    'subtype': 'visit_date',
                    'description': 'Medical visit date',
                    'constraints': {'start_date': '2023-01-01', 'end_date': '2024-12-31'}
                },
                {
                    'name': 'medical_record_number',
                    'type': 'text',
                    'subtype': 'medical_record',
                    'description': 'Medical record number',
                    'constraints': {'unique': True, 'null_percentage': 1}
                }
            ]
        }
    
    @staticmethod
    def social_media_posts() -> Dict[str, Any]:
        """Social media posts template."""
        return {
            'name': 'Social Media Posts',
            'description': 'Social media content with engagement metrics',
            'fields': [
                {
                    'name': 'post_id',
                    'type': 'integer',
                    'subtype': 'id',
                    'description': 'Unique post identifier',
                    'constraints': {'unique': True, 'min_val': 1000000, 'max_val': 9999999}
                },
                {
                    'name': 'user_id',
                    'type': 'integer',
                    'subtype': 'id',
                    'description': 'User identifier',
                    'constraints': {'min_val': 1, 'max_val': 100000}
                },
                {
                    'name': 'username',
                    'type': 'text',
                    'subtype': 'name',
                    'description': 'Username',
                    'constraints': {'null_percentage': 1}
                },
                {
                    'name': 'post_content',
                    'type': 'text',
                    'subtype': 'paragraph',
                    'description': 'Post content text',
                    'constraints': {'null_percentage': 2}
                },
                {
                    'name': 'likes',
                    'type': 'integer',
                    'subtype': 'integer',
                    'description': 'Number of likes',
                    'constraints': {'min_val': 0, 'max_val': 10000}
                },
                {
                    'name': 'shares',
                    'type': 'integer',
                    'subtype': 'integer',
                    'description': 'Number of shares',
                    'constraints': {'min_val': 0, 'max_val': 1000}
                },
                {
                    'name': 'comments',
                    'type': 'integer',
                    'subtype': 'integer',
                    'description': 'Number of comments',
                    'constraints': {'min_val': 0, 'max_val': 500}
                },
                {
                    'name': 'post_date',
                    'type': 'date',
                    'subtype': 'post_date',
                    'description': 'Post date and time',
                    'constraints': {'start_date': '2023-01-01', 'end_date': '2024-12-31'}
                },
                {
                    'name': 'hashtags',
                    'type': 'text',
                    'subtype': 'custom',
                    'description': 'Post hashtags',
                    'constraints': {'pattern': '#{word} #{word} #{word}', 'null_percentage': 30}
                },
                {
                    'name': 'post_type',
                    'type': 'categorical',
                    'subtype': 'custom',
                    'description': 'Type of post',
                    'constraints': {'categories': ['Text', 'Image', 'Video', 'Link', 'Poll']}
                }
            ]
        }
    
    @staticmethod
    def iot_sensor_data() -> Dict[str, Any]:
        """IoT sensor data template."""
        return {
            'name': 'IoT Sensor Data',
            'description': 'Internet of Things sensor readings with environmental data',
            'fields': [
                {
                    'name': 'device_id',
                    'type': 'text',
                    'subtype': 'custom',
                    'description': 'IoT device identifier',
                    'constraints': {'pattern': 'DEV_{id}'}
                },
                {
                    'name': 'timestamp',
                    'type': 'date',
                    'subtype': 'sensor_timestamp',
                    'description': 'Sensor reading timestamp',
                    'constraints': {'start_date': '2024-01-01', 'end_date': '2024-12-31'}
                },
                {
                    'name': 'temperature',
                    'type': 'float',
                    'subtype': 'temperature',
                    'description': 'Temperature reading (°C)',
                    'constraints': {'min_val': -10.0, 'max_val': 40.0, 'null_percentage': 1}
                },
                {
                    'name': 'humidity',
                    'type': 'float',
                    'subtype': 'humidity',
                    'description': 'Humidity reading (%)',
                    'constraints': {'min_val': 0.0, 'max_val': 100.0, 'null_percentage': 1}
                },
                {
                    'name': 'pressure',
                    'type': 'float',
                    'subtype': 'float',
                    'description': 'Atmospheric pressure (hPa)',
                    'constraints': {'min_val': 950.0, 'max_val': 1050.0, 'null_percentage': 2}
                },
                {
                    'name': 'latitude',
                    'type': 'float',
                    'subtype': 'latitude',
                    'description': 'Device latitude',
                    'constraints': {'min_val': -90.0, 'max_val': 90.0, 'null_percentage': 1}
                },
                {
                    'name': 'longitude',
                    'type': 'float',
                    'subtype': 'longitude',
                    'description': 'Device longitude',
                    'constraints': {'min_val': -180.0, 'max_val': 180.0, 'null_percentage': 1}
                },
                {
                    'name': 'battery_level',
                    'type': 'float',
                    'subtype': 'percentage',
                    'description': 'Device battery level (%)',
                    'constraints': {'min_val': 0.0, 'max_val': 100.0, 'null_percentage': 2}
                },
                {
                    'name': 'signal_strength',
                    'type': 'integer',
                    'subtype': 'integer',
                    'description': 'Signal strength (dBm)',
                    'constraints': {'min_val': -120, 'max_val': -30, 'null_percentage': 3}
                }
            ]
        }
    
    @staticmethod
    def financial_transactions() -> Dict[str, Any]:
        """Financial transactions template."""
        return {
            'name': 'Financial Transactions',
            'description': 'Banking and financial transaction records',
            'fields': [
                {
                    'name': 'transaction_id',
                    'type': 'integer',
                    'subtype': 'id',
                    'description': 'Unique transaction identifier',
                    'constraints': {'unique': True, 'min_val': 100000000, 'max_val': 999999999}
                },
                {
                    'name': 'account_number',
                    'type': 'text',
                    'subtype': 'bank_account',
                    'description': 'Bank account number',
                    'constraints': {'null_percentage': 1}
                },
                {
                    'name': 'transaction_type',
                    'type': 'categorical',
                    'subtype': 'custom',
                    'description': 'Type of transaction',
                    'constraints': {'categories': ['Deposit', 'Withdrawal', 'Transfer', 'Payment', 'Fee', 'Interest']}
                },
                {
                    'name': 'amount',
                    'type': 'float',
                    'subtype': 'transaction_amount',
                    'description': 'Transaction amount',
                    'constraints': {'min_val': 0.01, 'max_val': 50000.0, 'null_percentage': 1}
                },
                {
                    'name': 'transaction_date',
                    'type': 'date',
                    'subtype': 'transaction_date',
                    'description': 'Transaction date and time',
                    'constraints': {'start_date': '2023-01-01', 'end_date': '2024-12-31'}
                },
                {
                    'name': 'merchant_name',
                    'type': 'text',
                    'subtype': 'company',
                    'description': 'Merchant or recipient name',
                    'constraints': {'null_percentage': 15}
                },
                {
                    'name': 'merchant_category',
                    'type': 'categorical',
                    'subtype': 'custom',
                    'description': 'Merchant category code',
                    'constraints': {'categories': ['Groceries', 'Gas', 'Restaurants', 'Retail', 'Utilities', 'Healthcare', 'Entertainment']}
                },
                {
                    'name': 'balance_after',
                    'type': 'float',
                    'subtype': 'currency',
                    'description': 'Account balance after transaction',
                    'constraints': {'min_val': 0.0, 'max_val': 100000.0, 'null_percentage': 2}
                }
            ]
        }
    
    @staticmethod
    def user_clickstream() -> Dict[str, Any]:
        """User clickstream data template."""
        return {
            'name': 'User Clickstream',
            'description': 'Web user behavior and navigation data',
            'fields': [
                {
                    'name': 'session_id',
                    'type': 'text',
                    'subtype': 'custom',
                    'description': 'User session identifier',
                    'constraints': {'pattern': 'SESS_{id}'}
                },
                {
                    'name': 'user_id',
                    'type': 'integer',
                    'subtype': 'id',
                    'description': 'User identifier',
                    'constraints': {'min_val': 1, 'max_val': 100000, 'null_percentage': 20}
                },
                {
                    'name': 'page_url',
                    'type': 'text',
                    'subtype': 'url',
                    'description': 'Page URL visited',
                    'constraints': {'null_percentage': 1}
                },
                {
                    'name': 'page_title',
                    'type': 'text',
                    'subtype': 'sentence',
                    'description': 'Page title',
                    'constraints': {'null_percentage': 2}
                },
                {
                    'name': 'timestamp',
                    'type': 'date',
                    'subtype': 'datetime',
                    'description': 'Page visit timestamp',
                    'constraints': {'start_date': '2024-01-01', 'end_date': '2024-12-31'}
                },
                {
                    'name': 'duration_seconds',
                    'type': 'integer',
                    'subtype': 'integer',
                    'description': 'Time spent on page (seconds)',
                    'constraints': {'min_val': 1, 'max_val': 3600, 'null_percentage': 1}
                },
                {
                    'name': 'referrer_url',
                    'type': 'text',
                    'subtype': 'url',
                    'description': 'Referring page URL',
                    'constraints': {'null_percentage': 40}
                },
                {
                    'name': 'user_agent',
                    'type': 'text',
                    'subtype': 'user_agent',
                    'description': 'Browser user agent',
                    'constraints': {'null_percentage': 2}
                },
                {
                    'name': 'device_type',
                    'type': 'categorical',
                    'subtype': 'custom',
                    'description': 'Device type',
                    'constraints': {'categories': ['Desktop', 'Mobile', 'Tablet']}
                }
            ]
        }
    
    @staticmethod
    def product_catalog() -> Dict[str, Any]:
        """Product catalog template."""
        return {
            'name': 'Product Catalog',
            'description': 'E-commerce product catalog with pricing and inventory',
            'fields': [
                {
                    'name': 'product_id',
                    'type': 'integer',
                    'subtype': 'id',
                    'description': 'Unique product identifier',
                    'constraints': {'unique': True, 'min_val': 10000, 'max_val': 99999}
                },
                {
                    'name': 'product_name',
                    'type': 'text',
                    'subtype': 'custom',
                    'description': 'Product name',
                    'constraints': {'pattern': '{company} {product_type}'}
                },
                {
                    'name': 'description',
                    'type': 'text',
                    'subtype': 'description',
                    'description': 'Product description',
                    'constraints': {'null_percentage': 2}
                },
                {
                    'name': 'category',
                    'type': 'categorical',
                    'subtype': 'custom',
                    'description': 'Product category',
                    'constraints': {'categories': ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Sports', 'Beauty', 'Toys', 'Automotive']}
                },
                {
                    'name': 'subcategory',
                    'type': 'categorical',
                    'subtype': 'custom',
                    'description': 'Product subcategory',
                    'constraints': {'categories': ['Smartphones', 'Laptops', 'Accessories', 'Men\'s Clothing', 'Women\'s Clothing', 'Fiction', 'Non-fiction']}
                },
                {
                    'name': 'price',
                    'type': 'float',
                    'subtype': 'currency',
                    'description': 'Product price',
                    'constraints': {'min_val': 0.01, 'max_val': 5000.0, 'null_percentage': 1}
                },
                {
                    'name': 'inventory_count',
                    'type': 'integer',
                    'subtype': 'integer',
                    'description': 'Available inventory',
                    'constraints': {'min_val': 0, 'max_val': 1000, 'null_percentage': 1}
                },
                {
                    'name': 'rating',
                    'type': 'float',
                    'subtype': 'rating',
                    'description': 'Average customer rating',
                    'constraints': {'min_val': 1.0, 'max_val': 5.0, 'null_percentage': 5}
                },
                {
                    'name': 'review_count',
                    'type': 'integer',
                    'subtype': 'integer',
                    'description': 'Number of reviews',
                    'constraints': {'min_val': 0, 'max_val': 10000, 'null_percentage': 5}
                },
                {
                    'name': 'created_date',
                    'type': 'date',
                    'subtype': 'date',
                    'description': 'Product creation date',
                    'constraints': {'start_date': '2020-01-01', 'end_date': '2024-12-31'}
                }
            ]
        }
    
    @staticmethod
    def marketing_campaigns() -> Dict[str, Any]:
        """Marketing campaigns template."""
        return {
            'name': 'Marketing Campaigns',
            'description': 'Marketing campaign performance and customer engagement data',
            'fields': [
                {
                    'name': 'campaign_id',
                    'type': 'integer',
                    'subtype': 'id',
                    'description': 'Unique campaign identifier',
                    'constraints': {'unique': True, 'min_val': 1000, 'max_val': 9999}
                },
                {
                    'name': 'campaign_name',
                    'type': 'text',
                    'subtype': 'custom',
                    'description': 'Campaign name',
                    'constraints': {'pattern': '{season} {product_type} Campaign'}
                },
                {
                    'name': 'campaign_type',
                    'type': 'categorical',
                    'subtype': 'custom',
                    'description': 'Type of marketing campaign',
                    'constraints': {'categories': ['Email', 'Social Media', 'Search Ads', 'Display Ads', 'TV', 'Radio', 'Print']}
                },
                {
                    'name': 'start_date',
                    'type': 'date',
                    'subtype': 'date',
                    'description': 'Campaign start date',
                    'constraints': {'start_date': '2023-01-01', 'end_date': '2024-12-31'}
                },
                {
                    'name': 'end_date',
                    'type': 'date',
                    'subtype': 'date',
                    'description': 'Campaign end date',
                    'constraints': {'start_date': '2023-01-01', 'end_date': '2024-12-31'}
                },
                {
                    'name': 'budget',
                    'type': 'float',
                    'subtype': 'currency',
                    'description': 'Campaign budget',
                    'constraints': {'min_val': 1000.0, 'max_val': 1000000.0, 'null_percentage': 1}
                },
                {
                    'name': 'impressions',
                    'type': 'integer',
                    'subtype': 'integer',
                    'description': 'Number of impressions',
                    'constraints': {'min_val': 0, 'max_val': 10000000, 'null_percentage': 1}
                },
                {
                    'name': 'clicks',
                    'type': 'integer',
                    'subtype': 'integer',
                    'description': 'Number of clicks',
                    'constraints': {'min_val': 0, 'max_val': 100000, 'null_percentage': 1}
                },
                {
                    'name': 'conversions',
                    'type': 'integer',
                    'subtype': 'integer',
                    'description': 'Number of conversions',
                    'constraints': {'min_val': 0, 'max_val': 10000, 'null_percentage': 1}
                },
                {
                    'name': 'cost_per_click',
                    'type': 'float',
                    'subtype': 'currency',
                    'description': 'Cost per click',
                    'constraints': {'min_val': 0.01, 'max_val': 10.0, 'null_percentage': 2}
                }
            ]
        }
