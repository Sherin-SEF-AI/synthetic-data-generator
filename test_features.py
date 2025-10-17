"""
Comprehensive feature test for the Synthetic Data Generator
"""

import sys
import os
import time
import requests
import json
from typing import Dict, List, Any

# Add current directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_generators():
    """Test all data generators"""
    print("🧪 Testing Data Generators...")
    
    try:
        from generators import TextGenerator, NumericGenerator, DateGenerator, AIGenerator
        
        # Test text generator
        text_gen = TextGenerator(seed=42)
        names = text_gen.generate(5, "name")
        emails = text_gen.generate(5, "email")
        print(f"✅ Text Generator: Generated {len(names)} names and {len(emails)} emails")
        
        # Test numeric generator
        num_gen = NumericGenerator(seed=42)
        ages = num_gen.generate(5, "age")
        salaries = num_gen.generate(5, "salary")
        print(f"✅ Numeric Generator: Generated {len(ages)} ages and {len(salaries)} salaries")
        
        # Test date generator
        date_gen = DateGenerator(seed=42)
        dates = date_gen.generate(5, "date")
        print(f"✅ Date Generator: Generated {len(dates)} dates")
        
        # Test AI generator (may fail if model not available)
        try:
            ai_gen = AIGenerator(seed=42)
            descriptions = ai_gen.generate(3, "description")
            print(f"✅ AI Generator: Generated {len(descriptions)} descriptions")
        except Exception as e:
            print(f"⚠️  AI Generator: Not available ({str(e)[:50]}...)")
        
        return True
    except Exception as e:
        print(f"❌ Generator test failed: {e}")
        return False

def test_templates():
    """Test schema templates"""
    print("\n🧪 Testing Schema Templates...")
    
    try:
        from templates import SchemaTemplates
        
        templates = SchemaTemplates.get_all_templates()
        print(f"✅ Found {len(templates)} templates")
        
        # Test a few templates
        for template_name in ["customer_database", "ecommerce_transactions", "employee_records"]:
            if template_name in templates:
                template = templates[template_name]
                print(f"✅ Template '{template_name}': {len(template['fields'])} fields")
            else:
                print(f"❌ Template '{template_name}' not found")
                return False
        
        return True
    except Exception as e:
        print(f"❌ Template test failed: {e}")
        return False

def test_privacy():
    """Test privacy features"""
    print("\n🧪 Testing Privacy Features...")
    
    try:
        from privacy import DataAnonymizer, DifferentialPrivacy
        
        # Test anonymizer
        anonymizer = DataAnonymizer(seed=42)
        emails = ["john@example.com", "jane@example.com", "bob@example.com"]
        
        # Test medium anonymization
        anonymized = anonymizer.anonymize_data(emails, "email", "medium")
        print(f"✅ Anonymizer: {len(anonymized)} emails anonymized")
        
        # Test differential privacy
        dp = DifferentialPrivacy(epsilon=1.0, seed=42)
        numbers = [100, 200, 300, 400, 500]
        noisy_numbers = dp.add_laplace_noise(numbers)
        print(f"✅ Differential Privacy: Added noise to {len(noisy_numbers)} numbers")
        
        return True
    except Exception as e:
        print(f"❌ Privacy test failed: {e}")
        return False

def test_exporters():
    """Test export functionality"""
    print("\n🧪 Testing Export Functions...")
    
    try:
        from utils import DataExporter
        
        # Sample data
        sample_data = [
            {"name": "John", "age": 30, "email": "john@example.com"},
            {"name": "Jane", "age": 25, "email": "jane@example.com"}
        ]
        
        exporter = DataExporter()
        
        # Test CSV export
        csv_content = exporter.export_to_csv(sample_data)
        print(f"✅ CSV Export: {len(csv_content)} characters")
        
        # Test JSON export
        json_content = exporter.export_to_json(sample_data)
        print(f"✅ JSON Export: {len(json_content)} characters")
        
        # Test SQL export
        sql_content = exporter.export_to_sql(sample_data)
        print(f"✅ SQL Export: {len(sql_content)} characters")
        
        return True
    except Exception as e:
        print(f"❌ Export test failed: {e}")
        return False

