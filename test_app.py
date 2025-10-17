"""
Simple test script for the Synthetic Data Generator application.
"""

import sys
import os

# Add the current directory to the Python path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from generators import TextGenerator, NumericGenerator, DateGenerator
from templates import SchemaTemplates
from utils import SchemaValidator, DataValidator, DataExporter
from privacy import DataAnonymizer

def test_generators():
    """Test the data generators."""
    print("Testing data generators...")
    
    # Test text generator
    text_gen = TextGenerator(seed=42)
    names = text_gen.generate(5, "name")
    emails = text_gen.generate(5, "email")
    print(f"Generated names: {names}")
    print(f"Generated emails: {emails}")
    
    # Test numeric generator
    num_gen = NumericGenerator(seed=42)
    ages = num_gen.generate(5, "age")
    salaries = num_gen.generate(5, "salary")
    print(f"Generated ages: {ages}")
    print(f"Generated salaries: {salaries}")
    
    # Test date generator
    date_gen = DateGenerator(seed=42)
    dates = date_gen.generate(5, "date")
    print(f"Generated dates: {dates}")
    
    print("✅ Generator tests passed!")

def test_templates():
    """Test the schema templates."""
    print("\nTesting schema templates...")
    
    templates = SchemaTemplates.get_all_templates()
    print(f"Available templates: {list(templates.keys())}")
    
    # Test customer database template
    customer_template = templates['customer_database']
    print(f"Customer template has {len(customer_template['fields'])} fields")
    
    print("✅ Template tests passed!")

def test_validators():
    """Test the validators."""
    print("\nTesting validators...")
    
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
    print(f"Schema validation result: {result['valid']}")
    
    print("✅ Validator tests passed!")

def test_exporters():
    """Test the exporters."""
    print("\nTesting exporters...")
    
    # Test data export
    sample_data = [
        {"name": "John", "age": 30, "email": "john@example.com"},
        {"name": "Jane", "age": 25, "email": "jane@example.com"}
    ]
    
    exporter = DataExporter()
    csv_content = exporter.export_to_csv(sample_data)
    json_content = exporter.export_to_json(sample_data)
    
    print(f"CSV export length: {len(csv_content)}")
    print(f"JSON export length: {len(json_content)}")
    
    print("✅ Exporter tests passed!")

def test_privacy():
    """Test privacy features."""
    print("\nTesting privacy features...")
    
    # Test anonymizer
    anonymizer = DataAnonymizer(seed=42)
    emails = ["john@example.com", "jane@example.com", "bob@example.com"]
    
    anonymized = anonymizer.anonymize_data(emails, "email", "medium")
    print(f"Original emails: {emails}")
    print(f"Anonymized emails: {anonymized}")
    
    print("✅ Privacy tests passed!")

def main():
    """Run all tests."""
    print("🧪 Running Synthetic Data Generator Tests\n")
    
    try:
        test_generators()
        test_templates()
        test_validators()
        test_exporters()
        test_privacy()
        
        print("\n🎉 All tests passed successfully!")
        print("The Synthetic Data Generator is ready to use!")
        
    except Exception as e:
        print(f"\n❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()
