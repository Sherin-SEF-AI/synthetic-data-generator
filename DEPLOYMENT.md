# 🚀 Deployment Guide - Synthetic Data Generator

## Overview

This guide provides step-by-step instructions for deploying the Synthetic Data Generator application to Hugging Face Spaces or any other hosting platform.

## 📋 Prerequisites

- Python 3.8 or higher
- pip3 package manager
- Git (for version control)
- Hugging Face account (for Spaces deployment)

## 🏗️ Local Development Setup

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd synthetic-data-gen-HF
chmod +x install_and_run.sh
./install_and_run.sh
```

### 2. Manual Installation
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run tests
python3 test_app.py

# Start the application
python3 app.py
```

## 🌐 Hugging Face Spaces Deployment

### 1. Create a New Space
1. Go to [Hugging Face Spaces](https://huggingface.co/spaces)
2. Click "Create new Space"
3. Choose "Gradio" as the SDK
4. Set visibility (Public/Private)
5. Create the space

### 2. Upload Files
Upload these files to your Space:
- `app.py` (main application)
- `requirements.txt` (dependencies)
- `README.md` (documentation)
- All folders: `generators/`, `privacy/`, `templates/`, `utils/`, `assets/`

### 3. Configure Space Settings
In your Space settings:
- **SDK**: Gradio
- **SDK Version**: 4.44.0
- **App File**: app.py
- **Hardware**: CPU Basic (free) or upgrade for better performance

### 4. Deploy
The Space will automatically build and deploy when you push files.

## 🔧 Configuration Options

### Environment Variables
You can set these in your Space settings:

```bash
# Default seed for reproducibility
DEFAULT_SEED=42

# Default privacy level
DEFAULT_PRIVACY_LEVEL=medium

# Maximum rows for generation
MAX_ROWS=100000

# Enable/disable AI features
ENABLE_AI_GENERATION=true
```

### Custom Templates
To add custom templates:

1. Edit `templates/schema_templates.py`
2. Add your template method
3. Update the `get_all_templates()` method
4. Redeploy

## 📊 Performance Optimization

### For Large Datasets
- Use chunked generation for >10,000 rows
- Enable compression for exports
- Consider upgrading hardware for faster generation

### Memory Management
- The app automatically handles memory for large datasets
- Streaming exports for files >100MB
- Progress indicators for long operations

## 🔒 Security Considerations

### Privacy Levels
- **Low**: For internal testing only
- **Medium**: Suitable for most use cases
- **High**: For sensitive data scenarios

### Data Handling
- No data is stored permanently
- All generation happens in memory
- Downloads are temporary

## 🐛 Troubleshooting

### Common Issues

#### 1. Import Errors
```bash
# Ensure all dependencies are installed
pip3 install -r requirements.txt
```

#### 2. Memory Issues
- Reduce the number of rows
- Use chunked generation
- Upgrade hardware

#### 3. Slow Generation
- Use smaller datasets for testing
- Disable AI generation for faster results
- Check system resources

### Debug Mode
To enable debug mode, modify `app.py`:
```python
app.launch(
    debug=True,
    show_error=True
)
```

## 📈 Monitoring

### Usage Metrics
The app tracks:
- Number of generations
- Popular templates
- Export formats used
- Error rates

### Performance Metrics
- Generation speed
- Memory usage
- Export times

## 🔄 Updates and Maintenance

### Regular Updates
1. Update dependencies in `requirements.txt`
2. Test with `python3 test_app.py`
3. Deploy to Spaces

### Adding Features
1. Create feature branch
2. Implement changes
3. Add tests
4. Update documentation
5. Deploy

## 📞 Support

### Getting Help
- Check the README.md for documentation
- Run `python3 test_app.py` for diagnostics
- Check Hugging Face Spaces logs for errors

### Reporting Issues
- Use GitHub Issues for bug reports
- Include error messages and steps to reproduce
- Provide system information

## 🎯 Best Practices

### For Users
- Start with small datasets (100-1000 rows)
- Use templates for common use cases
- Set appropriate privacy levels
- Validate schemas before generation

### For Developers
- Follow the existing code structure
- Add tests for new features
- Update documentation
- Use type hints and docstrings

## 📋 Checklist for Deployment

- [ ] All files uploaded to Space
- [ ] Dependencies installed correctly
- [ ] Tests passing
- [ ] Documentation updated
- [ ] Privacy settings configured
- [ ] Performance tested
- [ ] Error handling verified
- [ ] Export functionality working

## 🎉 Success!

Once deployed, your Synthetic Data Generator will be available at:
`https://huggingface.co/spaces/your-username/your-space-name`

Users can:
- Build custom schemas
- Use pre-built templates
- Generate realistic data
- Export in multiple formats
- Maintain privacy compliance

---

**Happy generating! 🎲**
