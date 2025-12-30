from functools import wraps
from flask import request, jsonify, g
from app.models import User


def token_required(f):
    """Decorator to require valid JWT token"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = None
        
        # Get token from Authorization header
        if 'Authorization' in request.headers:
            auth_header = request.headers['Authorization']
            try:
                token = auth_header.split(' ')[1]  # Bearer <token>
            except IndexError:
                return jsonify({
                    'error': 'Unauthorized',
                    'message': 'Invalid authorization header format. Use: Bearer <token>',
                    'status': 401
                }), 401
        
        if not token:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication token is missing',
                'status': 401
            }), 401
        
        # Verify token
        payload = User.verify_token(token)
        if not payload:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Invalid or expired token',
                'status': 401
            }), 401
        
        # Get user from database
        user = User.query.get(payload['user_id'])
        if not user:
            return jsonify({
                'error': 'Unauthorized',
                'message': 'User not found',
                'status': 401
            }), 401
        
        # Store user in request context
        g.current_user = user
        
        return f(*args, **kwargs)
    
    return decorated_function


def admin_required(f):
    """Decorator to require admin role (must be used with @token_required)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'current_user'):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication required',
                'status': 401
            }), 401
        
        if g.current_user.role != 'admin':
            return jsonify({
                'error': 'Forbidden',
                'message': 'Admin role required',
                'status': 403
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function


def active_user_required(f):
    """Decorator to require active user status (must be used with @token_required)"""
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not hasattr(g, 'current_user'):
            return jsonify({
                'error': 'Unauthorized',
                'message': 'Authentication required',
                'status': 401
            }), 401
        
        if g.current_user.status != 'active':
            return jsonify({
                'error': 'Forbidden',
                'message': 'Account is inactive. Please contact administrator.',
                'status': 403
            }), 403
        
        return f(*args, **kwargs)
    
    return decorated_function
