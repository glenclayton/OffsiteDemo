# Nigel Number API

A Django-based REST API server that calculates the "Nigel Number" for any given positive integer. The Nigel Number is defined as the sum of all prime numbers that are less than or equal to a given positive integer N.

## Quick Start

### Prerequisites

- Python 3.8 or higher
- pip (Python package installer)

### Installation

1. Clone or download the project
2. Create a virtual environment (recommended):
   ```bash
   python -m venv venv
   source venv/bin/activate  # On macOS/Linux
   # or
   venv\Scripts\activate     # On Windows
   ```

3. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

### Running the Server

#### Using the Startup Script (Recommended)

The easiest way to start the server is using the provided `run.py` script:

```bash
# Start with default settings (host: 127.0.0.1, port: 8000)
python run.py

# Start on a different port
python run.py --port 9000

# Allow external connections
python run.py --host 0.0.0.0

# Enable debug mode
python run.py --debug

# Skip automatic database migrations
python run.py --no-migrate

# Enable verbose logging
python run.py --verbose
```

#### Using Django's manage.py

Alternatively, you can use Django's standard management command:

```bash
# Run migrations first
python manage.py migrate

# Start the server
python manage.py runserver 127.0.0.1:8000
```

### Environment Variables

You can configure the server using environment variables:

- `NIGEL_API_HOST`: Default host (default: 127.0.0.1)
- `NIGEL_API_PORT`: Default port (default: 8000)
- `NIGEL_API_DEBUG`: Enable debug mode (default: False)
- `DJANGO_SETTINGS_MODULE`: Django settings module

Example:
```bash
export NIGEL_API_HOST=0.0.0.0
export NIGEL_API_PORT=9000
export NIGEL_API_DEBUG=true
python run.py
```

## API Usage

Once the server is running, you can access the API at:

```
GET http://localhost:8000/api/nigel-number/?n=<positive_integer>
```

### Examples

```bash
# Calculate Nigel Number for 10
curl "http://localhost:8000/api/nigel-number/?n=10"

# Response:
{
    "input": 10,
    "nigel_number": 17,
    "primes_found": [2, 3, 5, 7]
}
```

### Error Responses

The API returns appropriate HTTP status codes and error messages:

```bash
# Invalid input
curl "http://localhost:8000/api/nigel-number/?n=-5"

# Response (HTTP 400):
{
    "error": "Invalid input value",
    "details": "Parameter 'n' must be greater than 0"
}
```

## Development

### Running Tests

```bash
# Run all tests
DJANGO_SETTINGS_MODULE=nigel_api.settings pytest

# Run with verbose output
DJANGO_SETTINGS_MODULE=nigel_api.settings pytest -v

# Run specific test file
DJANGO_SETTINGS_MODULE=nigel_api.settings pytest api/tests.py
```

### Project Structure

```
nigel_api/
├── manage.py              # Django management script
├── run.py                 # Main startup script
├── requirements.txt       # Python dependencies
├── README.md             # This file
├── nigel_api/            # Django project settings
│   ├── __init__.py
│   ├── settings.py       # Django configuration
│   ├── urls.py           # Main URL routing
│   └── wsgi.py           # WSGI application
└── api/                  # Main API application
    ├── __init__.py
    ├── views.py          # API endpoints
    ├── urls.py           # API URL patterns
    ├── serializers.py    # Request/response serializers
    ├── utils.py          # Prime number calculations
    └── test_*.py         # Test files
```

## Features

- RESTful API endpoint for Nigel Number calculation
- Input validation for positive integers
- Proper HTTP status codes and error handling
- JSON response format
- CORS support for cross-origin requests
- Performance optimizations for large inputs
- Request logging for monitoring
- Automatic database migrations
- Configurable host, port, and debug settings
- Environment variable support

## Troubleshooting

### Common Issues

1. **Port already in use**: Try a different port with `--port` option
2. **Permission denied**: On some systems, ports below 1024 require admin privileges
3. **Django not found**: Make sure you've activated your virtual environment and installed dependencies
4. **Migration errors**: Try running `python manage.py migrate` manually

### Getting Help

If you encounter issues:

1. Check the server logs for error messages
2. Ensure all dependencies are installed: `pip install -r requirements.txt`
3. Verify you're in the correct directory (should contain `manage.py`)
4. Try running with `--verbose` flag for more detailed logging

### Server Startup Script Options

```
usage: run.py [-h] [--host HOST] [--port PORT] [--debug] [--no-migrate] [--verbose]

Start the Nigel Number API server

options:
  -h, --help     show this help message and exit
  --host HOST    Host to bind the server to (default: 127.0.0.1)
  --port PORT    Port to bind the server to (default: 8000)
  --debug        Enable debug mode (default: False)
  --no-migrate   Skip automatic database migrations
  --verbose, -v  Enable verbose logging

Examples:
  python run.py                          # Start with default settings
  python run.py --host 0.0.0.0          # Allow external connections
  python run.py --port 9000             # Use custom port
  python run.py --debug                 # Enable debug mode
  python run.py --no-migrate            # Skip automatic migrations
```