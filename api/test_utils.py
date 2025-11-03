"""
Unit tests for prime number calculation utilities.
"""

import pytest
from .utils import calculate_nigel_number, sieve_of_eratosthenes


class TestSieveOfEratosthenes:
    """Test cases for the Sieve of Eratosthenes algorithm."""
    
    def test_sieve_empty_for_n_less_than_2(self):
        """Test that sieve returns empty list for n < 2."""
        assert sieve_of_eratosthenes(0) == []
        assert sieve_of_eratosthenes(1) == []
    
    def test_sieve_small_numbers(self):
        """Test sieve with small numbers."""
        assert sieve_of_eratosthenes(2) == [2]
        assert sieve_of_eratosthenes(3) == [2, 3]
        assert sieve_of_eratosthenes(5) == [2, 3, 5]
        assert sieve_of_eratosthenes(10) == [2, 3, 5, 7]
    
    def test_sieve_larger_numbers(self):
        """Test sieve with larger numbers."""
        primes_20 = sieve_of_eratosthenes(20)
        expected_20 = [2, 3, 5, 7, 11, 13, 17, 19]
        assert primes_20 == expected_20
        
        primes_30 = sieve_of_eratosthenes(30)
        expected_30 = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29]
        assert primes_30 == expected_30


class TestCalculateNigelNumber:
    """Test cases for the Nigel Number calculation."""
    
    def test_edge_case_n_equals_1(self):
        """Test that N=1 returns sum=0 and empty primes list."""
        result = calculate_nigel_number(1)
        assert result == {"sum": 0, "primes": []}
    
    def test_edge_case_n_equals_2(self):
        """Test that N=2 returns sum=2 and primes=[2]."""
        result = calculate_nigel_number(2)
        assert result == {"sum": 2, "primes": [2]}
    
    def test_small_numbers(self):
        """Test Nigel Number calculation for small numbers."""
        # N=3: primes=[2, 3], sum=5
        result = calculate_nigel_number(3)
        assert result == {"sum": 5, "primes": [2, 3]}
        
        # N=10: primes=[2, 3, 5, 7], sum=17
        result = calculate_nigel_number(10)
        assert result == {"sum": 17, "primes": [2, 3, 5, 7]}
    
    def test_larger_numbers(self):
        """Test Nigel Number calculation for larger numbers."""
        # N=20: primes=[2, 3, 5, 7, 11, 13, 17, 19], sum=77
        result = calculate_nigel_number(20)
        expected_primes = [2, 3, 5, 7, 11, 13, 17, 19]
        expected_sum = sum(expected_primes)
        assert result == {"sum": expected_sum, "primes": expected_primes}
        assert result["sum"] == 77
    
    def test_return_structure(self):
        """Test that the return structure is correct."""
        result = calculate_nigel_number(10)
        assert isinstance(result, dict)
        assert "sum" in result
        assert "primes" in result
        assert isinstance(result["sum"], int)
        assert isinstance(result["primes"], list)
        assert all(isinstance(p, int) for p in result["primes"])
    
    def test_invalid_input_zero(self):
        """Test that N=0 raises ValueError."""
        with pytest.raises(ValueError, match="Input must be a positive integer"):
            calculate_nigel_number(0)
    
    def test_invalid_input_negative(self):
        """Test that negative numbers raise ValueError."""
        with pytest.raises(ValueError, match="Input must be a positive integer"):
            calculate_nigel_number(-1)
        with pytest.raises(ValueError, match="Input must be a positive integer"):
            calculate_nigel_number(-10)
    
    def test_invalid_input_non_integer(self):
        """Test that non-integer inputs raise ValueError."""
        with pytest.raises(ValueError, match="Input must be a positive integer"):
            calculate_nigel_number("10")
        with pytest.raises(ValueError, match="Input must be a positive integer"):
            calculate_nigel_number(10.5)
        with pytest.raises(ValueError, match="Input must be a positive integer"):
            calculate_nigel_number(None)
    
    def test_performance_large_number(self):
        """Test performance with a reasonably large number."""
        import time
        start_time = time.time()
        result = calculate_nigel_number(1000)
        end_time = time.time()
        
        # Should complete in reasonable time (less than 1 second)
        assert end_time - start_time < 1.0
        
        # Verify the result is correct
        assert isinstance(result["sum"], int)
        assert isinstance(result["primes"], list)
        assert len(result["primes"]) == 168  # There are 168 primes <= 1000
        assert result["sum"] == 76127  # Sum of primes <= 1000