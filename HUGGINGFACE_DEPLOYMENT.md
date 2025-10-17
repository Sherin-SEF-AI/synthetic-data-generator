# 🚀 Hugging Face Spaces Deployment Guide

## Quick Deployment Steps

### Option 1: Automatic Deployment (Recommended)

1. **Run the deployment script:**
   ```bash
   python deploy_to_hf.py
   ```

2. **Follow the prompts:**
   - Enter your Hugging Face username
   - Enter your space name (e.g., `username/synthetic-data-generator`)

3. **Wait for deployment:**
   - The script will automatically create the space and upload all files
   - Your app will be available at: `https://huggingface.co/spaces/username/synthetic-data-generator`

### Option 2: Manual Deployment

1. **Create a new Space on Hugging Face:**
   - Go to [Hugging Face Spaces](https://huggingface.co/spaces)
   - Click "Create new Space"
   - Choose "Gradio" as the SDK
   - Set visibility (Public/Private)
   - Create the space

2. **Upload files:**
   - Upload all files from this directory to your space
   - Ensure `app.py` is the main file
   - Upload `requirements.txt` with dependencies

3. **Configure the space:**
   - Set the app file to `app.py`
   - The space will automatically build and deploy

## 📁 Files to Upload

### Required Files
- ✅ `app.py` - Main application file
- ✅ `requirements.txt` - Python dependencies
- ✅ `README.md` - Documentation
- ✅ `config.yaml` - Space configuration

### Required Directories
- ✅ `generators/` - Data generation modules
- ✅ `privacy/` - Privacy protection modules
- ✅ `templates/` - Pre-built schema templates
- ✅ `utils/` - Utility functions
- ✅ `assets/` - Example files and assets

### Optional Files
- ✅ `.gitattributes` - Git LFS configuration
- ✅ `.gitignore` - Git ignore rules
- ✅ `DEPLOYMENT.md` - Deployment documentation
- ✅ `FEATURE_SUMMARY.md` - Feature documentation

## ⚙️ Space Configuration

The space is configured with the following settings:

```yaml
title: "Synthetic Data Generator"
emoji: "🎲"
colorFrom: "blue"
colorTo: "purple"
sdk: "gradio"
sdk_version: "5.49.1"
app_file: "app.py"
pinned: false
license: "apache-2.0"
tags:
  - synthetic-data
  - data-generation
  - privacy
  - machine-learning
  - data-science
  - testing
  - development
```

## 🔧 Hardware Requirements

### Recommended Hardware
- **CPU Basic**: For testing and small datasets (up to 1,000 rows)
- **CPU Upgrade**: For larger datasets (up to 10,000 rows)
- **GPU**: For AI-powered text generation (optional)

### Memory Usage
- **Base Application**: ~200MB
- **With AI Models**: ~1GB
- **Large Datasets**: Additional memory as needed

## 📊 Performance Optimization

### For Hugging Face Spaces
1. **Start with small datasets** (100-1,000 rows) for testing
2. **Use CPU Basic** for initial deployment
3. **Upgrade hardware** if needed for larger datasets
4. **Monitor memory usage** in the space logs

### Optimization Tips
- The app automatically handles memory management
- Large datasets are generated in chunks
- Export streaming prevents memory issues
- AI features have fallback to Faker for performance

## 🐛 Troubleshooting

### Common Issues

#### 1. Build Failures
- Check `requirements.txt` for version conflicts
- Ensure all dependencies are compatible
- Check the build logs in the space

#### 2. Memory Issues
- Reduce the number of rows generated
- Use CPU Basic hardware
- Disable AI features if not needed

#### 3. Import Errors
- Verify all Python files are uploaded
- Check file paths and imports
- Ensure all modules are in the correct directories

### Debug Mode
To enable debug mode, modify `app.py`:
```python
app.launch(
    debug=True,
    show_error=True
)
```

## 📈 Monitoring

### Space Metrics
- **Build Status**: Check the space build logs
- **Memory Usage**: Monitor in the space settings
- **User Activity**: View in the space analytics

### Application Logs
- Check the space logs for runtime errors
- Monitor memory usage during generation
- Track user interactions and performance

## 🔄 Updates

### Updating the Space
1. **Make changes** to your local files
2. **Commit changes** to git
3. **Push to Hugging Face**:
   ```bash
   git add .
   git commit -m "Update: description of changes"
   git push origin main
   ```

### Version Control
- The space automatically rebuilds on push
- Use meaningful commit messages
- Tag releases for version tracking

## 🎯 Best Practices

### For Users
- Start with small datasets (100-1,000 rows)
- Use pre-built templates for common use cases
- Set appropriate privacy levels
- Export in your preferred format

### For Developers
- Test locally before deploying
- Use version control for changes
- Monitor space performance
- Keep dependencies updated

## 📞 Support

### Getting Help
- Check the space logs for errors
- Review the README.md for documentation
- Test locally with `python app.py`
- Check Hugging Face Spaces documentation

### Reporting Issues
- Use GitHub Issues for bug reports
- Include error messages and steps to reproduce
- Provide space URL and configuration details

## 🎉 Success!

Once deployed, your Synthetic Data Generator will be available at:
`https://huggingface.co/spaces/your-username/your-space-name`

Users can:
- ✅ Generate realistic synthetic data
- ✅ Use 10 pre-built templates
- ✅ Export in 6 different formats
- ✅ Maintain privacy compliance
- ✅ Access comprehensive documentation

---

**Happy generating! 🎲**
