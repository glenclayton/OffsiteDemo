# Project Structure

## Django Project Organization

### Standard Django Layout
```
nigel_api/                 # Django project root
├── manage.py             # Django management script
├── requirements.txt      # Python dependencies
├── nigel_api/           # Main project package
│   ├── __init__.py
│   ├── settings.py      # Django settings
│   ├── urls.py          # URL routing
│   └── wsgi.py          # WSGI application
└── api/                 # Main API application
    ├── __init__.py
    ├── models.py        # Data models (if needed)
    ├── views.py         # API views/endpoints
    ├── urls.py          # API URL patterns
    ├── serializers.py   # DRF serializers
    ├── utils.py         # Prime number calculations
    └── test_*.py        # pytest test files
```

### Key Conventions
- **Apps**: Use Django apps to organize functionality
- **Views**: Keep API logic in views.py or separate view modules
- **Utils**: Mathematical calculations in utils.py or separate modules
- **Tests**: Use pytest for comprehensive test coverage in test_*.py files or tests/ directory
- **Settings**: Environment-specific settings management

### File Naming
- Use lowercase with underscores for Python files
- Use descriptive names for modules and functions
- Follow Django naming conventions for models, views, and URLs

### Code Organization
- Separate business logic from API presentation
- Keep prime number calculation logic in utility modules
- Use Django REST Framework serializers for data validation
- Implement proper error handling and logging

### Configuration Files
- `.env` files for environment variables
- `requirements.txt` or `pyproject.toml` for dependencies
- Django settings split by environment (dev/prod)
- CORS configuration for cross-origin requests