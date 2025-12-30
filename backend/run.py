#!/usr/bin/env python3
"""
Application entry point
Run with: python run.py
"""
import os
from dotenv import load_dotenv
from app import create_app, db
from app.models import User

# Load environment variables
load_dotenv()

# Create Flask app
app = create_app()


@app.shell_context_processor
def make_shell_context():
    """Make database and models available in Flask shell"""
    return {'db': db, 'User': User}


@app.cli.command()
def create_admin():
    """Create an admin user"""
    email = input("Enter admin email: ")
    password = input("Enter admin password: ")
    full_name = input("Enter admin full name: ")
    
    # Check if user exists
    if User.query.filter_by(email=email).first():
        print("Error: Email already exists")
        return
    
    # Create admin user
    admin = User(
        email=email,
        full_name=full_name,
        role='admin',
        status='active'
    )
    admin.set_password(password)
    
    db.session.add(admin)
    db.session.commit()
    
    print(f"Admin user created successfully: {email}")


if __name__ == '__main__':
    # Tables should be created manually or via flask db upgrade
    # Uncomment below to create tables on first run:
    # with app.app_context():
    #     db.create_all()
    #     print("Database tables created")
    
    # Run the application
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])
