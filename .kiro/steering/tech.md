# Technology Stack

## Framework & Language
- **Python**: Primary programming language
- **Django**: Web framework for REST API development
- **Django REST Framework**: For building RESTful APIs

## Development Environment
- **Python 3.x**: Required runtime
- **Virtual Environment**: Use venv for dependency isolation
- **VSCode**: Recommended IDE with Python extensions

## Common Commands

### Environment Setup
```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
source venv/bin/activate  # macOS/Linux

# Upgrade pip
pip install --upgrade pip

# Install dependencies
pip install django djangorestframework pytest pytest-django
```

### Development
```bash
# Run development server
python manage.py runserver

# Run migrations
python manage.py migrate

# Create migrations
python manage.py makemigrations

# Run tests
pytest

# Collect static files
python manage.py collectstatic
```

### Code Quality
```bash
# Format code (if using black)
black .

# Lint code (if using ruff)
ruff check .

# Type checking (if using mypy)
mypy .
```

## Dependencies
- Django for web framework
- Django REST Framework for API endpoints
- pytest and pytest-django for testing
- Standard library for prime number calculations
- Consider optimization libraries for large number processing