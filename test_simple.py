"""
Simple test to verify the application components work
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

def test_imports():
    """Test that all modules can be imported"""
    print("Testing imports...")
    
    try:
        from generators import TextGenerator, NumericGenerator, DateGenerator
        print("✅ Generators imported successfully")
    except Exception as e:
        print(f"❌ Generator import failed: {e}")
        return False
    
    try:
        from templates import SchemaTemplates
        print("✅ Templates imported successfully")
    except Exception as e:
        print(f"❌ Template import failed: {e}")
        return False
    
    try:
        from privacy import DataAnonymizer
        print("✅ Privacy modules imported successfully")
    except Exception as e:
        print(f"❌ Privacy import failed: {e}")
        return False
    
    try:
        from utils import SchemaValidator, DataExporter
        print("✅ Utils imported successfully")
    except Exception as e:
        print(f"❌ Utils import failed: {e}")
        return False
    
    return True

def test_basic_functionality():
    """Test basic functionality"""
    print("\nTesting basic functionality...")
    
    try:
        from generators import TextGenerator, NumericGenerator
        from templates import SchemaTemplates
        
        # Test text generation
        text_gen = TextGenerator(seed=42)
        names = text_gen.generate(3, "name")
        print(f"✅ Generated names: {names}")
        
        # Test numeric generation
        num_gen = NumericGenerator(seed=42)
        ages = num_gen.generate(3, "age")
        print(f"✅ Generated ages: {ages}")
        
        # Test templates
        templates = SchemaTemplates.get_all_templates()
        print(f"✅ Available templates: {len(templates)}")
        
        return True
    except Exception as e:
        print(f"❌ Basic functionality test failed: {e}")
        return False

def test_gradio_import():
    """Test Gradio import and basic setup"""
    print("\nTesting Gradio...")
    
    try:
        import gradio as gr
        print(f"✅ Gradio imported successfully (version: {gr.__version__})")
        
        # Test basic Gradio interface
        def simple_function(text):
            return f"Hello {text}!"
        
        demo = gr.Interface(
            fn=simple_function,
            inputs="text",
            outputs="text",
            title="Test Interface"
        )
        print("✅ Gradio interface created successfully")
        
        return True
    except Exception as e:
        print(f"❌ Gradio test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🧪 Running Simple Tests for Synthetic Data Generator\n")
    
    all_passed = True
    
    # Test imports
    if not test_imports():
        all_passed = False
    
    # Test basic functionality
    if not test_basic_functionality():
        all_passed = False
    
    # Test Gradio
    if not test_gradio_import():
        all_passed = False
    
    if all_passed:
        print("\n🎉 All simple tests passed!")
        print("The application components are working correctly.")
        print("You can now run the full application with: python app.py")
    else:
        print("\n❌ Some tests failed. Please check the errors above.")
    
    return all_passed

if __name__ == "__main__":
    main()
