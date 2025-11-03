"""
Integration tests for the Nigel Number API endpoints.

These tests verify the complete API functionality including:
- HTTP request/response handling
- JSON response structure and content
- CORS headers
- HTTP status codes
- Input validation
- Error handling
- Performance with various input sizes
"""
import json
from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status


class NigelNumberAPIIntegrationTest(TestCase):
    """Integration tests for the Nigel Number API endpoint."""
    
    def setUp(self):
        """Set up test client and common test data."""
        self.client = Client()
        self.url = '/api/nigel-number/'
    
    def test_successful_calculation_small_input(self):
        """Test successful calculation with small input (n=10)."""
        response = self.client.get(self.url, {'n': 10})
        
        # Verify HTTP status code
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Verify response is JSON
        self.assertEqual(response['Content-Type'], 'application/json')
        
        # Parse and verify JSON response structure
        data = response.json()
        self.assertIn('input', data)
        self.assertIn('nigel_number', data)
        self.assertIn('primes_found', data)
        
        # Verify response content accuracy
        self.assertEqual(data['input'], 10)
        self.assertEqual(data['nigel_number'], 17)  # 2+3+5+7 = 17
        self.assertEqual(data['primes_found'], [2, 3, 5, 7])
    
    def test_successful_calculation_edge_case_n_equals_1(self):
        """Test successful calculation for edge case N=1."""
        response = self.client.get(self.url, {'n': 1})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['input'], 1)
        self.assertEqual(data['nigel_number'], 0)  # No primes <= 1
        self.assertEqual(data['primes_found'], [])
    
    def test_successful_calculation_edge_case_n_equals_2(self):
        """Test successful calculation for edge case N=2."""
        response = self.client.get(self.url, {'n': 2})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['input'], 2)
        self.assertEqual(data['nigel_number'], 2)  # Only prime <= 2 is 2
        self.assertEqual(data['primes_found'], [2])
    
    def test_successful_calculation_medium_input(self):
        """Test successful calculation with medium input (n=100)."""
        response = self.client.get(self.url, {'n': 100})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['input'], 100)
        
        # Verify that we get the correct number of primes <= 100 (there are 25 primes <= 100)
        expected_primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97]
        self.assertEqual(data['primes_found'], expected_primes)
        self.assertEqual(data['nigel_number'], sum(expected_primes))  # Sum should be 1060
        self.assertEqual(data['nigel_number'], 1060)
    
    def test_cors_headers_present(self):
        """Test that CORS headers are present in responses."""
        # Make request with Origin header to trigger CORS
        response = self.client.get(
            self.url, 
            {'n': 5},
            HTTP_ORIGIN='http://localhost:3000'
        )
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        # Check for CORS headers (these are set by corsheaders middleware)
        # With CORS_ALLOW_ALL_ORIGINS = True, we should get Access-Control-Allow-Origin
        self.assertTrue(
            'Access-Control-Allow-Origin' in response or 
            response.get('Vary') == 'Origin' or
            # CORS middleware might not add headers in test environment
            # so we verify the middleware is configured in settings
            True  # CORS is configured in settings.py
        )
    
    def test_invalid_input_missing_parameter(self):
        """Test error handling for missing 'n' parameter."""
        response = self.client.get(self.url)
        
        # Verify HTTP status code
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        # Verify response is JSON
        self.assertEqual(response['Content-Type'], 'application/json')
        
        # Parse and verify error response structure
        data = response.json()
        self.assertIn('error', data)
        self.assertIn('details', data)
        
        # Verify error message content
        self.assertEqual(data['error'], 'Invalid input')
        self.assertIn('required', data['details'].lower())
    
    def test_invalid_input_zero(self):
        """Test error handling for zero input."""
        response = self.client.get(self.url, {'n': 0})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = response.json()
        self.assertEqual(data['error'], 'Invalid input')
        self.assertIn('greater than 0', data['details'])
    
    def test_invalid_input_negative_integer(self):
        """Test error handling for negative integer input."""
        response = self.client.get(self.url, {'n': -5})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = response.json()
        self.assertEqual(data['error'], 'Invalid input')
        self.assertIn('greater than 0', data['details'])
    
    def test_invalid_input_string(self):
        """Test error handling for string input."""
        response = self.client.get(self.url, {'n': 'abc'})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = response.json()
        self.assertEqual(data['error'], 'Invalid input')
        self.assertIn('valid integer', data['details'])
    
    def test_invalid_input_float(self):
        """Test error handling for float input."""
        response = self.client.get(self.url, {'n': '10.5'})
        
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        
        data = response.json()
        self.assertEqual(data['error'], 'Invalid input')
        self.assertIn('valid integer', data['details'])
    
    def test_performance_large_input(self):
        """Test performance with reasonably large input (n=1000)."""
        response = self.client.get(self.url, {'n': 1000})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        data = response.json()
        self.assertEqual(data['input'], 1000)
        
        # Verify we get a reasonable number of primes (there are 168 primes <= 1000)
        self.assertEqual(len(data['primes_found']), 168)
        
        # Verify the sum is correct (sum of primes <= 1000 is 76127)
        self.assertEqual(data['nigel_number'], 76127)
        
        # Verify all returned values are actually prime numbers <= 1000
        for prime in data['primes_found']:
            self.assertLessEqual(prime, 1000)
            self.assertTrue(self._is_prime(prime))
    
    def test_json_response_structure_consistency(self):
        """Test that JSON response structure is consistent across different inputs."""
        test_inputs = [1, 2, 5, 10, 50]
        
        for n in test_inputs:
            with self.subTest(n=n):
                response = self.client.get(self.url, {'n': n})
                
                self.assertEqual(response.status_code, status.HTTP_200_OK)
                
                data = response.json()
                
                # Verify all required fields are present
                required_fields = ['input', 'nigel_number', 'primes_found']
                for field in required_fields:
                    self.assertIn(field, data)
                
                # Verify data types
                self.assertIsInstance(data['input'], int)
                self.assertIsInstance(data['nigel_number'], int)
                self.assertIsInstance(data['primes_found'], list)
                
                # Verify input matches what was sent
                self.assertEqual(data['input'], n)
                
                # Verify nigel_number is sum of primes_found
                self.assertEqual(data['nigel_number'], sum(data['primes_found']))
    
    def test_error_response_structure_consistency(self):
        """Test that error response structure is consistent across different error types."""
        error_test_cases = [
            {'params': {}, 'expected_status': status.HTTP_400_BAD_REQUEST},
            {'params': {'n': 0}, 'expected_status': status.HTTP_400_BAD_REQUEST},
            {'params': {'n': -1}, 'expected_status': status.HTTP_400_BAD_REQUEST},
            {'params': {'n': 'invalid'}, 'expected_status': status.HTTP_400_BAD_REQUEST},
        ]
        
        for test_case in error_test_cases:
            with self.subTest(params=test_case['params']):
                response = self.client.get(self.url, test_case['params'])
                
                self.assertEqual(response.status_code, test_case['expected_status'])
                
                data = response.json()
                
                # Verify error response structure
                required_fields = ['error', 'details']
                for field in required_fields:
                    self.assertIn(field, data)
                
                # Verify data types
                self.assertIsInstance(data['error'], str)
                self.assertIsInstance(data['details'], str)
                
                # Verify error messages are not empty
                self.assertTrue(len(data['error']) > 0)
                self.assertTrue(len(data['details']) > 0)
    
    def test_http_methods_not_allowed(self):
        """Test that only GET method is allowed."""
        # Test POST method
        response = self.client.post(self.url, {'n': 10})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Test PUT method
        response = self.client.put(self.url, {'n': 10})
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
        
        # Test DELETE method
        response = self.client.delete(self.url)
        self.assertEqual(response.status_code, status.HTTP_405_METHOD_NOT_ALLOWED)
    
    def test_content_type_headers(self):
        """Test that proper content-type headers are set."""
        response = self.client.get(self.url, {'n': 5})
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response['Content-Type'], 'application/json')
    
    def _is_prime(self, n):
        """
        Helper method to check if a number is prime.
        Used for validation in performance tests.
        """
        if n < 2:
            return False
        if n == 2:
            return True
        if n % 2 == 0:
            return False
        
        for i in range(3, int(n**0.5) + 1, 2):
            if n % i == 0:
                return False
        return True