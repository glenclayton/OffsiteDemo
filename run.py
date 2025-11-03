#!/usr/bin/env python
"""
Main startup script for the Nigel Number API server.

This script provides a convenient way to start the Django development server
with configurable options for host, port, debug mode, and automatic database
migrations.
"""

import argparse
import logging
import os
import sys
import subprocess
from pathlib import Path


def setup_logging(debug=False):
    """Configure logging for server startup and shutdown."""
    log_level = logging.DEBUG if debug else logging.INFO
    logging.basicConfig(
        level=log_level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        handlers=[
            logging.StreamHandler(sys.stdout)
        ]
    )
    return logging.getLogger('nigel_api_server')


def check_django_installation():
    """Check if Django is properly installed."""
    try:
        import django
        return True
    except ImportError:
        return False


def run_migrations(logger):
    """Run Django database migrations automatically."""
    logger.info("Running database migrations...")
    try:
        # Set Django settings module
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nigel_api.settings')
        
        # Run migrations
        result = subprocess.run([
            sys.executable, 'manage.py', 'migrate', '--verbosity=1'
        ], capture_output=True, text=True, check=True)
        
        logger.info("Database migrations completed successfully")
        if result.stdout:
            logger.debug(f"Migration output: {result.stdout}")
        return True
        
    except subprocess.CalledProcessError as e:
        logger.error(f"Migration failed: {e}")
        if e.stdout:
            logger.error(f"Migration stdout: {e.stdout}")
        if e.stderr:
            logger.error(f"Migration stderr: {e.stderr}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error during migration: {e}")
        return False


def start_server(host, port, debug, logger):
    """Start the Django development server."""
    logger.info(f"Starting Nigel Number API server on {host}:{port}")
    logger.info(f"Debug mode: {'enabled' if debug else 'disabled'}")
    
    try:
        # Set environment variables
        os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'nigel_api.settings')
        if debug:
            os.environ['DJANGO_DEBUG'] = 'True'
        
        # Build runserver command
        cmd = [sys.executable, 'manage.py', 'runserver', f'{host}:{port}']
        
        logger.info("Server starting... Press Ctrl+C to stop")
        logger.info(f"API endpoint will be available at: http://{host}:{port}/api/nigel-number/")
        
        # Start the server
        subprocess.run(cmd, check=True)
        
    except KeyboardInterrupt:
        logger.info("Server shutdown requested by user")
    except subprocess.CalledProcessError as e:
        logger.error(f"Server failed to start: {e}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error starting server: {e}")
        return False
    finally:
        logger.info("Server shutdown complete")
    
    return True


def parse_arguments():
    """Parse command-line arguments."""
    parser = argparse.ArgumentParser(
        description='Start the Nigel Number API server',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python run.py                          # Start with default settings
  python run.py --host 0.0.0.0          # Allow external connections
  python run.py --port 9000             # Use custom port
  python run.py --debug                 # Enable debug mode
  python run.py --no-migrate            # Skip automatic migrations
  
Environment Variables:
  NIGEL_API_HOST     - Default host (default: 127.0.0.1)
  NIGEL_API_PORT     - Default port (default: 8000)
  NIGEL_API_DEBUG    - Enable debug mode (default: False)
  DJANGO_SETTINGS_MODULE - Django settings module
        """
    )
    
    parser.add_argument(
        '--host',
        default=os.getenv('NIGEL_API_HOST', '127.0.0.1'),
        help='Host to bind the server to (default: 127.0.0.1)'
    )
    
    parser.add_argument(
        '--port',
        type=int,
        default=int(os.getenv('NIGEL_API_PORT', '8000')),
        help='Port to bind the server to (default: 8000)'
    )
    
    parser.add_argument(
        '--debug',
        action='store_true',
        default=os.getenv('NIGEL_API_DEBUG', '').lower() in ('true', '1', 'yes'),
        help='Enable debug mode (default: False)'
    )
    
    parser.add_argument(
        '--no-migrate',
        action='store_true',
        help='Skip automatic database migrations'
    )
    
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose logging'
    )
    
    return parser.parse_args()


def validate_arguments(args, logger):
    """Validate command-line arguments."""
    # Validate port range
    if not (1 <= args.port <= 65535):
        logger.error(f"Invalid port number: {args.port}. Must be between 1 and 65535.")
        return False
    
    # Validate host format (basic check)
    if not args.host:
        logger.error("Host cannot be empty")
        return False
    
    return True


def check_project_structure():
    """Check if we're in a valid Django project directory."""
    required_files = ['manage.py', 'nigel_api/settings.py']
    for file_path in required_files:
        if not Path(file_path).exists():
            return False, f"Missing required file: {file_path}"
    return True, None


def main():
    """Main entry point for the server startup script."""
    # Parse command-line arguments
    args = parse_arguments()
    
    # Setup logging
    logger = setup_logging(debug=args.debug or args.verbose)
    
    try:
        logger.info("Nigel Number API Server Startup")
        logger.info("=" * 40)
        
        # Check project structure
        is_valid, error_msg = check_project_structure()
        if not is_valid:
            logger.error(f"Invalid project structure: {error_msg}")
            logger.error("Please run this script from the project root directory")
            sys.exit(1)
        
        # Validate arguments
        if not validate_arguments(args, logger):
            sys.exit(1)
        
        # Check Django installation
        if not check_django_installation():
            logger.error("Django is not installed or not available")
            logger.error("Please install dependencies: pip install -r requirements.txt")
            sys.exit(1)
        
        # Run migrations unless skipped
        if not args.no_migrate:
            if not run_migrations(logger):
                logger.error("Failed to run database migrations")
                logger.error("Use --no-migrate to skip migrations or fix the database issues")
                sys.exit(1)
        else:
            logger.info("Skipping database migrations (--no-migrate flag used)")
        
        # Start the server
        success = start_server(args.host, args.port, args.debug, logger)
        
        if not success:
            sys.exit(1)
            
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        if args.debug or args.verbose:
            logger.exception("Full traceback:")
        sys.exit(1)


if __name__ == '__main__':
    main()