def test_validators():
    """Test validation functions"""
    print("\n🧪 Testing Validators...")
    
    try:
        from utils import SchemaValidator, DataValidator
        
        # Test schema validation
        validator = SchemaValidator()
        sample_schema = {
            "name": "Test Schema",
            "fields": [
                {
                    "name": "test_field",
                    "type": "text",
                    "subtype": "name",
                    "description": "Test field"
                }
            ]
        }
        
        result = validator.validate_schema(sample_schema)
        print(f"✅ Schema Validator: Validation result = {result['valid']}")
        
        # Test data validation
        data_validator = DataValidator()
        sample_data = [{"test_field": "John Doe"}]
        validation_result = data_validator.validate_data(sample_data, sample_schema)
        print(f"✅ Data Validator: Validation result = {validation_result['valid']}")
        
        return True
    except Exception as e:
        print(f"❌ Validator test failed: {e}")
        return False

def test_web_interface():
    """Test if the web interface is accessible"""
    print("\n🧪 Testing Web Interface...")
    
    try:
        # Test if the app is running
        response = requests.get("http://localhost:7860", timeout=10)
        if response.status_code == 200:
            print("✅ Web Interface: Application is accessible")
            return True
        else:
            print(f"❌ Web Interface: HTTP {response.status_code}")
            return False
    except requests.exceptions.RequestException as e:
        print(f"❌ Web Interface: Not accessible ({str(e)[:50]}...)")
        return False

def test_data_generation():
    """Test end-to-end data generation"""
    print("\n🧪 Testing End-to-End Data Generation...")
    
    try:
        from generators import TextGenerator, NumericGenerator, DateGenerator
        from templates import SchemaTemplates
        
        # Get customer database template
        templates = SchemaTemplates.get_all_templates()
        template = templates["customer_database"]
        
        # Initialize generators
        text_gen = TextGenerator(seed=42)
        num_gen = NumericGenerator(seed=42)
        date_gen = DateGenerator(seed=42)
        
        # Generate 10 records
        data = []
        for i in range(10):
            record = {}
            for field in template["fields"][:5]:  # Test first 5 fields
                field_name = field["name"]
                field_type = field["type"]
                field_subtype = field.get("subtype", "custom")
                constraints = field.get("constraints", {})
                
                if field_type == "text":
                    value = text_gen.generate(1, field_subtype, **constraints)[0]
                elif field_type == "integer":
                    value = num_gen.generate(1, field_subtype, **constraints)[0]
                elif field_type == "float":
                    value = num_gen.generate(1, field_subtype, **constraints)[0]
                elif field_type == "date":
                    value = date_gen.generate(1, field_subtype, **constraints)[0]
                else:
                    value = f"Generated_{i}"
                
                record[field_name] = value
            
            data.append(record)
        
        print(f"✅ End-to-End Generation: Created {len(data)} records with {len(data[0])} fields each")
        
        # Test export
        from utils import DataExporter
        exporter = DataExporter()
        csv_content = exporter.export_to_csv(data)
        print(f"✅ Export Integration: Generated {len(csv_content)} character CSV")
        
        return True
    except Exception as e:
        print(f"❌ End-to-End test failed: {e}")
        return False

def main():
    """Run all feature tests"""
    print("🎲 Synthetic Data Generator - Feature Test Suite")
    print("=" * 50)
    
    tests = [
        ("Data Generators", test_generators),
        ("Schema Templates", test_templates),
        ("Privacy Features", test_privacy),
        ("Export Functions", test_exporters),
        ("Validators", test_validators),
        ("Web Interface", test_web_interface),
        ("End-to-End Generation", test_data_generation)
    ]
    
    passed = 0
    total = len(tests)
    
    for test_name, test_func in tests:
        try:
            if test_func():
                passed += 1
        except Exception as e:
            print(f"❌ {test_name}: Unexpected error - {e}")
    
    print("\n" + "=" * 50)
    print(f"📊 Test Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("🎉 All features are working correctly!")
        print("✅ The Synthetic Data Generator is fully functional!")
    else:
        print(f"⚠️  {total - passed} tests failed. Check the errors above.")
    
    return passed == total

if __name__ == "__main__":
    main()
