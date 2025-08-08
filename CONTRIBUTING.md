# Contributing to TalkVision

Thank you for your interest in contributing to TalkVision! This document provides guidelines for contributing to the project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/TalkVision.git
   cd TalkVision
   ```
3. **Create a virtual environment**:
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```
4. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

## 🔄 Development Workflow

1. **Create a feature branch**:

   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and ensure they work:

   ```bash
   uvicorn app:app --reload
   ```

3. **Test your changes** thoroughly

4. **Commit your changes**:

   ```bash
   git add .
   git commit -m "Add: description of your changes"
   ```

5. **Push to your fork**:

   ```bash
   git push origin feature/your-feature-name
   ```

6. **Create a Pull Request** on GitHub

## 📝 Commit Message Guidelines

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove, etc.)
- Keep the first line under 50 characters
- Use present tense

Examples:

- `Add: audio validation for file uploads`
- `Fix: memory leak in audio processing`
- `Update: Whisper model to latest version`

## 🧪 Testing

Before submitting a PR, please ensure:

1. **The app starts without errors**:

   ```bash
   uvicorn app:app --reload
   ```

2. **API endpoints work correctly**:

   - Test `/` endpoint returns status
   - Test `/transcribe/` with a sample audio file

3. **Code follows Python best practices**:
   - Use proper error handling
   - Add docstrings to functions
   - Follow PEP 8 style guidelines

## 🎯 Areas for Contribution

We welcome contributions in these areas:

### 🚀 Features

- Support for additional audio formats
- Real-time streaming transcription
- Multiple language support
- Audio preprocessing improvements
- API rate limiting
- Authentication system

### 🐛 Bug Fixes

- Memory optimization
- Error handling improvements
- File cleanup issues
- Cross-platform compatibility

### 📚 Documentation

- API documentation improvements
- Code comments and docstrings
- Tutorial creation
- ESP32 integration examples

### 🔧 DevOps

- Docker containerization
- CI/CD pipeline improvements
- Monitoring and logging
- Performance optimizations

## 📋 Pull Request Guidelines

### Before Submitting

- [ ] Code runs without errors
- [ ] New features include appropriate error handling
- [ ] Changes are tested locally
- [ ] Documentation is updated if needed
- [ ] Commit messages follow guidelines

### PR Description Template

```markdown
## Description

Brief description of changes

## Type of Change

- [ ] Bug fix
- [ ] New feature
- [ ] Documentation update
- [ ] Performance improvement
- [ ] Code refactoring

## Testing

- [ ] Tested locally
- [ ] API endpoints work
- [ ] No breaking changes

## Checklist

- [ ] Code follows project style
- [ ] Self-review completed
- [ ] Documentation updated
```

## 🔍 Code Style

- Follow [PEP 8](https://pep8.org/) Python style guidelines
- Use meaningful variable and function names
- Add type hints where appropriate
- Include docstrings for functions and classes
- Keep functions small and focused

Example:

```python
def transcribe_audio(file_path: str) -> dict:
    """
    Transcribe the given audio file and return the result.

    Args:
        file_path (str): Path to the audio file

    Returns:
        dict: Transcription result with text and metadata

    Raises:
        FileNotFoundError: If audio file doesn't exist
        Exception: If transcription fails
    """
    # Implementation here
```

## 🆘 Getting Help

If you need help or have questions:

1. **Check existing issues** on GitHub
2. **Create a new issue** with detailed description
3. **Join discussions** in existing issues
4. **Review the documentation** in README.md

## 🎉 Recognition

Contributors will be acknowledged in:

- README.md contributors section
- Release notes for significant contributions
- GitHub contributors page

Thank you for helping make TalkVision better! 🙏
