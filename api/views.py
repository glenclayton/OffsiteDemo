"""
API views for the Nigel Number API.
"""
import logging
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import Http404

from .serializers import (
    NigelNumberInputSerializer, 
    NigelNumberResponseSerializer, 
    ErrorResponseSerializer
)
from .utils import calculate_nigel_number

# Set up logging for this module
logger = logging.getLogger('api')


class NigelNumberAPIView(APIView):
    """
    API view for calculating the Nigel Number.
    
    Handles GET requests with a positive integer parameter 'n' and returns
    the calculated Nigel Number (sum of all primes <= n) along with the
    list of primes found.
    """
    
    def get(self, request):
        """
        Handle GET request for Nigel Number calculation.
        
        Query Parameters:
            n (int): A positive integer for which to calculate the Nigel Number
            
        Returns:
            Response: JSON response with calculated Nigel Number or error message
        """
        try:
            # Log the incoming request
            client_ip = self.get_client_ip(request)
            logger.info(f"Nigel Number calculation request from {client_ip}, params: {request.query_params}")
            
            # Validate input using serializer
            input_serializer = NigelNumberInputSerializer(data=request.query_params)
            
            if not input_serializer.is_valid():
                # Handle validation errors
                error_details = self._format_validation_errors(input_serializer.errors)
                logger.warning(f"Invalid input from {client_ip}: {error_details}")
                
                error_response = ErrorResponseSerializer({
                    'error': 'Invalid input',
                    'details': error_details
                })
                
                return Response(
                    error_response.data,
                    status=status.HTTP_400_BAD_REQUEST
                )
            
            # Extract validated input
            n = input_serializer.validated_data['n']
            
            # Calculate Nigel Number using utility function
            try:
                result = calculate_nigel_number(n)
                
                # Structure the response data
                response_data = {
                    'input': n,
                    'nigel_number': result['sum'],
                    'primes_found': result['primes']
                }
                
                # Validate response structure
                response_serializer = NigelNumberResponseSerializer(response_data)
                
                # Log successful calculation
                logger.info(f"Successful calculation for n={n}: Nigel Number={result['sum']}, Primes count={len(result['primes'])}")
                
                return Response(
                    response_serializer.data,
                    status=status.HTTP_200_OK
                )
                
            except ValueError as e:
                # Handle calculation errors (should not happen with validated input)
                logger.error(f"Calculation error for n={n}: {str(e)}")
                
                error_response = ErrorResponseSerializer({
                    'error': 'Calculation error',
                    'details': str(e)
                })
                
                return Response(
                    error_response.data,
                    status=status.HTTP_400_BAD_REQUEST
                )
                
        except Exception as e:
            # Handle unexpected server errors
            logger.error(f"Unexpected error in Nigel Number calculation: {str(e)}", exc_info=True)
            
            error_response = ErrorResponseSerializer({
                'error': 'Internal server error',
                'details': 'An unexpected error occurred during calculation'
            })
            
            return Response(
                error_response.data,
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
    def get_client_ip(self, request):
        """
        Get the client IP address from the request.
        
        Args:
            request: Django request object
            
        Returns:
            str: Client IP address
        """
        x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
        if x_forwarded_for:
            ip = x_forwarded_for.split(',')[0]
        else:
            ip = request.META.get('REMOTE_ADDR')
        return ip
    
    def _format_validation_errors(self, errors):
        """
        Format validation errors into a readable string.
        
        Args:
            errors (dict): Validation errors from serializer
            
        Returns:
            str: Formatted error message
        """
        if 'n' not in errors:
            return "Missing required parameter 'n'"
        
        error_messages = errors['n']
        if isinstance(error_messages, list) and error_messages:
            return error_messages[0]
        
        return "Invalid parameter 'n'"
