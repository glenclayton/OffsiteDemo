# Design Document - Nigel Number API

## Overview

The Nigel Number API is a Django-based REST API server that provides a single endpoint for calculating the "Nigel Number" of any positive integer. The system follows RESTful conventions and implements robust error handling, input validation, and performance optimizations.

The API calculates the sum of all prime numbers less than or equal to a given positive integer N, returning the result in a structured JSON format with appropriate HTTP status codes.

## Architecture

### High-Level Architecture

```
Client Request → Django URL Router → API View → Prime Calculator → JSON Response
                                        ↓
                                   Input Validator
                                        ↓
                                   Error Handler
```

### Technology Stack
- **Framework**: Django with Django REST Framework
- **Language**: Python 3.x
- **API Style**: RESTful HTTP API
- **Response Format**: JSON
- **Development Server**: Django development server / Gunicorn (production)
- **Testing**: pytest with pytest-django
- **Containerization**: Docker with multi-stage builds

### Design Decisions

1. **Django REST Framework**: Chosen for its robust serialization, validation, and HTTP response handling capabilities
2. **Single Endpoint Design**: Simple GET endpoint aligns with the mathematical function nature of the service
3. **Stateless Design**: No database required as calculations are performed on-demand
4. **Efficient Prime Calculation**: Sieve of Eratosthenes algorithm for optimal performance with larger inputs

## Components and Interfaces

### API Endpoint

**Endpoint**: `GET /api/nigel-number/`
**Query Parameter**: `n` (positive integer)

**Request Example**:
```
GET /api/nigel-number/?n=10
```

**Success Response Example**:
```json
{
    "input": 10,
    "nigel_number": 17,
    "primes_found": [2, 3, 5, 7]
}
```

### Core Components

#### 1. API View (`api/views.py`)
- Handles HTTP requests and responses
- Orchestrates input validation and calculation
- Manages error responses and status codes
- Implements CORS headers

#### 2. Input Validator
- Validates query parameter presence
- Ensures input is a positive integer
- Returns structured error messages for invalid inputs

#### 3. Prime Number Calculator (`api/utils.py`)
- Implements Sieve of Eratosthenes algorithm
- Handles edge cases (N=1, N=2)
- Optimized for performance with reasonable input sizes
- Returns both the sum and list of primes found

#### 4. Serializer (`api/serializers.py`)
- Validates input parameters
- Structures response data
- Handles error message formatting

#### 5. URL Configuration
- Maps endpoint to view function
- Integrates with Django's URL routing system

## Data Models

### Request Model
```python
{
    "n": int  # Positive integer (required)
}
```

### Success Response Model
```python
{
    "input": int,           # Original input value
    "nigel_number": int,    # Calculated sum of primes
    "primes_found": list    # List of prime numbers found
}
```

### Error Response Model
```python
{
    "error": str,           # Error message
    "details": str          # Additional error details
}
```

## Error Handling

### Error Scenarios and Responses

#### 1. Missing Parameter (HTTP 400)
```json
{
    "error": "Missing required parameter",
    "details": "Parameter 'n' is required"
}
```

#### 2. Invalid Input Type (HTTP 400)
```json
{
    "error": "Invalid input type",
    "details": "Parameter 'n' must be a positive integer"
}
```

#### 3. Non-Positive Integer (HTTP 400)
```json
{
    "error": "Invalid input value",
    "details": "Parameter 'n' must be greater than 0"
}
```

#### 4. Internal Server Error (HTTP 500)
```json
{
    "error": "Internal server error",
    "details": "An unexpected error occurred during calculation"
}
```

### Error Handling Strategy
- Input validation occurs before any calculations
- All errors return structured JSON responses
- Appropriate HTTP status codes for different error types
- Detailed error messages for debugging while maintaining security
- Logging of all errors for monitoring purposes

## Performance Considerations

### Prime Number Calculation Optimization
- **Sieve of Eratosthenes**: Efficient algorithm for finding all primes up to N
- **Memory Management**: Reasonable limits on input size to prevent memory exhaustion
- **Caching Strategy**: No caching implemented initially (stateless design)
- **Time Complexity**: O(N log log N) for prime generation

### Edge Case Handling
- **N = 1**: Returns 0 (no primes ≤ 1)
- **N = 2**: Returns 2 (only prime ≤ 2 is 2 itself)
- **Large N**: Implements reasonable upper bounds to prevent performance issues

## Testing Strategy

### Test Categories

