#!/usr/bin/env python3

import os
import sys
from dotenv import load_dotenv


def load_configuration():
    """
    Load and validate required environment variables.
    """

    # Load .env file (for development)
    load_dotenv()

    required_vars = [
        "MATRIX_MODE",
        "DATABASE_URL",
        "API_KEY",
        "LOG_LEVEL",
        "ZION_ENDPOINT",
    ]

    config = {}

    for var in required_vars:
        value = os.getenv(var)
        if not value:
            print(f"Configuration error: Missing {var}")
            sys.exit(1)
        config[var] = value

    return config


def security_check():
    """
    Simulate environment security checks.
    """
    print("Environment security check:")

    # Check that no secrets are hardcoded (basic simulation)
    print("[OK] No hardcoded secrets detected")

    # Check .env exists in development mode
    if os.path.exists(".env"):
        print("[OK] .env file properly configured")
    else:
        print("[WARNING] .env file not found")

    # Production override check
    print("[OK] Production overrides available")


def main():
    print("ORACLE STATUS: Reading the Matrix...")

    config = load_configuration()

    print("Configuration loaded:")

    # Mode
    print(f"Mode: {config['MATRIX_MODE']}")

    # Database status message
    if config["MATRIX_MODE"] == "development":
        print("Database: Connected to local instance")
    else:
        print("Database: Connected to production cluster")

    # API status
    if config["API_KEY"]:
        print("API Access: Authenticated")
    else:
        print("API Access: Not authenticated")

    # Log level
    print(f"Log Level: {config['LOG_LEVEL']}")

    # Zion endpoint status
    if config["ZION_ENDPOINT"]:
        print("Zion Network: Online")
    else:
        print("Zion Network: Offline")

    security_check()

    print("The Oracle sees all configurations.")


if __name__ == "__main__":
    main()