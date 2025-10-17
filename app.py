"""
Synthetic Data Generator - Main Application

A comprehensive Gradio application for generating realistic synthetic data
with privacy-preserving features and multiple export options.
"""

import gradio as gr
import pandas as pd
import json
import random
import numpy as np
from typing import Dict, List, Any, Optional, Tuple
import io
import base64
from datetime import datetime

# Import our custom modules
from generators import TextGenerator, NumericGenerator, DateGenerator, AIGenerator
from privacy import DataAnonymizer, DifferentialPrivacy
from templates import SchemaTemplates
from utils import SchemaValidator, DataValidator, DataExporter


class SyntheticDataApp:
    """Main application class for the Synthetic Data Generator."""
    
    def __init__(self):
        """Initialize the application."""
        self.current_schema = None
        self.generated_data = None
        self.templates = SchemaTemplates.get_all_templates()
        
        # Initialize generators
        self.text_generator = TextGenerator()
        self.numeric_generator = NumericGenerator()
        self.date_generator = DateGenerator()
        self.ai_generator = AIGenerator()
        
        # Initialize privacy tools
        self.anonymizer = DataAnonymizer()
        self.dp = DifferentialPrivacy(epsilon=1.0)
    
    def create_schema_builder_tab(self) -> gr.Blocks:
        """Create the schema builder interface."""
        with gr.Blocks(title="Schema Builder") as tab:
            gr.Markdown("# 🏗️ Schema Builder")
            gr.Markdown("Build your custom data schema by adding fields with specific types and constraints.")
            
            with gr.Row():
                with gr.Column(scale=2):
                    # Schema metadata
                    schema_name = gr.Textbox(
                        label="Schema Name",
                        placeholder="Enter a name for your schema",
                        value="My Custom Schema"
                    )
                    schema_description = gr.Textbox(
                        label="Schema Description",
                        placeholder="Describe what this schema represents",
                        value="Custom synthetic data schema"
                    )
                    
                    # Field list
                    gr.Markdown("### Fields")
                    fields_display = gr.HTML(value="<p>No fields added yet. Click 'Add Field' to get started.</p>")
                    
                    with gr.Row():
                        add_field_btn = gr.Button("➕ Add Field", variant="secondary")
                        clear_schema_btn = gr.Button("🗑️ Clear Schema", variant="stop")
                
                with gr.Column(scale=1):
                    # Field editor
                    gr.Markdown("### Field Editor")
                    
                    field_name = gr.Textbox(
                        label="Field Name",
                        placeholder="e.g., customer_id",
                        info="Must be a valid identifier"
                    )
                    
                    field_type = gr.Dropdown(
                        choices=["text", "integer", "float", "date", "boolean", "categorical"],
                        label="Field Type",
                        value="text"
                    )
                    
                    field_subtype = gr.Dropdown(
                        choices=["name"],
                        label="Field Subtype",
                        value="name"
                    )
                    
                    field_description = gr.Textbox(
                        label="Description",
                        placeholder="Describe this field"
                    )
                    
                    # Constraints
                    gr.Markdown("#### Constraints")
                    
                    with gr.Row():
                        min_val = gr.Number(label="Min Value", precision=2)
                        max_val = gr.Number(label="Max Value", precision=2)
                    
                    with gr.Row():
                        null_percentage = gr.Slider(0, 100, 0, step=1, label="Null %")
                        unique_checkbox = gr.Checkbox(label="Unique Values")
                    
                    categories = gr.Textbox(
                        label="Categories (comma-separated)",
                        placeholder="Option1, Option2, Option3",
                        visible=False
                    )
                    
                    pattern = gr.Textbox(
                        label="Pattern/Format",
                        placeholder="e.g., {name}@{company}.com",
                        visible=False
                    )
                    
                    with gr.Row():
                        save_field_btn = gr.Button("💾 Save Field", variant="primary")
                        cancel_field_btn = gr.Button("❌ Cancel", variant="secondary")
            
            # Schema actions
            with gr.Row():
                validate_schema_btn = gr.Button("✅ Validate Schema", variant="secondary")
                save_schema_btn = gr.Button("💾 Save Schema", variant="primary")
                load_schema_btn = gr.Button("📁 Load Schema", variant="secondary")
            
            # Schema JSON display
            schema_json = gr.JSON(label="Schema JSON", visible=False)
            
            # Event handlers
            field_type.change(
                self.update_field_subtype_options,
                inputs=[field_type],
                outputs=[field_subtype, categories, pattern]
            )
            
            add_field_btn.click(
                self.add_field_to_schema,
                inputs=[field_name, field_type, field_subtype, field_description, 
                       min_val, max_val, null_percentage, unique_checkbox, categories, pattern],
                outputs=[fields_display, schema_json]
            )
            
            save_field_btn.click(
                self.add_field_to_schema,
                inputs=[field_name, field_type, field_subtype, field_description,
                       min_val, max_val, null_percentage, unique_checkbox, categories, pattern],
                outputs=[fields_display, schema_json]
            )
            
            validate_schema_btn.click(
                self.validate_current_schema,
                inputs=[schema_json],
                outputs=[gr.Textbox(label="Validation Results", visible=True)]
            )
        
        return tab
    
    def create_templates_tab(self) -> gr.Blocks:
        """Create the templates selection interface."""
        with gr.Blocks(title="Templates") as tab:
            gr.Markdown("# 📋 Pre-built Templates")
            gr.Markdown("Choose from our collection of pre-built schemas for common use cases.")
            
            with gr.Row():
                with gr.Column(scale=1):
                    # Template selection
                    template_dropdown = gr.Dropdown(
                        choices=list(self.templates.keys()),
                        label="Select Template",
                        value=list(self.templates.keys())[0] if self.templates else None
                    )
                    
                    load_template_btn = gr.Button("📥 Load Template", variant="primary")
                    
                    # Template preview
                    template_preview = gr.JSON(label="Template Preview")
                
                with gr.Column(scale=2):
                    # Template details
                    template_name = gr.Textbox(label="Template Name", interactive=False)
                    template_description = gr.Textbox(label="Description", interactive=False)
                    
                    # Fields table
                    fields_table = gr.Dataframe(
                        headers=["Name", "Type", "Subtype", "Description"],
                        datatype=["str", "str", "str", "str"],
                        label="Template Fields"
                    )
            
            # Event handlers
            template_dropdown.change(
                self.update_template_preview,
                inputs=[template_dropdown],
                outputs=[template_preview, template_name, template_description, fields_table]
            )
            
            load_template_btn.click(
                self.load_template,
                inputs=[template_dropdown],
                outputs=[gr.Textbox(label="Load Status", visible=True)]
            )
        
        return tab
    
    def create_generate_tab(self) -> gr.Blocks:
        """Create the data generation interface."""
        with gr.Blocks(title="Generate Data") as tab:
            gr.Markdown("# 🎲 Generate Synthetic Data")
            gr.Markdown("Configure generation parameters and create your synthetic dataset.")
            
            with gr.Row():
                with gr.Column(scale=1):
                    # Generation parameters
                    gr.Markdown("### Generation Parameters")
                    
                    num_rows = gr.Slider(
                        10, 100000, 1000, step=10,
                        label="Number of Rows",
                        info="Maximum 100,000 rows for performance"
                    )
                    
                    seed = gr.Number(
                        label="Random Seed",
                        value=42,
                        info="Set for reproducible results"
                    )
                    
                    privacy_level = gr.Radio(
                        choices=["low", "medium", "high"],
                        value="medium",
                        label="Privacy Level",
                        info="Higher levels provide more privacy but less realistic data"
                    )
                    
                    # Data quality controls
                    gr.Markdown("### Data Quality Controls")
                    
                    missing_percentage = gr.Slider(
                        0, 20, 0, step=1,
                        label="Missing Values %",
                        info="Percentage of records with missing values"
                    )
                    
                    outlier_percentage = gr.Slider(
                        0, 10, 0, step=1,
                        label="Outliers %",
                        info="Percentage of numeric values that are outliers"
                    )
                    
                    duplicate_percentage = gr.Slider(
                        0, 5, 0, step=1,
                        label="Duplicates %",
                        info="Percentage of duplicate records"
                    )
                    
                    generate_btn = gr.Button("🚀 Generate Data", variant="primary", size="lg")
                
                with gr.Column(scale=2):
                    # Generation status and preview
                    generation_status = gr.Textbox(
                        label="Generation Status",
                        value="Ready to generate data",
                        interactive=False
                    )
                    
                    progress_bar = gr.Progress()
                    
                    # Data preview
                    data_preview = gr.Dataframe(
                        label="Data Preview (First 50 rows)"
                    )
                    
                    # Statistics
                    stats_display = gr.HTML(label="Dataset Statistics")
            
            # Event handlers
            generate_btn.click(
                self.generate_data,
                inputs=[num_rows, seed, privacy_level, missing_percentage, 
                       outlier_percentage, duplicate_percentage],
                outputs=[generation_status, data_preview, stats_display]
            )
        
        return tab
    
    def create_export_tab(self) -> gr.Blocks:
        """Create the export interface."""
        with gr.Blocks(title="Export Data") as tab:
            gr.Markdown("# 📤 Export Data")
            gr.Markdown("Export your generated data in various formats.")
            
            with gr.Row():
                with gr.Column(scale=1):
                    # Export options
                    gr.Markdown("### Export Options")
                    
                    export_format = gr.Dropdown(
                        choices=["csv", "json", "excel", "parquet", "sql", "pandas"],
                        value="csv",
                        label="Export Format"
                    )
                    
                    json_format = gr.Radio(
                        choices=["array", "lines"],
                        value="array",
                        label="JSON Format",
                        visible=False
                    )
                    
                    table_name = gr.Textbox(
                        label="Table Name (for SQL)",
                        value="synthetic_data",
                        visible=False
                    )
                    
                    variable_name = gr.Textbox(
                        label="Variable Name (for Pandas)",
                        value="df",
                        visible=False
                    )
                    
                    compress_file = gr.Checkbox(
                        label="Compress (ZIP)",
                        value=False
                    )
                    
                    export_btn = gr.Button("📥 Export Data", variant="primary")
                
                with gr.Column(scale=2):
                    # Export preview and download
                    export_preview = gr.Textbox(
                        label="Export Preview",
                        lines=10
                    )
                    
                    download_file = gr.File(
                        label="Download File",
                        visible=False
                    )
                    
                    export_info = gr.HTML(label="Export Information")
            
            # Event handlers
            export_format.change(
                self.update_export_options,
                inputs=[export_format],
                outputs=[json_format, table_name, variable_name]
            )
            
            export_btn.click(
                self.export_data,
                inputs=[export_format, json_format, table_name, variable_name, compress_file],
                outputs=[export_preview, download_file, export_info]
            )
        
        return tab
    
    def create_documentation_tab(self) -> gr.Blocks:
        """Create the documentation interface."""
        with gr.Blocks(title="Documentation") as tab:
            gr.Markdown("# 📚 Documentation")
            
            with gr.Tabs():
                with gr.Tab("Getting Started"):
                    gr.Markdown("""
                    ## Welcome to Synthetic Data Generator
                    
                    This application helps you create realistic synthetic data for testing, development, and analysis purposes while maintaining privacy.
                    
                    ### Quick Start
                    1. **Choose a Template**: Go to the Templates tab and select a pre-built schema
                    2. **Customize**: Use the Schema Builder to modify fields or create your own
                    3. **Generate**: Set parameters and generate your data
                    4. **Export**: Download in your preferred format
                    
                    ### Key Features
                    - 🏗️ **Visual Schema Builder**: Create custom data schemas
                    - 📋 **Pre-built Templates**: Common use cases ready to use
                    - 🔒 **Privacy Protection**: Multiple anonymization levels
                    - 📊 **Data Quality Controls**: Add missing values, outliers, duplicates
                    - 📤 **Multiple Export Formats**: CSV, JSON, Excel, Parquet, SQL, Python
                    - 🤖 **AI-Powered**: Uses AI for realistic text generation
                    """)
                
                with gr.Tab("Field Types"):
                    gr.Markdown("""
                    ## Supported Field Types
                    
                    ### Text Fields
                    - **name**: Person names
                    - **email**: Email addresses
                    - **address**: Street addresses
                    - **phone**: Phone numbers
                    - **company**: Company names
                    - **job_title**: Job titles
                    - **description**: Product descriptions
                    - **sentence**: Random sentences
                    - **paragraph**: Random paragraphs
                    - **url**: Web URLs
                    - **user_agent**: Browser user agents
                    - **mac_address**: MAC addresses
                    - **credit_card**: Credit card numbers
                    - **bank_account**: Bank account numbers
                    - **patient_id**: Medical patient IDs
                    - **medical_record**: Medical record numbers
                    - **diagnosis_code**: ICD-10 codes
                    - **medication**: Medication names
                    - **country**: Country names
                    - **city**: City names
                    - **zip_code**: ZIP codes
                    - **ipv4**: IPv4 addresses
                    - **ipv6**: IPv6 addresses
                    - **custom**: Custom text with patterns
                    
                    ### Numeric Fields
                    - **integer**: Random integers
                    - **float**: Random floats
                    - **percentage**: Percentage values
                    - **currency**: Currency amounts
                    - **id**: Numeric IDs
                    - **transaction_amount**: Transaction amounts
                    - **salary**: Salary amounts
                    - **age**: Age values
                    - **temperature**: Temperature readings
                    - **humidity**: Humidity percentages
                    - **latitude**: Latitude coordinates
                    - **longitude**: Longitude coordinates
                    - **rating**: Rating values
                    - **score**: Score values
                    
                    ### Date Fields
                    - **date**: Random dates
                    - **datetime**: Random date and time
                    - **time**: Random time
                    - **date_range**: Date ranges
                    - **signup_date**: Signup dates (weekday bias)
                    - **transaction_date**: Transaction dates (business hours bias)
                    - **hire_date**: Hire dates
                    - **visit_date**: Medical visit dates
                    - **post_date**: Social media post dates
                    - **sensor_timestamp**: IoT sensor timestamps
                    """)
                
                with gr.Tab("Privacy Features"):
                    gr.Markdown("""
                    ## Privacy Protection Features
                    
                    ### Privacy Levels
                    - **Low**: Realistic but identifiable data
                    - **Medium**: Realistic with anonymization (masking, fuzzing)
                    - **High**: Fully anonymous with differential privacy
                    
                    ### Anonymization Techniques
                    - **Email Masking**: j***@example.com
                    - **Name Pseudonymization**: Person 1, Person 2
                    - **Phone Masking**: ***-***-1234
                    - **Address Generalization**: 123 *** St
                    - **Date Fuzzing**: Random date shifts
                    - **Numeric Noise**: Statistical noise addition
                    
                    ### Differential Privacy
                    - Laplace noise for numeric data
                    - Gaussian noise for aggregations
                    - K-anonymity checking
                    - Privacy budget management
                    
                    ### PII Detection
                    - Automatic PII detection
                    - Risk level assessment
                    - Privacy report generation
                    """)
                
                with gr.Tab("Export Formats"):
                    gr.Markdown("""
                    ## Export Formats
                    
                    ### CSV
                    - Standard comma-separated values
                    - UTF-8 encoding
                    - Header row included
                    
                    ### JSON
                    - Array format: `[{"field": "value"}, ...]`
                    - Lines format: One JSON object per line
                    - Pretty-printed with indentation
                    
                    ### Excel (.xlsx)
                    - Multiple sheets support
                    - Formatted headers
                    - Auto-adjusted column widths
                    
                    ### Parquet
                    - Columnar format
                    - Efficient compression
                    - Schema preservation
                    
                    ### SQL
                    - INSERT statements
                    - Table creation ready
                    - Escaped values
                    
                    ### Python Pandas
                    - DataFrame code generation
                    - Ready to run
                    - Variable naming
                    """)
                
                with gr.Tab("Examples"):
                    gr.Markdown("""
                    ## Example Use Cases
                    
                    ### 1. Customer Database
                    Generate realistic customer data for testing CRM systems.
                    
                    ### 2. E-commerce Transactions
                    Create transaction data for testing payment systems.
                    
                    ### 3. Healthcare Records
                    Generate patient data for testing medical applications.
                    
                    ### 4. IoT Sensor Data
                    Create sensor readings for testing IoT platforms.
                    
                    ### 5. Social Media Posts
                    Generate social media content for testing analytics.
                    
                    ### 6. Financial Transactions
                    Create banking data for testing financial applications.
                    """)
        
        return tab
    
    def create_main_app(self) -> gr.Blocks:
        """Create the main application interface."""
        with gr.Blocks(
            title="Synthetic Data Generator",
            theme=gr.themes.Soft(
                primary_hue="blue",
                secondary_hue="gray",
                neutral_hue="slate"
            ),
            css="""
            .gradio-container {
                max-width: 1200px !important;
                margin: auto !important;
            }
            .tab-nav {
                background: linear-gradient(90deg, #1E40AF 0%, #3B82F6 100%);
            }
            """
        ) as app:
            # Header
            gr.Markdown("""
            # 🎲 Synthetic Data Generator
            
            Create realistic, privacy-preserving synthetic data for testing, development, and analysis.
            
            ---
            """)
            
            # Main tabs
            with gr.Tabs():
                with gr.Tab("🏗️ Schema Builder"):
                    self.create_schema_builder_tab()
                
                with gr.Tab("📋 Templates"):
                    self.create_templates_tab()
                
                with gr.Tab("🎲 Generate"):
                    self.create_generate_tab()
                
                with gr.Tab("📤 Export"):
                    self.create_export_tab()
                
                with gr.Tab("📚 Documentation"):
                    self.create_documentation_tab()
        
        return app
    
    # Event handler methods
    def update_field_subtype_options(self, field_type: str) -> Tuple[List[str], bool, bool]:
        """Update field subtype options based on field type."""
        subtype_options = {
            "text": ["name", "email", "address", "phone", "company", "job_title", 
                    "description", "sentence", "paragraph", "url", "user_agent", 
                    "mac_address", "credit_card", "bank_account", "patient_id", 
                    "medical_record", "diagnosis_code", "medication", "country", 
                    "city", "zip_code", "ipv4", "ipv6", "custom"],
            "integer": ["integer", "id", "age", "rating", "score"],
            "float": ["float", "percentage", "currency", "transaction_amount", 
                     "salary", "temperature", "humidity", "latitude", "longitude", 
                     "rating", "score"],
            "date": ["date", "datetime", "time", "date_range", "signup_date", 
                    "transaction_date", "hire_date", "visit_date", "post_date", 
                    "sensor_timestamp"],
            "boolean": ["boolean"],
            "categorical": ["custom"]
        }
        
        options = subtype_options.get(field_type, ["custom"])
        show_categories = field_type == "categorical"
        show_pattern = field_type == "text"
        
        return gr.Dropdown(choices=options, value=options[0]), show_categories, show_pattern
    
    def add_field_to_schema(self, name: str, field_type: str, subtype: str, 
                           description: str, min_val: float, max_val: float,
                           null_percentage: float, unique: bool, categories: str,
                           pattern: str) -> Tuple[str, Dict]:
        """Add a field to the current schema."""
        if not name:
            return "Please enter a field name.", {}
        
        if not self.current_schema:
            self.current_schema = {
                "name": "Custom Schema",
                "description": "Custom synthetic data schema",
                "fields": []
            }
        
        # Build constraints
        constraints = {}
        if min_val is not None:
            constraints["min_val"] = min_val
        if max_val is not None:
            constraints["max_val"] = max_val
        if null_percentage > 0:
            constraints["null_percentage"] = null_percentage
        if unique:
            constraints["unique"] = True
        if categories and field_type == "categorical":
            constraints["categories"] = [cat.strip() for cat in categories.split(",")]
        if pattern and field_type == "text":
            constraints["pattern"] = pattern
        
        # Create field
        field = {
            "name": name,
            "type": field_type,
            "subtype": subtype,
            "description": description or f"Generated {field_type} field",
            "constraints": constraints
        }
        
        self.current_schema["fields"].append(field)
        
        # Update display
        fields_html = self._generate_fields_html()
        return fields_html, self.current_schema
    
    def _generate_fields_html(self) -> str:
        """Generate HTML display for fields."""
        if not self.current_schema or not self.current_schema["fields"]:
            return "<p>No fields added yet. Click 'Add Field' to get started.</p>"
        
        html = "<table style='width: 100%; border-collapse: collapse;'>"
        html += "<tr style='background-color: #f0f0f0;'>"
        html += "<th style='border: 1px solid #ddd; padding: 8px;'>Name</th>"
        html += "<th style='border: 1px solid #ddd; padding: 8px;'>Type</th>"
        html += "<th style='border: 1px solid #ddd; padding: 8px;'>Subtype</th>"
        html += "<th style='border: 1px solid #ddd; padding: 8px;'>Description</th>"
        html += "<th style='border: 1px solid #ddd; padding: 8px;'>Constraints</th>"
        html += "</tr>"
        
        for field in self.current_schema["fields"]:
            constraints_str = ", ".join([f"{k}: {v}" for k, v in field.get("constraints", {}).items()])
            html += "<tr>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{field['name']}</td>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{field['type']}</td>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{field['subtype']}</td>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{field['description']}</td>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{constraints_str}</td>"
            html += "</tr>"
        
        html += "</table>"
        return html
    
    def validate_current_schema(self, schema: Dict) -> str:
        """Validate the current schema."""
        if not schema:
            return "No schema to validate."
        
        validator = SchemaValidator()
        result = validator.validate_schema(schema)
        
        if result["valid"]:
            return "✅ Schema is valid!"
        else:
            errors = "\n".join([f"❌ {error}" for error in result["errors"]])
            return f"❌ Schema validation failed:\n{errors}"
    
    def update_template_preview(self, template_name: str) -> Tuple[Dict, str, str, List]:
        """Update template preview when selection changes."""
        if not template_name or template_name not in self.templates:
            return {}, "", "", []
        
        template = self.templates[template_name]
        
        # Convert fields to table format
        fields_table = []
        for field in template["fields"]:
            constraints_str = ", ".join([f"{k}: {v}" for k, v in field.get("constraints", {}).items()])
            fields_table.append([
                field["name"],
                field["type"],
                field.get("subtype", ""),
                field.get("description", ""),
                constraints_str
            ])
        
        return template, template["name"], template["description"], fields_table
    
    def load_template(self, template_name: str) -> str:
        """Load a template as the current schema."""
        if not template_name or template_name not in self.templates:
            return "❌ Template not found."
        
        self.current_schema = self.templates[template_name]
        return f"✅ Loaded template: {template_name}"
    
    def generate_data(self, num_rows: int, seed: int, privacy_level: str,
                     missing_percentage: float, outlier_percentage: float,
                     duplicate_percentage: float) -> Tuple[str, pd.DataFrame, str]:
        """Generate synthetic data based on current schema."""
        if not self.current_schema:
            return "❌ No schema loaded. Please select a template or build a custom schema.", pd.DataFrame(), ""
        
        try:
            # Set seed for reproducibility
            random.seed(seed)
            np.random.seed(seed)
            
            # Initialize generators with seed
            self.text_generator = TextGenerator(seed)
            self.numeric_generator = NumericGenerator(seed)
            self.date_generator = DateGenerator(seed)
            self.ai_generator = AIGenerator(seed)
            self.anonymizer = DataAnonymizer(seed)
            
            # Generate data
            data = []
            for i in range(num_rows):
                record = {}
                for field in self.current_schema["fields"]:
                    field_name = field["name"]
                    field_type = field["type"]
                    field_subtype = field.get("subtype", "custom")
                    constraints = field.get("constraints", {})
                    
                    # Generate value based on type
                    if field_type == "text":
                        value = self.text_generator.generate(1, field_subtype, **constraints)[0]
                    elif field_type == "integer":
                        value = self.numeric_generator.generate(1, field_subtype, **constraints)[0]
                    elif field_type == "float":
                        value = self.numeric_generator.generate(1, field_subtype, **constraints)[0]
                    elif field_type == "date":
                        value = self.date_generator.generate(1, field_subtype, **constraints)[0]
                    elif field_type == "boolean":
                        value = random.choice([True, False])
                    elif field_type == "categorical":
                        categories = constraints.get("categories", ["Option1", "Option2", "Option3"])
                        value = random.choice(categories)
                    else:
                        value = f"Generated_{i}"
                    
                    record[field_name] = value
                
                data.append(record)
            
            # Apply data quality controls
            if missing_percentage > 0:
                missing_count = int(len(data) * missing_percentage / 100)
                missing_indices = random.sample(range(len(data)), missing_count)
                for idx in missing_indices:
                    field_to_null = random.choice(list(data[idx].keys()))
                    data[idx][field_to_null] = None
            
            if duplicate_percentage > 0:
                duplicate_count = int(len(data) * duplicate_percentage / 100)
                duplicates = random.choices(data, k=duplicate_count)
                data.extend(duplicates)
            
            # Apply privacy protection
            if privacy_level != "low":
                for field in self.current_schema["fields"]:
                    field_name = field["name"]
                    field_type = field["type"]
                    field_values = [record[field_name] for record in data]
                    
                    anonymized_values = self.anonymizer.anonymize_data(
                        field_values, field_type, privacy_level
                    )
                    
                    for i, record in enumerate(data):
                        record[field_name] = anonymized_values[i]
            
            # Store generated data
            self.generated_data = data
            
            # Create DataFrame for preview
            df = pd.DataFrame(data)
            
            # Generate statistics
            stats_html = self._generate_statistics_html(data)
            
            return f"✅ Generated {len(data)} records successfully!", df.head(50), stats_html
            
        except Exception as e:
            return f"❌ Error generating data: {str(e)}", pd.DataFrame(), ""
    
    def _generate_statistics_html(self, data: List[Dict]) -> str:
        """Generate HTML statistics display."""
        if not data:
            return "<p>No data to analyze.</p>"
        
        html = "<div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px;'>"
        html += "<h3>📊 Dataset Statistics</h3>"
        html += f"<p><strong>Total Records:</strong> {len(data):,}</p>"
        html += f"<p><strong>Total Fields:</strong> {len(data[0].keys()) if data else 0}</p>"
        
        # Field statistics
        html += "<h4>Field Analysis:</h4>"
        html += "<table style='width: 100%; border-collapse: collapse;'>"
        html += "<tr style='background-color: #e9ecef;'>"
        html += "<th style='border: 1px solid #ddd; padding: 8px;'>Field</th>"
        html += "<th style='border: 1px solid #ddd; padding: 8px;'>Type</th>"
        html += "<th style='border: 1px solid #ddd; padding: 8px;'>Null %</th>"
        html += "<th style='border: 1px solid #ddd; padding: 8px;'>Unique</th>"
        html += "</tr>"
        
        for field_name in data[0].keys():
            values = [record[field_name] for record in data]
            null_count = sum(1 for v in values if v is None)
            null_percentage = (null_count / len(values)) * 100
            unique_count = len(set(v for v in values if v is not None))
            
            # Determine field type
            non_null_values = [v for v in values if v is not None]
            if non_null_values:
                field_type = type(non_null_values[0]).__name__
            else:
                field_type = "None"
            
            html += "<tr>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{field_name}</td>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{field_type}</td>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{null_percentage:.1f}%</td>"
            html += f"<td style='border: 1px solid #ddd; padding: 8px;'>{unique_count:,}</td>"
            html += "</tr>"
        
        html += "</table>"
        html += "</div>"
        
        return html
    
    def update_export_options(self, export_format: str) -> Tuple[bool, bool, bool]:
        """Update export options based on format."""
        show_json_format = export_format == "json"
        show_table_name = export_format == "sql"
        show_variable_name = export_format == "pandas"
        
        return show_json_format, show_table_name, show_variable_name
    
    def export_data(self, export_format: str, json_format: str, table_name: str,
                   variable_name: str, compress: bool) -> Tuple[str, str, str]:
        """Export generated data in specified format."""
        if not self.generated_data:
            return "❌ No data to export. Please generate data first.", "", ""
        
        try:
            exporter = DataExporter()
            
            if export_format == "csv":
                content = exporter.export_to_csv(self.generated_data)
                filename = "synthetic_data.csv"
            elif export_format == "json":
                content = exporter.export_to_json(self.generated_data, json_format)
                filename = "synthetic_data.json"
            elif export_format == "excel":
                content = exporter.export_to_excel(self.generated_data)
                filename = "synthetic_data.xlsx"
            elif export_format == "parquet":
                content = exporter.export_to_parquet(self.generated_data)
                filename = "synthetic_data.parquet"
            elif export_format == "sql":
                content = exporter.export_to_sql(self.generated_data, table_name)
                filename = "synthetic_data.sql"
            elif export_format == "pandas":
                content = exporter.export_to_pandas_code(self.generated_data, variable_name)
                filename = "synthetic_data.py"
            else:
                return "❌ Unsupported export format.", "", ""
            
            # Handle compression
            if compress and export_format in ["csv", "json", "sql", "pandas"]:
                files = {filename: content}
                content = exporter.create_zip_archive(files)
                filename = filename.replace(".", "_compressed.zip")
            
            # Create download file
            if isinstance(content, str):
                content_bytes = content.encode('utf-8')
            else:
                content_bytes = content
            
            # Encode for download
            b64_content = base64.b64encode(content_bytes).decode()
            download_url = f"data:application/octet-stream;base64,{b64_content}"
            
            # Generate export info
            export_info = exporter.get_export_info(self.generated_data, export_format)
            info_html = f"""
            <div style='background-color: #f8f9fa; padding: 15px; border-radius: 5px;'>
                <h3>📤 Export Information</h3>
                <p><strong>Format:</strong> {export_info['format'].upper()}</p>
                <p><strong>Size:</strong> {export_info['size_mb']} MB</p>
                <p><strong>Records:</strong> {export_info['record_count']:,}</p>
                <p><strong>Fields:</strong> {export_info['field_count']}</p>
            </div>
            """
            
            # Preview content (first 1000 characters)
            preview = content[:1000] if isinstance(content, str) else f"Binary file ({len(content)} bytes)"
            if len(content) > 1000 and isinstance(content, str):
                preview += "\n... (truncated)"
            
            return f"✅ Export ready! Click download to save.", download_url, info_html
            
        except Exception as e:
            return f"❌ Export failed: {str(e)}", "", ""


def main():
    """Main function to run the application."""
    app_instance = SyntheticDataApp()
    app = app_instance.create_main_app()
    
    app.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=True,
        show_error=True
    )


if __name__ == "__main__":
    main()
