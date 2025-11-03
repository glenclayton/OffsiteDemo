from django.test import TestCase
from rest_framework import serializers
from .serializers import NigelNumberInputSerializer, NigelNumberResponseSerializer, ErrorResponseSerializer


class TestNigelNumberInputSerializer(TestCase):
    """Test cases for the NigelNumberInputSerializer."""
    
    def test_valid_positive_integer(self):
        """Test that valid positive integers pass validation."""
        serializer = NigelNumberInputSerializer(data={'n': 10})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['n'], 10)
        
        serializer = NigelNumberInputSerializer(data={'n': 1})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['n'], 1)
        
        serializer = NigelNumberInputSerializer(data={'n': 1000})
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data['n'], 1000)
    
    def test_invalid_zero(self):
        """Test that zero fails validation."""
        serializer = NigelNumberInputSerializer(data={'n': 0})
        self.assertFalse(serializer.is_valid())
        self.assertIn('n', serializer.errors)
        self.assertEqual(
            serializer.errors['n'][0], 
            "Parameter 'n' must be greater than 0"
        )
    
    def test_invalid_negative_integer(self):
        """Test that negative integers fail validation."""
        serializer = NigelNumberInputSerializer(data={'n': -5})
        self.assertFalse(serializer.is_valid())
        self.assertIn('n', serializer.errors)
        self.assertEqual(
            serializer.errors['n'][0], 
            "Parameter 'n' must be greater than 0"
        )
    
    def test_missing_parameter(self):
        """Test that missing 'n' parameter fails validation."""
        serializer = NigelNumberInputSerializer(data={})
        self.assertFalse(serializer.is_valid())
        self.assertIn('n', serializer.errors)
        self.assertEqual(serializer.errors['n'][0], "This field is required.")
    
    def test_invalid_string_input(self):
        """Test that string inputs fail validation."""
        serializer = NigelNumberInputSerializer(data={'n': 'abc'})
        self.assertFalse(serializer.is_valid())
        self.assertIn('n', serializer.errors)
        self.assertEqual(serializer.errors['n'][0], "A valid integer is required.")
    
    def test_invalid_float_input(self):
        """Test that float inputs fail validation."""
        serializer = NigelNumberInputSerializer(data={'n': 10.5})
        self.assertFalse(serializer.is_valid())
        self.assertIn('n', serializer.errors)
        self.assertEqual(serializer.errors['n'][0], "A valid integer is required.")


class TestNigelNumberResponseSerializer(TestCase):
    """Test cases for the NigelNumberResponseSerializer."""
    
    def test_valid_response_data(self):
        """Test serialization of valid response data."""
        data = {
            'input': 10,
            'nigel_number': 17,
            'primes_found': [2, 3, 5, 7]
        }
        serializer = NigelNumberResponseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, data)
    
    def test_serialization_output(self):
        """Test that serializer produces correct output."""
        data = {
            'input': 5,
            'nigel_number': 10,
            'primes_found': [2, 3, 5]
        }
        serializer = NigelNumberResponseSerializer(data)
        expected_output = {
            'input': 5,
            'nigel_number': 10,
            'primes_found': [2, 3, 5]
        }
        self.assertEqual(serializer.data, expected_output)
    
    def test_empty_primes_list(self):
        """Test serialization with empty primes list (N=1 case)."""
        data = {
            'input': 1,
            'nigel_number': 0,
            'primes_found': []
        }
        serializer = NigelNumberResponseSerializer(data)
        self.assertEqual(serializer.data, data)


class TestErrorResponseSerializer(TestCase):
    """Test cases for the ErrorResponseSerializer."""
    
    def test_error_response_serialization(self):
        """Test serialization of error response data."""
        data = {
            'error': 'Invalid input value',
            'details': "Parameter 'n' must be greater than 0"
        }
        serializer = ErrorResponseSerializer(data)
        self.assertEqual(serializer.data, data)
    
    def test_validation_error_format(self):
        """Test that error response follows expected format."""
        data = {
            'error': 'Missing required parameter',
            'details': "Parameter 'n' is required"
        }
        serializer = ErrorResponseSerializer(data=data)
        self.assertTrue(serializer.is_valid())
        self.assertEqual(serializer.validated_data, data)
