#!/usr/bin/env python3
"""
Script to create an admin user with pre-defined credentials
Run with: python create_admin.py
"""
import os
import sys
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Add the app to the path
sys.path.insert(0, os.path.dirname(__file__))

from app import create_app, db
from app.models import User

def create_admin_user():
    """Create an admin user with pre-defined credentials"""
    app = create_app()
    
    with app.app_context():
        # Admin credentials
        ADMIN_EMAIL = "admin@example1.com"
        ADMIN_PASSWORD = "Admin@12345678"
        ADMIN_NAME = "System Administrator"
        
        # Check if admin user already exists
        existing_admin = User.query.filter_by(email=ADMIN_EMAIL).first()
        if existing_admin:
            print(f"❌ Admin user already exists with email: {ADMIN_EMAIL}")
            print(f"\n📋 Existing Admin Credentials:")
            print(f"   Email: {ADMIN_EMAIL}")
            print(f"   Role: {existing_admin.role}")
            print(f"   Status: {existing_admin.status}")
            return
        
        # Create new admin user
        admin = User(
            email=ADMIN_EMAIL,
            full_name=ADMIN_NAME,
            role='admin',
            status='active'
        )
        admin.set_password(ADMIN_PASSWORD)
        
        db.session.add(admin)
        db.session.commit()
        
        print("✅ Admin user created successfully!")
        print(f"\n📋 Admin Login Credentials:")
        print(f"   Email: {ADMIN_EMAIL}")
        print(f"   Password: {ADMIN_PASSWORD}")
        print(f"   Role: admin")
        print(f"\n🌐 You can now login at: http://localhost:5173/login")

if __name__ == '__main__':
    create_admin_user()
