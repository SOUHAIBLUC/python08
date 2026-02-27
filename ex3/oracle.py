#!/usr/bin/env python3
"""
Exercise 02: Accessing the Mainframe - Environment Variables.

This program demonstrates secure configuration management using environment variables.
It shows how to keep sensitive data (API keys, passwords) out of your code.

KEY CONCEPTS:
1. Environment Variables: System-level variables accessible to programs
   - Set in shell: export API_KEY="secret123"
   - Accessed in Python: os.getenv("API_KEY")

2. .env Files: Local files storing environment variables
   - NOT committed to git (in .gitignore)
   - Loaded by python-dotenv library
   - Format: KEY=value

3. Configuration Hierarchy (priority order):
   1. Environment variables (highest priority)
   2. .env file
   3. Default values (fallback)

4. Security Best Practice:
   - NEVER hardcode secrets in code
   - NEVER commit .env files to version control
   - ALWAYS use .env.example (without real secrets) for templates
"""

import os
import sys
from typing import Dict, Optional


def load_env_file(filename: str = ".env") -> Dict[str, str]:
    """
    Load environment variables from a .env file.
    
    HOW .env FILES WORK:
    - Simple text file with KEY=VALUE pairs
    - One variable per line
    - Comments start with #
    - Example:
        # Database configuration
        DATABASE_URL=postgresql://localhost/mydb
        API_KEY=secret123
    
    This is a simplified implementation. In production, use python-dotenv library.
    
    Args:
        filename: Path to .env file
    
    Returns:
        Dictionary of environment variables from file
    """
    env_vars = {}
    
    # Check if file exists
    if not os.path.exists(filename):
        return env_vars
    
    try:
        with open(filename, 'r') as f:
            for line in f:
                # Strip whitespace
                line = line.strip()
                
                # Skip empty lines and comments
                if not line or line.startswith('#'):
                    continue
                
                # Split on first '=' only
                if '=' in line:
                    key, value = line.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    
                    # Remove quotes if present
                    if value.startswith('"') and value.endswith('"'):
                        value = value[1:-1]
                    elif value.startswith("'") and value.endswith("'"):
                        value = value[1:-1]
                    
                    env_vars[key] = value
        
        return env_vars
    
    except Exception as e:
        print(f"Error loading .env file: {e}")
        return env_vars


def get_config_value(key: str, env_vars: Dict[str, str], 
                      default: Optional[str] = None) -> Optional[str]:
    """
    Get configuration value with priority: ENV > .env file > default.
    
    CONFIGURATION HIERARCHY EXPLAINED:
    
    1. Environment variables (highest priority)
       - Set in shell before running program
       - Example: export API_KEY="production_key"
       - Use case: Production servers, CI/CD systems
    
    2. .env file (medium priority)
       - Local development configuration
       - Example: API_KEY=development_key
       - Use case: Local development
    
    3. Default value (lowest priority)
       - Fallback if not set anywhere
       - Use case: Non-sensitive defaults
    
    Args:
        key: Configuration key to look up
        env_vars: Dictionary from .env file
        default: Default value if not found
    
    Returns:
        Configuration value or None
    """
    # Priority 1: Check actual environment variables
    value = os.getenv(key)
    if value is not None:
        return value
    
    # Priority 2: Check .env file
    if key in env_vars:
        return env_vars[key]
    
    # Priority 3: Use default
    return default


