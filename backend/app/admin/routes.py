from flask import Blueprint, request, jsonify, g, current_app
from app import db
from app.models import User
from app.users.decorators import token_required, admin_required

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/users', methods=['GET'])
@token_required
@admin_required
def get_all_users():
    """Get all users with pagination (admin only)"""
    # Get pagination parameters
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', current_app.config['USERS_PER_PAGE'], type=int)
    
    # Limit per_page to prevent abuse
    per_page = min(per_page, 100)
    
    # Query users with pagination
    pagination = User.query.order_by(User.created_at.desc()).paginate(
        page=page,
        per_page=per_page,
        error_out=False
    )
    
    users = pagination.items
    
    return jsonify({
        'users': [user.to_dict(include_timestamps=True) for user in users],
        'total': pagination.total,
        'page': pagination.page,
        'pages': pagination.pages,
        'per_page': per_page
    }), 200


@admin_bp.route('/users/<int:user_id>/activate', methods=['PUT'])
@token_required
@admin_required
def activate_user(user_id):
    """Activate a user account (admin only)"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'error': 'Not Found',
            'message': 'User not found',
            'status': 404
        }), 404
    
    # Check if already active
    if user.status == 'active':
        return jsonify({
            'message': 'User is already active',
            'user': user.to_dict(include_timestamps=True)
        }), 200
    
    user.status = 'active'
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'User activated successfully',
            'user': user.to_dict(include_timestamps=True)
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to activate user',
            'status': 500
        }), 500


@admin_bp.route('/users/<int:user_id>/deactivate', methods=['PUT'])
@token_required
@admin_required
def deactivate_user(user_id):
    """Deactivate a user account (admin only)"""
    user = User.query.get(user_id)
    
    if not user:
        return jsonify({
            'error': 'Not Found',
            'message': 'User not found',
            'status': 404
        }), 404
    
    # Prevent admin from deactivating themselves
    if user.id == g.current_user.id:
        return jsonify({
            'error': 'Bad Request',
            'message': 'You cannot deactivate your own account',
            'status': 400
        }), 400
    
    # Check if already inactive
    if user.status == 'inactive':
        return jsonify({
            'message': 'User is already inactive',
            'user': user.to_dict(include_timestamps=True)
        }), 200
    
    user.status = 'inactive'
    
    try:
        db.session.commit()
        return jsonify({
            'message': 'User deactivated successfully',
            'user': user.to_dict(include_timestamps=True)
        }), 200
    
    except Exception as e:
        db.session.rollback()
        return jsonify({
            'error': 'Internal Server Error',
            'message': 'Failed to deactivate user',
            'status': 500
        }), 500
