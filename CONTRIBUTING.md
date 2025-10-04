# Contributing to AdaptLearn

Thank you for your interest in contributing to AdaptLearn! This document provides guidelines and instructions for contributing to the project.

## 🚀 Getting Started

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/your-username/adaptlearn.git
   cd adaptlearn
   ```
3. **Set up the development environment** (see README.md)
4. **Create a branch** for your feature or bug fix:
   ```bash
   git checkout -b feature/your-feature-name
   ```

## 💻 Development Workflow

### Backend Development (Python/FastAPI)

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Run the backend server:
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000 --reload
   ```

3. Test your changes:
   ```bash
   pytest
   ```

4. Follow PEP 8 style guidelines

### Frontend Development (React/Vite)

1. Install dependencies:
   ```bash
   cd frontend
   npm install
   ```

2. Run the development server:
   ```bash
   npm run dev
   ```

3. Build for production:
   ```bash
   npm run build
   ```

4. Follow the existing code style (ESLint configured)

## 📝 Code Style

### Python
- Follow PEP 8 guidelines
- Use type hints where appropriate
- Write docstrings for functions and classes
- Keep functions focused and single-purpose

### JavaScript/React
- Use functional components with hooks
- Follow the existing component structure
- Use Tailwind CSS classes for styling
- Keep components small and reusable

### Commit Messages
Use conventional commits format:
```
type(scope): subject

body (optional)

footer (optional)
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Example:
```
feat(quiz): add LaTeX rendering support

- Added react-markdown with remark-math
- Integrated rehype-katex for math rendering
- Updated question generator prompts

Closes #123
```

## 🐛 Reporting Bugs

When reporting bugs, please include:

1. **Description**: Clear description of the issue
2. **Steps to Reproduce**: Detailed steps to reproduce the bug
3. **Expected Behavior**: What should happen
4. **Actual Behavior**: What actually happens
5. **Environment**: OS, browser, Python/Node versions
6. **Screenshots**: If applicable

## ✨ Suggesting Features

When suggesting features:

1. **Use Case**: Explain the problem you're trying to solve
2. **Proposed Solution**: Describe your suggested feature
3. **Alternatives**: Any alternative solutions you've considered
4. **Additional Context**: Screenshots, examples, etc.

## 🧪 Testing

### Backend Tests
```bash
pytest
pytest --cov=app  # With coverage
```

### Frontend Tests
```bash
cd frontend
npm test
```

## 📋 Pull Request Process

1. **Update documentation** if needed
2. **Add tests** for new features
3. **Ensure all tests pass**
4. **Update README.md** if adding new features
5. **Follow the code style** guidelines
6. **Write a clear PR description**:
   - What changes were made
   - Why they were made
   - How to test them

### PR Title Format
```
type: Brief description of changes

Examples:
- feat: Add support for custom difficulty levels
- fix: Resolve quiz timeout issue
- docs: Update API documentation
```

## 🔍 Code Review

All submissions require review. We'll:
- Check code quality and style
- Verify tests pass
- Ensure documentation is updated
- Test the functionality

## 🎯 Areas for Contribution

We welcome contributions in:

### Features
- Additional subjects and topics
- More chart types in analytics
- Export quiz results functionality
- User authentication system
- Question bank management UI
- Mobile app (React Native)

### Improvements
- Performance optimizations
- Better error handling
- Accessibility improvements
- Internationalization (i18n)
- Test coverage
- Documentation

### Bug Fixes
- Check the [Issues](https://github.com/yourusername/adaptlearn/issues) page

## 📚 Resources

- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS](https://tailwindcss.com/)
- [shadcn/ui](https://ui.shadcn.com/)
- [Google Gemini API](https://ai.google.dev/docs)

## 📄 License

By contributing, you agree that your contributions will be licensed under the same license as the project (MIT License).

## 🤝 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the code, not the person
- Help others learn and grow

## ❓ Questions?

Feel free to:
- Open an issue for questions
- Join discussions
- Reach out to maintainers

Thank you for contributing to AdaptLearn! 🎉
