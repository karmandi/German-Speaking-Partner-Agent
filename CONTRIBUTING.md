# Contributing to German Speaking Partner Agent

Thank you for your interest in contributing to this project! We welcome contributions from everyone. This document provides guidelines and instructions for contributing.

## 🎯 How to Contribute

### Reporting Bugs
If you encounter a bug, please create an issue with:
- Clear description of the bug
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)
- Screenshots/logs if applicable

### Suggesting Enhancements
We love feature ideas! Please submit an issue with:
- Clear description of the enhancement
- Use cases and benefits
- Possible implementation approach
- Examples or mockups if relevant

### Code Contributions
1. **Fork the repository**
   ```bash
   git clone https://github.com/yourusername/German-Speaking-Partner-Agent.git
   ```

2. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make your changes**
   - Keep changes focused and purposeful
   - Follow code style guidelines below
   - Add comments for complex logic
   - Update docstrings

4. **Test your changes**
   ```bash
   # Backend
   cd backend
   python -m pytest

   # Frontend
   cd frontend
   npm run lint
   npm run build
   ```

5. **Commit with meaningful messages**
   ```bash
   git commit -m "feat: Add feature description"
   ```

6. **Push and create a Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 📋 Code Style Guidelines

### Python (Backend)
- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints for functions
- Keep functions focused and under 50 lines when possible
- Use meaningful variable names
- Add docstrings to all public functions

Example:
```python
def generate_tutor_reply(user_input: str) -> Dict[str, str]:
    """
    Generate a natural German reply with corrections.
    
    Args:
        user_input: User's German sentence
        
    Returns:
        Dictionary with assistant reply and corrections
    """
    # Implementation here
    pass
```

### JavaScript/React (Frontend)
- Use functional components with hooks
- Keep components small and single-purpose
- Use meaningful prop names
- Add PropTypes or TypeScript types
- Use descriptive variable names

Example:
```javascript
function AudioRecorder({ onAudioSubmit }) {
  const [isRecording, setIsRecording] = useState(false);
  
  const handleStart = () => {
    setIsRecording(true);
  };
  
  return (
    <div className="recorder">
      {/* Component JSX */}
    </div>
  );
}
```

## 🔄 Pull Request Process

1. **Update documentation** - If your changes affect how the app works, update README or relevant docs
2. **Add tests** - Include tests for new features/bug fixes
3. **Ensure CI passes** - All automated checks must pass
4. **Request review** - Maintainers will review within 48 hours
5. **Address feedback** - Make requested changes and re-request review
6. **Merge** - Maintainers will merge once approved

## 📚 Development Setup

### Backend Development
```bash
cd backend
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

pip install -r requirements.txt
pip install pytest pytest-cov  # For testing

# Create .env file
echo "OPENAI_API_KEY=your_key_here" > .env

# Run the server
uvicorn app.main:app --reload

# Run tests
pytest
```

### Frontend Development
```bash
cd frontend
npm install

# Start development server
npm run dev

# Lint code
npm run lint

# Build for production
npm run build
```

## 📖 Documentation Standards

- Update README.md for new features
- Add inline comments for complex logic
- Keep commit messages clear and concise
- Use conventional commit format:
  - `feat:` - New feature
  - `fix:` - Bug fix
  - `docs:` - Documentation
  - `style:` - Code style
  - `refactor:` - Code refactoring
  - `perf:` - Performance improvement

## 🔒 Security Guidelines

- Never commit API keys or secrets
- Use environment variables for sensitive data
- Validate all user inputs
- Sanitize file uploads
- Report security vulnerabilities privately

## ❓ Questions?

- Check existing issues/discussions first
- Read the README and project documentation
- Open a discussion for questions
- Tag maintainers if urgent

## 📝 License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for making German Speaking Partner Agent better! 🚀**
