---
title: Synthetic Data Generator
emoji: 🎲
colorFrom: blue
colorTo: purple
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: apache-2.0
tags:
  - synthetic-data
  - data-generation
  - privacy
  - machine-learning
  - data-science
  - testing
  - development
---

# 🎲 Synthetic Data Generator

A comprehensive, privacy-preserving synthetic data generation platform built with Gradio. Create realistic datasets for testing, development, and analysis while maintaining data privacy and quality.

![Synthetic Data Generator](https://img.shields.io/badge/Status-Production%20Ready-brightgreen)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Gradio](https://img.shields.io/badge/Gradio-4.44.0-orange)
![License](https://img.shields.io/badge/License-Apache%202.0-green)

## ✨ Features

### 🏗️ **Visual Schema Builder**
- Drag-and-drop field management
- 25+ data types with realistic generators
- Advanced constraints and validation
- Real-time schema preview

### 📋 **Pre-built Templates**
- Customer Database
- E-commerce Transactions
- Employee Records
- Healthcare Records
- Social Media Posts
- IoT Sensor Data
- Financial Transactions
- User Clickstream Data
- Product Catalog
- Marketing Campaigns

### 🔒 **Privacy Protection**
- **Low**: Realistic but identifiable data
- **Medium**: Anonymized with masking/fuzzing
- **High**: Fully anonymous with differential privacy
- PII detection and risk assessment
- K-anonymity validation

### 📊 **Data Quality Controls**
- Configurable missing values (0-20%)
- Outlier injection (0-10%)
- Duplicate creation (0-5%)
- Statistical noise addition
- Data validation and quality reports

### 📤 **Multiple Export Formats**
- CSV, JSON (array/lines), Excel, Parquet
- SQL INSERT statements
- Python Pandas DataFrame code
- Compression support (ZIP)

### 🤖 **AI-Powered Generation**
- GPT-2 integration for realistic text
- Context-aware content generation
- Fallback to Faker for performance
- Custom pattern learning

## 🚀 Quick Start

### 1. **Choose a Template**
Navigate to the **Templates** tab and select from 10 pre-built schemas:
- Customer Database
- E-commerce Transactions
- Employee Records
- Healthcare Records
- And more...

### 2. **Customize Your Schema**
Use the **Schema Builder** to:
- Add/remove fields
- Set constraints and validation rules
- Configure data types and subtypes
- Define relationships between fields

### 3. **Generate Data**
In the **Generate** tab:
- Set number of rows (10 - 100,000)
- Choose privacy level
- Configure data quality parameters
- Set random seed for reproducibility

### 4. **Export Your Data**
Download in your preferred format:
- CSV for spreadsheets
- JSON for APIs
- Excel for business users
- Parquet for big data
- SQL for databases
- Python code for development

## 📋 Supported Data Types

### Text Fields
| Type | Description | Example |
|------|-------------|---------|
| `name` | Person names | "John Smith" |
| `email` | Email addresses | "john@example.com" |
| `address` | Street addresses | "123 Main St" |
| `phone` | Phone numbers | "(555) 123-4567" |
| `company` | Company names | "Acme Corp" |
| `job_title` | Job titles | "Software Engineer" |
| `description` | Product descriptions | "High-quality product..." |
| `url` | Web URLs | "https://example.com" |
| `credit_card` | Credit card numbers | "4532-1234-5678-9012" |
| `ipv4` | IPv4 addresses | "192.168.1.1" |

### Numeric Fields
| Type | Description | Example |
|------|-------------|---------|
| `integer` | Random integers | 42 |
| `float` | Random floats | 3.14159 |
| `percentage` | Percentage values | 85.5 |
| `currency` | Currency amounts | $1,234.56 |
| `age` | Age values | 28 |
| `salary` | Salary amounts | $75,000 |
| `rating` | Rating values | 4.5 |
| `latitude` | Latitude coordinates | 40.7128 |
| `longitude` | Longitude coordinates | -74.0060 |

### Date Fields
| Type | Description | Example |
|------|-------------|---------|
| `date` | Random dates | 2024-01-15 |
| `datetime` | Date and time | 2024-01-15 14:30:00 |
| `signup_date` | Signup dates (weekday bias) | 2024-01-15 |
| `transaction_date` | Transaction dates (business hours) | 2024-01-15 10:30:00 |
| `hire_date` | Hire dates | 2024-01-15 |

### Special Fields
| Type | Description | Example |
|------|-------------|---------|
| `boolean` | True/False values | true |
| `categorical` | Custom categories | "Premium", "Basic" |

## 🔒 Privacy Features

### Privacy Levels

#### Low Privacy
- Realistic, identifiable data
- Suitable for internal testing
- No anonymization applied

#### Medium Privacy
- **Email Masking**: `j***@example.com`
- **Name Masking**: `J*** S***`
- **Phone Masking**: `***-***-1234`
- **Address Masking**: `123 *** St`
- **Date Fuzzing**: ±30 days random shift

#### High Privacy
- **Pseudonymization**: Replace with generic values
- **Differential Privacy**: Statistical noise addition
- **K-anonymity**: Group-based anonymization
- **Generalization**: Reduce data specificity

### PII Detection
- Automatic detection of sensitive data
- Risk level assessment (Low/Medium/High)
- Privacy report generation
- Compliance recommendations

## 📊 Data Quality Features

### Missing Values
- Configurable percentage (0-20%)
- Realistic missing patterns
- Field-specific null rates

### Outliers
- Statistical outlier injection (0-10%)
- Realistic outlier patterns
- Numeric field support

### Duplicates
- Duplicate record creation (0-5%)
- Configurable duplicate patterns
- Relationship preservation

### Validation
- Schema validation
- Data type checking
- Constraint enforcement
- Quality score calculation

## 🛠️ Technical Details

### Architecture
```
synthetic-data-generator/
├── app.py                 # Main Gradio application
├── requirements.txt       # Python dependencies
├── generators/           # Data generation modules
│   ├── base_generator.py
│   ├── text_generator.py
│   ├── numeric_generator.py
│   ├── date_generator.py
│   └── ai_generator.py
├── privacy/              # Privacy protection modules
│   ├── anonymizer.py
│   └── differential_privacy.py
├── templates/            # Pre-built schemas
│   └── schema_templates.py
└── utils/               # Utility functions
    ├── validators.py
    └── exporters.py
```

### Dependencies
- **Gradio 4.44.0**: Web interface framework
- **Pandas 2.1.4**: Data manipulation
- **Faker 20.1.0**: Fake data generation
- **NumPy 1.24.3**: Numerical operations
- **Transformers 4.36.2**: AI text generation
- **PyArrow 14.0.1**: Parquet export
- **OpenPyXL 3.1.2**: Excel export

### Performance
- **Generation Speed**: ~1,000 records/second
- **Memory Usage**: Optimized for large datasets
- **Export Speed**: Streaming for large files
- **Concurrent Users**: Supports multiple sessions

## 📈 Use Cases

### 🧪 **Testing & Development**
- Unit test data
- Integration testing
- Performance testing
- Load testing scenarios

### 📊 **Data Science**
- Model training data
- Algorithm testing
- Statistical analysis
- Research datasets

### 🏢 **Business Applications**
- CRM testing
- ERP system testing
- Analytics platform testing
- Dashboard development

### 🔒 **Privacy Compliance**
- GDPR compliance testing
- HIPAA compliance testing
- Data anonymization
- Privacy impact assessments

## 🎯 Examples

### Customer Database
```json
{
  "customer_id": 12345,
  "first_name": "John",
  "last_name": "Smith",
  "email": "john.smith@email.com",
  "phone": "(555) 123-4567",
  "address": "123 Main St",
  "city": "New York",
  "country": "United States",
  "age": 28,
  "signup_date": "2024-01-15",
  "lifetime_value": 1250.50
}
```

### E-commerce Transaction
```json
{
  "transaction_id": 9876543,
  "customer_id": 12345,
  "product_name": "Wireless Headphones",
  "category": "Electronics",
  "quantity": 1,
  "unit_price": 99.99,
  "total_amount": 99.99,
  "transaction_date": "2024-01-15 14:30:00",
  "payment_method": "Credit Card"
}
```

## 🔧 Configuration

### Environment Variables
```bash
# Optional: Set default seed
DEFAULT_SEED=42

# Optional: Set privacy level
DEFAULT_PRIVACY_LEVEL=medium

# Optional: Set max rows
MAX_ROWS=100000
```

### Custom Templates
Add your own templates by extending `SchemaTemplates`:

```python
@staticmethod
def custom_template() -> Dict[str, Any]:
    return {
        'name': 'Custom Template',
        'description': 'My custom data schema',
        'fields': [
            {
                'name': 'custom_field',
                'type': 'text',
                'subtype': 'name',
                'description': 'Custom field description',
                'constraints': {'null_percentage': 5}
            }
        ]
    }
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guidelines](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/your-username/synthetic-data-generator.git
cd synthetic-data-generator
pip install -r requirements.txt
python app.py
```

### Running Tests
```bash
python -m pytest tests/
```

## 📄 License

This project is licensed under the Apache License 2.0 - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- [Faker](https://faker.readthedocs.io/) for realistic data generation
- [Gradio](https://gradio.app/) for the web interface
- [Hugging Face](https://huggingface.co/) for AI models
- [Pandas](https://pandas.pydata.org/) for data manipulation

## 📞 Support

- 📧 Email: support@syntheticdata.com
- 💬 Discord: [Join our community](https://discord.gg/syntheticdata)
- 📖 Documentation: [docs.syntheticdata.com](https://docs.syntheticdata.com)
- 🐛 Issues: [GitHub Issues](https://github.com/your-username/synthetic-data-generator/issues)

---

**Made with ❤️ for the data community**

*Generate realistic data. Protect privacy. Build better applications.*
