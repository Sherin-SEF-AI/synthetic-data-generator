"""
Data Validation Utilities

Provides validation functions for schemas and generated data.
"""

import re
from typing import Any, Dict, List, Optional, Union
from datetime import datetime


class SchemaValidator:
    """Validates schema definitions."""
    
    @staticmethod
    def validate_schema(schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate a complete schema definition."""
        errors = []
        warnings = []
        
        # Check required fields
        if 'name' not in schema:
            errors.append("Schema must have a 'name' field")
        if 'fields' not in schema:
            errors.append("Schema must have a 'fields' field")
        
        if 'fields' in schema:
            if not isinstance(schema['fields'], list):
                errors.append("'fields' must be a list")
            else:
                # Validate each field
                for i, field in enumerate(schema['fields']):
                    field_errors = SchemaValidator.validate_field(field, i)
                    errors.extend(field_errors)
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings
        }
    
    @staticmethod
    def validate_field(field: Dict[str, Any], index: int) -> List[str]:
        """Validate a single field definition."""
        errors = []
        
        # Required field properties
        required_props = ['name', 'type']
        for prop in required_props:
            if prop not in field:
                errors.append(f"Field {index}: Missing required property '{prop}'")
        
        if 'name' in field:
            if not isinstance(field['name'], str) or not field['name'].strip():
                errors.append(f"Field {index}: 'name' must be a non-empty string")
            elif not re.match(r'^[a-zA-Z_][a-zA-Z0-9_]*$', field['name']):
                errors.append(f"Field {index}: 'name' must be a valid identifier")
        
        if 'type' in field:
            valid_types = ['text', 'integer', 'float', 'date', 'boolean', 'categorical']
            if field['type'] not in valid_types:
                errors.append(f"Field {index}: 'type' must be one of {valid_types}")
        
        # Validate constraints
        if 'constraints' in field:
            constraint_errors = SchemaValidator.validate_constraints(field['constraints'], field.get('type'), index)
            errors.extend(constraint_errors)
        
        return errors
    
    @staticmethod
    def validate_constraints(constraints: Dict[str, Any], field_type: str, field_index: int) -> List[str]:
        """Validate field constraints."""
        errors = []
        
        # Numeric constraints
        if field_type in ['integer', 'float']:
            if 'min_val' in constraints and 'max_val' in constraints:
                if constraints['min_val'] > constraints['max_val']:
                    errors.append(f"Field {field_index}: min_val cannot be greater than max_val")
        
        # Date constraints
        if field_type == 'date':
            if 'start_date' in constraints:
                try:
                    datetime.strptime(constraints['start_date'], '%Y-%m-%d')
                except ValueError:
                    errors.append(f"Field {field_index}: start_date must be in YYYY-MM-DD format")
            
            if 'end_date' in constraints:
                try:
                    datetime.strptime(constraints['end_date'], '%Y-%m-%d')
                except ValueError:
                    errors.append(f"Field {field_index}: end_date must be in YYYY-MM-DD format")
            
            if 'start_date' in constraints and 'end_date' in constraints:
                try:
                    start = datetime.strptime(constraints['start_date'], '%Y-%m-%d')
                    end = datetime.strptime(constraints['end_date'], '%Y-%m-%d')
                    if start > end:
                        errors.append(f"Field {field_index}: start_date cannot be after end_date")
                except ValueError:
                    pass  # Already handled above
        
        # Categorical constraints
        if field_type == 'categorical':
            if 'categories' in constraints:
                if not isinstance(constraints['categories'], list) or len(constraints['categories']) == 0:
                    errors.append(f"Field {field_index}: categories must be a non-empty list")
        
        # Null percentage
        if 'null_percentage' in constraints:
            null_pct = constraints['null_percentage']
            if not isinstance(null_pct, (int, float)) or null_pct < 0 or null_pct > 100:
                errors.append(f"Field {field_index}: null_percentage must be between 0 and 100")
        
        return errors


class DataValidator:
    """Validates generated data against schema."""
    
    @staticmethod
    def validate_data(data: List[Dict[str, Any]], schema: Dict[str, Any]) -> Dict[str, Any]:
        """Validate generated data against schema."""
        errors = []
        warnings = []
        
        if not data:
            warnings.append("No data generated")
            return {'valid': True, 'errors': errors, 'warnings': warnings}
        
        # Check if all required fields are present
        schema_fields = {field['name'] for field in schema.get('fields', [])}
        data_fields = set(data[0].keys()) if data else set()
        
        missing_fields = schema_fields - data_fields
        extra_fields = data_fields - schema_fields
        
        if missing_fields:
            errors.append(f"Missing fields in data: {missing_fields}")
        if extra_fields:
            warnings.append(f"Extra fields in data: {extra_fields}")
        
        # Validate each record
        for i, record in enumerate(data):
            record_errors = DataValidator.validate_record(record, schema, i)
            errors.extend(record_errors)
        
        return {
            'valid': len(errors) == 0,
            'errors': errors,
            'warnings': warnings,
            'record_count': len(data)
        }
    
    @staticmethod
    def validate_record(record: Dict[str, Any], schema: Dict[str, Any], record_index: int) -> List[str]:
        """Validate a single record against schema."""
        errors = []
        
        for field in schema.get('fields', []):
            field_name = field['name']
            field_type = field['type']
            constraints = field.get('constraints', {})
            
            if field_name not in record:
                errors.append(f"Record {record_index}: Missing field '{field_name}'")
                continue
            
            value = record[field_name]
            
            # Check null constraints
            if value is None:
                if constraints.get('null_percentage', 0) == 0:
                    errors.append(f"Record {record_index}: Field '{field_name}' cannot be null")
                continue
            
            # Type validation
            type_errors = DataValidator.validate_value_type(value, field_type, field_name, record_index)
            errors.extend(type_errors)
            
            # Constraint validation
            constraint_errors = DataValidator.validate_value_constraints(
                value, constraints, field_name, record_index
            )
            errors.extend(constraint_errors)
        
        return errors
    
    @staticmethod
    def validate_value_type(value: Any, expected_type: str, field_name: str, record_index: int) -> List[str]:
        """Validate that a value matches the expected type."""
        errors = []
        
        if expected_type == 'integer':
            if not isinstance(value, int):
                errors.append(f"Record {record_index}: Field '{field_name}' must be an integer, got {type(value).__name__}")
        elif expected_type == 'float':
            if not isinstance(value, (int, float)):
                errors.append(f"Record {record_index}: Field '{field_name}' must be a number, got {type(value).__name__}")
        elif expected_type == 'text':
            if not isinstance(value, str):
                errors.append(f"Record {record_index}: Field '{field_name}' must be a string, got {type(value).__name__}")
        elif expected_type == 'date':
            if not isinstance(value, (str, datetime)):
                errors.append(f"Record {record_index}: Field '{field_name}' must be a date, got {type(value).__name__}")
        elif expected_type == 'boolean':
            if not isinstance(value, bool):
                errors.append(f"Record {record_index}: Field '{field_name}' must be a boolean, got {type(value).__name__}")
        
        return errors
    
    @staticmethod
    def validate_value_constraints(value: Any, constraints: Dict[str, Any], 
                                 field_name: str, record_index: int) -> List[str]:
        """Validate that a value meets the specified constraints."""
        errors = []
        
        # Numeric range constraints
        if isinstance(value, (int, float)):
            if 'min_val' in constraints and value < constraints['min_val']:
                errors.append(f"Record {record_index}: Field '{field_name}' value {value} is below minimum {constraints['min_val']}")
            if 'max_val' in constraints and value > constraints['max_val']:
                errors.append(f"Record {record_index}: Field '{field_name}' value {value} is above maximum {constraints['max_val']}")
        
        # String length constraints
        if isinstance(value, str):
            if 'min_length' in constraints and len(value) < constraints['min_length']:
                errors.append(f"Record {record_index}: Field '{field_name}' length {len(value)} is below minimum {constraints['min_length']}")
            if 'max_length' in constraints and len(value) > constraints['max_length']:
                errors.append(f"Record {record_index}: Field '{field_name}' length {len(value)} is above maximum {constraints['max_length']}")
        
        # Categorical constraints
        if 'categories' in constraints:
            if value not in constraints['categories']:
                errors.append(f"Record {record_index}: Field '{field_name}' value '{value}' is not in allowed categories {constraints['categories']}")
        
        # Regex pattern constraints
        if 'pattern' in constraints and isinstance(value, str):
            if not re.match(constraints['pattern'], value):
                errors.append(f"Record {record_index}: Field '{field_name}' value '{value}' does not match pattern '{constraints['pattern']}'")
        
        return errors
    
    @staticmethod
    def generate_quality_report(data: List[Dict[str, Any]], schema: Dict[str, Any]) -> Dict[str, Any]:
        """Generate a data quality report."""
        if not data:
            return {'error': 'No data to analyze'}
        
        report = {
            'total_records': len(data),
            'total_fields': len(schema.get('fields', [])),
            'field_analysis': {},
            'overall_quality_score': 0.0
        }
        
        quality_scores = []
        
        for field in schema.get('fields', []):
            field_name = field['name']
            field_analysis = DataValidator.analyze_field(data, field_name)
            report['field_analysis'][field_name] = field_analysis
            quality_scores.append(field_analysis['quality_score'])
        
        if quality_scores:
            report['overall_quality_score'] = sum(quality_scores) / len(quality_scores)
        
        return report
    
    @staticmethod
    def analyze_field(data: List[Dict[str, Any]], field_name: str) -> Dict[str, Any]:
        """Analyze a specific field in the dataset."""
        values = [record.get(field_name) for record in data]
        
        # Basic statistics
        total_count = len(values)
        null_count = sum(1 for v in values if v is None)
        non_null_count = total_count - null_count
        null_percentage = (null_count / total_count * 100) if total_count > 0 else 0
        
        # Unique values
        unique_values = len(set(v for v in values if v is not None))
        uniqueness_ratio = (unique_values / non_null_count) if non_null_count > 0 else 0
        
        # Data type consistency
        non_null_values = [v for v in values if v is not None]
        if non_null_values:
            primary_type = type(non_null_values[0]).__name__
            type_consistency = sum(1 for v in non_null_values if type(v).__name__ == primary_type) / len(non_null_values)
        else:
            primary_type = 'None'
            type_consistency = 1.0
        
        # Calculate quality score (0-100)
        quality_score = (
            (1 - null_percentage / 100) * 40 +  # 40% weight for completeness
            uniqueness_ratio * 30 +              # 30% weight for uniqueness
            type_consistency * 30                # 30% weight for type consistency
        ) * 100
        
        return {
            'total_count': total_count,
            'null_count': null_count,
            'non_null_count': non_null_count,
            'null_percentage': round(null_percentage, 2),
            'unique_values': unique_values,
            'uniqueness_ratio': round(uniqueness_ratio, 3),
            'primary_type': primary_type,
            'type_consistency': round(type_consistency, 3),
            'quality_score': round(quality_score, 2)
        }
