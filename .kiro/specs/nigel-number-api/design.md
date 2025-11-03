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
- **Development Server**: Django development server
- **Testing**: pytest with pytest-django

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

## Deployment Considerations

### Environment Configuration
- Environment-specific settings (development/production)
- Configurable logging levels
- CORS settings management

### Scalability
- Stateless design enables horizontal scaling
- No database dependencies simplify deployment
- Containerization-ready architecture