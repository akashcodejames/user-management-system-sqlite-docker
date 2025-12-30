#!/usr/bin/env bash
# Build script for Render deployment

# Exit on error
set -o errexit

# Install dependencies
pip install --upgrade pip
pip install -r requirements.txt

# Run database migrations
flask db upgrade
