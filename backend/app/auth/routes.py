from flask import Blueprint, request, jsonify, g
from app import db
from app.models import User
from app.auth.utils import validate_email, validate_password_strength, validate_required_fields
from datetime import datetime

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('/signup', methods=['POST'])
def signup():
    """User signup endpoint"""
    data = request.get_json()
    
    # Validate required fields
    is_valid, missing_fields = validate_required_fields(data, ['email', 'password', 'full_name'])
    if not is_valid:
        return jsonify({
            'error': 'Bad Request',
            'message': f'Missing required fields: {", ".join(missing_fields)}',
            'status': 400
        }), 400
    
    email = data['email'].lower().strip()
    password = data['password']
    full_name = data['full_name'].strip()
    
    # Validate email format
    is_valid, error_msg = validate_email(email)
    if not is_valid:
        return jsonify({
            'error': 'Bad Request',
            'message': f'Invalid email: {error_msg}',
            'status': 400
        }), 400
    
    # Check if email already exists
    if User.query.filter_by(email=email).first():
        return jsonify({
            'error': 'Bad Request',
            'message': 'Email already registered',
            'status': 400
        }), 400
    
    # Validate password strength
    is_valid, error_msg = validate_password_strength(password)
    if not is_valid:
        return jsonify({
            'error': 'Bad Request',
            'message': error_msg,
            'status': 400
        }), 400
    
    # Create new user
    user = User(
        email=email,
        full_name=full_name,
        role='user',  # Default role
        status='active'
    )
    user.set_password(password)
    
    try:
        db.session.add(user)
        db.session.commit()
        
        # Generate token
        token = user.generate_token()
        
        return jsonify({
            'token': token,
            'user': user.to_dict()
        }), 201
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to create user',
            'status': 500
        }), 500


@auth_bp.route('/login', methods=['POST'])
def login():
    """User login endpoint"""
    data = request.get_json()
    
    # Validate required fields
    is_valid, missing_fields = validate_required_fields(data, ['email', 'password'])
    if not is_valid:
        return jsonify({
            'error': 'Bad Request',
            'message': f'Missing required fields: {", ".join(missing_fields)}',
            'status': 400
        }), 400
    
    email = data['email'].lower().strip()
    password = data['password']
    
    # Find user by email
    user = User.query.filter_by(email=email).first()
    
    # Verify credentials
    if not user or not user.check_password(password):
        return jsonify({
            'error': 'Unauthorized',
            'message': 'Invalid email or password',
            'status': 401
        }), 401
    
    # Update last login
    user.last_login = datetime.utcnow()
    db.session.commit()
    
    # Generate token
    token = user.generate_token()
    
    return jsonify({
        'token': token,
        'user': user.to_dict(include_timestamps=True)
    }), 200


@auth_bp.route('/logout', methods=['POST'])
def logout():
    """User logout endpoint (client-side token deletion)"""
    # In JWT-based auth, logout is typically handled client-side
    # by deleting the token. For enhanced security, you could
    # implement a token blacklist here.
    
    return jsonify({
        'message': 'Logged out successfully'
    }), 200


@auth_bp.route('/me', methods=['GET'])
def get_current_user():
    """Get current user information from token"""
    from app.users.decorators import token_required
    
    @token_required
    def _get_current_user():
        return jsonify(g.current_user.to_dict(include_timestamps=True)), 200
    
    return _get_current_user()
