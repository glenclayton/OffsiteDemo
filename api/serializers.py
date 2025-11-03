"""
Serializers for the Nigel Number API.
"""
from rest_framework import serializers


class NigelNumberInputSerializer(serializers.Serializer):
    """
    Serializer for validating input to the Nigel Number API endpoint.
    Ensures the input 'n' is a positive integer.
    """
    n = serializers.IntegerField(
        required=True,
        help_text="A positive integer for which to calculate the Nigel Number"
    )
    
    def validate_n(self, value):
        """
        Custom validation method for positive integer checking.
        
        Args:
            value: The integer value to validate
            
        Returns:
            int: The validated positive integer
            
        Raises:
            serializers.ValidationError: If the value is not positive
        """
        if value <= 0:
            raise serializers.ValidationError(
                "Parameter 'n' must be greater than 0"
            )
        return value


class NigelNumberResponseSerializer(serializers.Serializer):
    """
    Serializer for structuring the JSON response from the Nigel Number API.
    """
    input = serializers.IntegerField(
        help_text="The original input value"
    )
    nigel_number = serializers.IntegerField(
        help_text="The calculated sum of all prime numbers less than or equal to the input"
    )
    primes_found = serializers.ListField(
        child=serializers.IntegerField(),
        help_text="List of prime numbers found that are less than or equal to the input"
    )


class ErrorResponseSerializer(serializers.Serializer):
    """
    Serializer for formatting error messages in API responses.
    """
    error = serializers.CharField(
        help_text="Brief error message describing the issue"
    )
    details = serializers.CharField(
        help_text="Additional details about the error"
    )