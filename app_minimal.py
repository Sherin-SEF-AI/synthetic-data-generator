"""
Minimal version of the Synthetic Data Generator for testing
"""

import gradio as gr
import pandas as pd
import random
import json
from typing import Dict, List, Any

# Import our modules
from generators import TextGenerator, NumericGenerator, DateGenerator
from templates import SchemaTemplates
from utils import DataExporter

def generate_sample_data(num_rows: int, template_name: str) -> pd.DataFrame:
    """Generate sample data using a template"""
    templates = SchemaTemplates.get_all_templates()
    
    if template_name not in templates:
        return pd.DataFrame()
    
    template = templates[template_name]
    data = []
    
    # Initialize generators
    text_gen = TextGenerator(seed=42)
    num_gen = NumericGenerator(seed=42)
    date_gen = DateGenerator(seed=42)
    
    for i in range(num_rows):
        record = {}
        for field in template["fields"]:
            field_name = field["name"]
            field_type = field["type"]
            field_subtype = field.get("subtype", "custom")
            constraints = field.get("constraints", {})
            
            try:
                if field_type == "text":
                    value = text_gen.generate(1, field_subtype, **constraints)[0]
                elif field_type == "integer":
                    value = num_gen.generate(1, field_subtype, **constraints)[0]
                elif field_type == "float":
                    value = num_gen.generate(1, field_subtype, **constraints)[0]
                elif field_type == "date":
                    value = date_gen.generate(1, field_subtype, **constraints)[0]
                elif field_type == "boolean":
                    value = random.choice([True, False])
                elif field_type == "categorical":
                    categories = constraints.get("categories", ["Option1", "Option2"])
                    value = random.choice(categories)
                else:
                    value = f"Generated_{i}"
                
                record[field_name] = value
            except Exception as e:
                record[field_name] = f"Error: {str(e)}"
        
        data.append(record)
    
    return pd.DataFrame(data)

def export_data_csv(data: pd.DataFrame) -> str:
    """Export data as CSV"""
    if data.empty:
        return "No data to export"
    
    exporter = DataExporter()
    csv_content = exporter.export_to_csv(data.to_dict('records'))
    return csv_content

def create_interface():
    """Create the Gradio interface"""
    
    with gr.Blocks(title="Synthetic Data Generator - Minimal") as demo:
        gr.Markdown("# 🎲 Synthetic Data Generator")
        gr.Markdown("Generate realistic synthetic data using pre-built templates.")
        
        with gr.Row():
            with gr.Column(scale=1):
                # Template selection
                template_dropdown = gr.Dropdown(
                    choices=list(SchemaTemplates.get_all_templates().keys()),
                    label="Select Template",
                    value="customer_database"
                )
                
                # Number of rows
                num_rows = gr.Slider(
                    10, 1000, 100, step=10,
                    label="Number of Rows"
                )
                
                # Generate button
                generate_btn = gr.Button("🚀 Generate Data", variant="primary")
            
            with gr.Column(scale=2):
                # Data preview
                data_preview = gr.Dataframe(
                    label="Generated Data Preview"
                )
                
                # Export section
                gr.Markdown("### Export Data")
                export_btn = gr.Button("📥 Export as CSV")
                export_output = gr.Textbox(
                    label="CSV Export",
                    lines=10
                )
        
        # Event handlers
        generate_btn.click(
            fn=generate_sample_data,
            inputs=[num_rows, template_dropdown],
            outputs=[data_preview]
        )
        
        export_btn.click(
            fn=export_data_csv,
            inputs=[data_preview],
            outputs=[export_output]
        )
    
    return demo

def main():
    """Main function"""
    print("🚀 Starting Minimal Synthetic Data Generator...")
    
    demo = create_interface()
    
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False,
        show_error=True,
        debug=True
    )

if __name__ == "__main__":
    main()
