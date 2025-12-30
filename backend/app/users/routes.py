from flask import Blueprint, request, jsonify, g
from app import db
from app.models import User
from app.users.decorators import token_required, active_user_required
from app.auth.utils import validate_email, validate_password_strength

users_bp = Blueprint('users', __name__)


@users_bp.route('/profile', methods=['GET'])
@token_required
@active_user_required
def get_profile():
    """Get current user's profile"""
    return jsonify(g.current_user.to_dict(include_timestamps=True)), 200


@users_bp.route('/profile', methods=['PUT'])
@token_required
@active_user_required
def update_profile():
    """Update current user's profile (name and email)"""
    data = request.get_json()
    
    if not data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'No data provided',
            'status': 400
        }), 400
    
    user = g.current_user
    updated = False
    
    # Update full name
    if 'full_name' in data:
        full_name = data['full_name'].strip()
        if not full_name:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Full name cannot be empty',
                'status': 400
            }), 400
        user.full_name = full_name
        updated = True
    
    # Update email
    if 'email' in data:
        email = data['email'].lower().strip()
        
        # Validate email format
        is_valid, error_msg = validate_email(email)
        if not is_valid:
            return jsonify({
                'error': 'Bad Request',
                'message': f'Invalid email: {error_msg}',
                'status': 400
            }), 400
        
        # Check if email is already taken by another user
        existing_user = User.query.filter_by(email=email).first()
        if existing_user and existing_user.id != user.id:
            return jsonify({
                'error': 'Bad Request',
                'message': 'Email already in use',
                'status': 400
            }), 400
        
        user.email = email
        updated = True
    
    if not updated:
        return jsonify({
            'error': 'Bad Request',
            'message': 'No valid fields to update',
            'status': 400
        }), 400
    
    try:
        db.session.commit()
        return jsonify(user.to_dict(include_timestamps=True)), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to update profile',
            'status': 500
        }), 500


@users_bp.route('/password', methods=['PUT'])
@token_required
@active_user_required
def change_password():
    """Change user's password"""
    data = request.get_json()
    
    # Validate required fields
    if not data or 'current_password' not in data or 'new_password' not in data:
        return jsonify({
            'error': 'Bad Request',
            'message': 'Current password and new password are required',
            'status': 400
        }), 400
    
    user = g.current_user
    current_password = data['current_password']
    new_password = data['new_password']
    
    # Verify current password
    if not user.check_password(current_password):
        return jsonify({
            'error': 'Bad Request',
            'message': 'Current password is incorrect',
            'status': 400
        }), 400
    
    # Validate new password strength
    is_valid, error_msg = validate_password_strength(new_password)
    if not is_valid:
        return jsonify({
            'error': 'Bad Request',
            'message': error_msg,
            'status': 400
        }), 400
    
    # Update password
    user.set_password(new_password)
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'Password updated successfully'
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to update password',
            'status': 500
        }), 500