class MatrixConfig:
    """
    Configuration manager for The Matrix application.
    
    This class encapsulates all configuration logic and provides
    a clean interface for accessing configuration values.
    """
    
    def __init__(self):
        """Initialize configuration by loading from .env and environment."""
        # Load .env file
        self.env_file_vars = load_env_file(".env")
        
        # Load all configuration values
        self.mode = self._get_value("MATRIX_MODE", "development")
        self.database_url = self._get_value(
            "DATABASE_URL", 
            "sqlite:///local_matrix.db"
        )
        self.api_key = self._get_value("API_KEY")
        self.log_level = self._get_value("LOG_LEVEL", "INFO")
        self.zion_endpoint = self._get_value(
            "ZION_ENDPOINT", 
            "https://localhost:9000"
        )
    
    def _get_value(self, key: str, default: Optional[str] = None) -> Optional[str]:
        """Helper to get config value with hierarchy."""
        return get_config_value(key, self.env_file_vars, default)
    
    def validate(self) -> bool:
        """
        Validate that all required configuration is present.
        
        Returns:
            True if configuration is valid
        """
        # Check for required values
        if self.mode not in ["development", "production"]:
            print(f"ERROR: MATRIX_MODE must be 'development' or 'production', "
                  f"got '{self.mode}'")
            return False
        
        # In production, API key is required
        if self.mode == "production" and not self.api_key:
            print("ERROR: API_KEY is required in production mode")
            return False
        
        return True
    
    def is_production(self) -> bool:
        """Check if running in production mode."""
        return self.mode == "production"
    
    def display_config(self) -> None:
        """Display current configuration (masking secrets)."""
        print("Configuration loaded:")
        print(f"  Mode: {self.mode}")
        
        # Database URL: mask password if present
        db_display = self.database_url
        if "://" in db_display and "@" in db_display:
            # postgresql://user:PASSWORD@host/db → postgresql://user:****@host/db
            protocol, rest = db_display.split("://", 1)
            if "@" in rest:
                credentials, host = rest.split("@", 1)
                if ":" in credentials:
                    user, _ = credentials.split(":", 1)
                    db_display = f"{protocol}://{user}:****@{host}"
        
        print(f"  Database: {db_display}")
        
        # API key: mask if present
        if self.api_key:
            masked_key = self.api_key[:4] + "*" * (len(self.api_key) - 4)
            print(f"  API Access: Authenticated ({masked_key})")
        else:
            print("  API Access: No key configured")
        
        print(f"  Log Level: {self.log_level}")
        print(f"  Zion Network: {self.zion_endpoint}")


def check_security() -> None:
    """
    Perform security checks on the configuration.
    
    SECURITY BEST PRACTICES:
    1. Never hardcode secrets in code
    2. Keep .env out of version control
    3. Use different secrets for dev/prod
    4. Validate configuration on startup
    5. Mask secrets in logs
    """
    print("\nEnvironment security check:")
    
    checks = []
    
    # Check 1: .env file should exist
    if os.path.exists(".env"):
        checks.append(("[OK]", ".env file found"))
    else:
        checks.append(("[WARN]", ".env file not found - using defaults"))
    
    # Check 2: .gitignore should exclude .env
    if os.path.exists(".gitignore"):
        with open(".gitignore", 'r') as f:
            gitignore_content = f.read()
            if ".env" in gitignore_content:
                checks.append(("[OK]", ".env properly excluded from git"))
            else:
                checks.append(("[WARN]", ".env not in .gitignore - add it!"))
    else:
        checks.append(("[WARN]", "No .gitignore found"))
    
    # Check 3: .env.example should exist as template
    if os.path.exists(".env.example"):
        checks.append(("[OK]", ".env.example template available"))
    else:
        checks.append(("[WARN]", "No .env.example found"))
    
    # Print all checks
    for status, message in checks:
        print(f"  {status} {message}")


def main() -> None:
    """
    Main entry point.
    
    PROGRAM FLOW:
    1. Load configuration from env vars and .env file
    2. Validate configuration
    3. Display configuration (masking secrets)
    4. Perform security checks
    """
    print("=" * 60)
    print("THE MATRIX - ACCESSING THE MAINFRAME")
    print("=" * 60)
    print()
    
    print("ORACLE STATUS: Reading the Matrix...")
    print()
    
    # Load configuration
    config = MatrixConfig()
    
    # Validate
    if not config.validate():
        print("\nConfiguration validation failed!")
        sys.exit(1)
    
    # Display configuration
    config.display_config()
    
    # Security checks
    check_security()
    
    print()
    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()
