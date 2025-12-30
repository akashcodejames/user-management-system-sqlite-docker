#!/usr/bin/env python3
"""
Secret Key Generator

Generates a secure random secret key for Flask applications.
Use this to generate SECRET_KEY and JWT_SECRET_KEY for production.

Usage:
    python generate_secret_key.py
    
This will generate two secure random keys that you can use in your .env file.
"""

import secrets
import string


def generate_secret_key(length=64):
    """
    Generate a cryptographically secure random secret key.
    
    Args:
        length (int): Length of the secret key (default: 64)
    
    Returns:
        str: A secure random string
    """
    alphabet = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(alphabet) for _ in range(length))


if __name__ == '__main__':
    print("=" * 80)
    print("🔐 SECRET KEY GENERATOR")
    print("=" * 80)
    print()
    print("Copy these keys to your production environment variables:")
    print()
    print("-" * 80)
    print("SECRET_KEY:")
    print(generate_secret_key())
    print()
    print("-" * 80)
    print("JWT_SECRET_KEY:")
    print(generate_secret_key())
    print()
    print("-" * 80)
    print()
    print("⚠️  IMPORTANT:")
    print("  - Store these keys securely")
    print("  - Never commit these to version control")
    print("  - Use different keys for different environments")
    print("  - Save these immediately - they won't be shown again")
    print()
    print("=" * 80)
