# Contributing to Gamma AI

Thank you for your interest in contributing to Gamma AI! This document provides guidelines and instructions for contributing to the project.

## 📋 Table of Contents

- [Code of Conduct](#code-of-conduct)
- [Getting Started](#getting-started)
- [Development Process](#development-process)
- [Coding Standards](#coding-standards)
- [Commit Messages](#commit-messages)
- [Pull Request Process](#pull-request-process)
- [Testing Guidelines](#testing-guidelines)
- [Documentation](#documentation)

---

## Code of Conduct

### Our Pledge

We are committed to providing a welcoming and inclusive environment for all contributors, regardless of background or experience level.

### Expected Behavior

- Be respectful and considerate
- Use inclusive language
- Accept constructive criticism gracefully
- Focus on what's best for the community
- Show empathy towards others

### Unacceptable Behavior

- Harassment or discriminatory language
- Trolling or insulting comments
- Publishing private information without permission
- Any conduct that would be inappropriate in a professional setting

---

## Getting Started

### 1. Fork the Repository

Click the "Fork" button at the top right of the repository page.

### 2. Clone Your Fork

```bash
git clone https://github.com/YOUR_USERNAME/AI-PPTX.git
cd AI-PPTX
```

### 3. Set Up Development Environment

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment template
cp .env.example .env
# Edit .env with your credentials
```

### 4. Create a Branch

```bash
git checkout -b feature/your-feature-name
# or
git checkout -b fix/issue-description
```

---

## Development Process

### Branch Naming Conventions

- **Features**: `feature/feature-name`
- **Bug Fixes**: `fix/bug-description`
- **Documentation**: `docs/what-changed`
- **Performance**: `perf/optimization-description`
- **Refactoring**: `refactor/component-name`

### Development Workflow

1. **Create an Issue** (if one doesn't exist)
   - Describe the feature or bug
   - Get feedback from maintainers
   
2. **Implement Changes**
   - Write clean, readable code
   - Follow coding standards (see below)
   - Add comments for complex logic
   
3. **Test Thoroughly**
   - Test your changes manually
   - Ensure no existing functionality breaks
   - Add automated tests if applicable
   
4. **Document Changes**
   - Update README if needed
   - Add inline comments
   - Update API documentation

5. **Submit Pull Request**
   - Follow PR template
   - Link related issues
   - Request review

---

## Coding Standards

### Python Code Style

Follow **PEP 8** guidelines:

```python
# Good
def generate_slides(prompt, count=8):
    """Generate presentation slides using AI.
    
    Args:
        prompt (str): The topic for the presentation
        count (int): Number of slides to generate
        
    Returns:
        list: Generated slide data
    """
    slides = []
    # Implementation...
    return slides

# Bad
def GenerateSlides(Prompt,Count=8):
    slides=[]
    return slides
```

### Key Python Guidelines

- **Indentation**: 4 spaces (no tabs)
- **Line Length**: Maximum 120 characters
- **Naming**:
  - Functions/variables: `snake_case`
  - Classes: `PascalCase`
  - Constants: `UPPER_CASE`
- **Imports**: Group in order (standard library, third-party, local)
- **Docstrings**: Use triple quotes for all functions and classes

### JavaScript Code Style

Follow **Airbnb Style Guide**:

```javascript
// Good
async function fetchPresentations() {
    try {
        const response = await apiRequest('/presentations');
        return response.data;
    } catch (error) {
        console.error('Failed to fetch presentations:', error);
        throw error;
    }
}

// Bad
function fetchPresentations() {
    return apiRequest('/presentations').then(r => r.data)
}
```

### Key JavaScript Guidelines

- **Indentation**: 4 spaces
- **Semicolons**: Always use them
- **Quotes**: Single quotes for strings
- **Arrow Functions**: Prefer for anonymous functions
- **Async/Await**: Use instead of raw promises
- **Comments**: Use JSDoc for function documentation

### HTML/CSS Guidelines

```html
<!-- Good -->
<div class="presentation-card" id="pres-123">
    <h3 class="presentation-title">My Presentation</h3>
    <p class="presentation-description">Description here</p>
</div>

<!-- Bad -->
<div id="pres-123" class="presentation-card">
    <h3>My Presentation</h3>
    <p>Description here</p>
</div>
```

**CSS:**
- Use meaningful class names
- Follow BEM naming convention when appropriate
- Group related styles together
- Add comments for complex selectors

---

## Commit Messages

### Format

```
<type>(<scope>): <subject>

<body>

<footer>
```

### Types

- **feat**: New feature
- **fix**: Bug fix
- **docs**: Documentation changes
- **style**: Code style changes (formatting, no logic change)
- **refactor**: Code refactoring
- **perf**: Performance improvements
- **test**: Adding or updating tests
- **chore**: Maintenance tasks

### Examples

```bash
# Good
feat(ai): Add support for DeepSeek AI model
fix(auth): Resolve JWT token expiration issue
docs(readme): Update installation instructions
perf(export): Optimize PDF generation speed

# Bad
fixed stuff
update
changes
```

### Detailed Commit Message

```
feat(presentations): Add slide duplication feature

- Add "Duplicate Slide" button to editor
- Implement server-side duplication logic
- Update API documentation
- Add validation for maximum slides limit

Closes #123
```

---

## Pull Request Process

### Before Submitting

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] Documentation updated
- [ ] Commits are well-formatted
- [ ] No merge conflicts
- [ ] Self-reviewed code

### PR Template

```markdown
## Description
Brief description of changes

## Type of Change
- [ ] Bug fix
- [ ] New feature
- [ ] Breaking change
- [ ] Documentation update

## Testing
How has this been tested?

## Checklist
- [ ] Code follows style guidelines
- [ ] Self-reviewed code
- [ ] Commented complex code
- [ ] Updated documentation
- [ ] No new warnings
- [ ] Added tests (if applicable)

## Related Issues
Closes #123
```

### Review Process

1. **Automated Checks**: CI/CD must pass
2. **Code Review**: At least one maintainer approval
3. **Testing**: Manual testing by reviewer
4. **Feedback**: Address all review comments
5. **Merge**: Maintainer will merge once approved

---

## Testing Guidelines

### Manual Testing

Before submitting PR, test:

1. **Fresh Installation**
   ```bash
   pip install -r requirements.txt
   python run.py
   ```

2. **Core Features**
   - User registration/login
   - Presentation generation
   - Edit presentation
   - Export to PDF/DOCX/PPTX
   - Theme selection

3. **Edge Cases**
   - Invalid inputs
   - Long text content
   - Special characters
   - Network failures

### Automated Testing (Future)

When adding tests:

```python
# tests/test_ai_service.py
import pytest
from services.ai_service import CloudAIService

def test_generate_slides():
    service = CloudAIService()
    slides = service.generate_slides("Test Topic", slides_count=3)
    
    assert len(slides) == 3
    assert all('title' in slide for slide in slides)
    assert all('content' in slide for slide in slides)
```

Run tests:
```bash
pytest tests/
```

---

## Documentation

### Inline Comments

```python
# Good - Explains WHY
# Use native DNS resolver to fix Windows GRPC issues
os.environ['GRPC_DNS_RESOLVER'] = 'native'

# Bad - Explains WHAT (already obvious)
# Set environment variable
os.environ['GRPC_DNS_RESOLVER'] = 'native'
```

### Function Documentation

```python
def generate_slides(prompt, slides_count=8, language="English", theme="dialogue"):
    """Generate presentation slides using AI.
    
    This function calls the AI API to generate slide content based on the
    provided prompt. It handles retries and fallbacks if the primary API fails.
    
    Args:
        prompt (str): The topic or description for the presentation
        slides_count (int, optional): Number of slides to generate. Defaults to 8.
        language (str, optional): Language for content. Defaults to "English".
        theme (str, optional): Visual theme name. Defaults to "dialogue".
        
    Returns:
        list[dict]: List of slide dictionaries with 'title', 'content', 'layout', etc.
        
    Raises:
        ValueError: If slides_count is not between 3 and 20
        APIError: If all AI services fail to respond
        
    Example:
        >>> slides = generate_slides("Climate Change", slides_count=5)
        >>> len(slides)
        5
    """
```

### README Updates

When adding features, update:
- Feature list
- Configuration section (if new env vars)
- API endpoints (if new routes)
- Troubleshooting (if common issues)

---

## Questions?

- **General Questions**: Open a [Discussion](https://github.com/Bsoumyaranjan32/AI-PPTX/discussions)
- **Bug Reports**: Open an [Issue](https://github.com/Bsoumyaranjan32/AI-PPTX/issues)
- **Feature Requests**: Open an [Issue](https://github.com/Bsoumyaranjan32/AI-PPTX/issues) with `[Feature Request]` prefix

---

## Recognition

All contributors will be recognized in:
- Repository contributors list
- Release notes
- Special mentions for significant contributions

Thank you for contributing to Gamma AI! 🎉