#### 1. Unit Tests
- Prime number calculation accuracy
- Input validation logic
- Edge case handling (N=1, N=2)
- Error message formatting

#### 2. Integration Tests
- End-to-end API endpoint testing
- HTTP status code validation
- JSON response structure verification
- CORS header presence

#### 3. Performance Tests
- Response time for various input sizes
- Memory usage validation
- Upper bound input testing

### Test Data Examples
- **Valid inputs**: 1, 2, 10, 100, 1000
- **Invalid inputs**: 0, -5, "abc", null, missing parameter
- **Edge cases**: Very large numbers, boundary conditions

### Testing Tools
- **pytest**: Primary testing framework
- **pytest-django**: Django-specific testing utilities
- **Django Test Client**: HTTP request simulation
- **Coverage tools**: Ensure comprehensive test coverage

## Security Considerations

### Input Validation
- Strict type checking for input parameters
- Range validation to prevent resource exhaustion
- SQL injection prevention (though no database is used)

### CORS Configuration
- Configurable CORS headers for cross-origin requests
- Appropriate security headers in responses

### Logging and Monitoring
- Request logging for audit trails
- Error logging for debugging and monitoring
- No sensitive data exposure in logs or error messages

## Docker Containerization Design

### Container Architecture

```
Docker Container
├── Python 3.x Runtime
├── Application Dependencies (requirements.txt)
├── Django Application Code
├── Gunicorn WSGI Server
└── Health Check Endpoint
```

### Dockerfile Design Strategy

#### Multi-Stage Build Approach
1. **Build Stage**: Install dependencies and prepare application
2. **Runtime Stage**: Copy only necessary files for minimal image size

#### Base Image Selection
- **Base Image**: `python:3.11-slim` for optimal size/performance balance
- **Security**: Regular base image updates for security patches
- **Size Optimization**: Multi-stage builds to reduce final image size

### Container Configuration

#### Port Configuration
- **Default Port**: 8000 (configurable via environment variable)
- **Health Check Port**: Same as application port
- **Port Mapping**: Configurable for different deployment environments

#### Environment Variables
```bash
PORT=8000                    # Application port
DJANGO_SETTINGS_MODULE=nigel_api.settings
DEBUG=False                  # Production setting
ALLOWED_HOSTS=*             # Configurable allowed hosts
```

#### Volume Mounts
- **Logs**: `/app/logs` for persistent logging
- **Static Files**: `/app/static` for static asset serving (if needed)

### Container Startup Process

1. **Dependency Installation**: Install Python packages from requirements.txt
2. **Application Setup**: Copy application code and configuration
3. **Database Migration**: Run Django migrations (if database is added later)
4. **Static Files**: Collect static files for production serving
5. **Server Startup**: Launch Gunicorn WSGI server
6. **Health Check**: Expose health check endpoint for container orchestration

### Production Server Configuration

#### Gunicorn Configuration
```python
# gunicorn.conf.py
bind = "0.0.0.0:8000"
workers = 4
worker_class = "sync"
worker_connections = 1000
max_requests = 1000
max_requests_jitter = 100
timeout = 30
keepalive = 2
```

#### Health Check Implementation
- **Endpoint**: `GET /health/`
- **Response**: JSON status with application health
- **Docker Health Check**: Built-in container health monitoring

### Container Security

#### Security Best Practices
- **Non-root User**: Run application as non-privileged user
- **Minimal Dependencies**: Only include necessary packages
- **Security Updates**: Regular base image updates
- **Secret Management**: Environment variables for sensitive configuration

#### Dockerfile Security Features
```dockerfile
# Create non-root user
RUN adduser --disabled-password --gecos '' appuser
USER appuser

# Set secure file permissions
COPY --chown=appuser:appuser . /app/
```

## Deployment Considerations

### Environment Configuration
- Environment-specific settings (development/production)
- Configurable logging levels
- CORS settings management
- Docker environment variable configuration

### Container Orchestration
- **Docker Compose**: Local development and testing
- **Kubernetes**: Production container orchestration
- **Health Checks**: Container health monitoring
- **Resource Limits**: CPU and memory constraints

### Scalability
- Stateless design enables horizontal scaling
- No database dependencies simplify deployment
- Container-based architecture supports auto-scaling
- Load balancer compatibility for multi-instance deployments

### Monitoring and Logging
- **Container Logs**: Structured logging to stdout/stderr
- **Health Monitoring**: Built-in health check endpoints
- **Metrics Collection**: Container resource usage monitoring
- **Log Aggregation**: Compatible with centralized logging systems