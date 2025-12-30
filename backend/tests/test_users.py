import pytest
import json
from app import create_app, db
from app.models import User


@pytest.fixture
def app():
    """Create and configure a test app"""
    app = create_app('testing')
    
    with app.app_context():
        db.create_all()
        yield app
        db.session.remove()
        db.drop_all()


@pytest.fixture
def client(app):
    """Test client for making requests"""
    return app.test_client()


@pytest.fixture
def auth_headers(client):
    """Create a user and return auth headers"""
    response = client.post('/api/auth/signup', 
        json={
            'email': 'user@example.com',
            'password': 'UserPass123',
            'full_name': 'Test User'
        }
    )
    
    data = json.loads(response.data)
    token = data['token']
    
    return {'Authorization': f'Bearer {token}'}


def test_get_profile(client, auth_headers):
    """Test getting user profile"""
    response = client.get('/api/users/profile', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['email'] == 'user@example.com'
    assert data['full_name'] == 'Test User'
    assert 'created_at' in data


def test_update_profile_name(client, auth_headers):
    """Test updating user name"""
    response = client.put('/api/users/profile',
        headers=auth_headers,
        json={'full_name': 'Updated Name'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['full_name'] == 'Updated Name'


def test_update_profile_email(client, auth_headers):
    """Test updating user email"""
    response = client.put('/api/users/profile',
        headers=auth_headers,
        json={'email': 'newemail@example.com'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['email'] == 'newemail@example.com'


def test_update_profile_duplicate_email(client, auth_headers):
    """Test updating to an already taken email"""
    # Create another user
    client.post('/api/auth/signup',
        json={
            'email': 'other@example.com',
            'password': 'OtherPass123',
            'full_name': 'Other User'
        }
    )
    
    # Try to update to that email
    response = client.put('/api/users/profile',
        headers=auth_headers,
        json={'email': 'other@example.com'}
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'already in use' in data['message'].lower()


def test_change_password_success(client, auth_headers):
    """Test successful password change"""
    response = client.put('/api/users/password',
        headers=auth_headers,
        json={
            'current_password': 'UserPass123',
            'new_password': 'NewSecurePass123'
        }
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'success' in data['message'].lower()
    
    # Verify can login with new password
    login_response = client.post('/api/auth/login',
        json={
            'email': 'user@example.com',
            'password': 'NewSecurePass123'
        }
    )
    assert login_response.status_code == 200


def test_change_password_wrong_current(client, auth_headers):
    """Test password change with wrong current password"""
    response = client.put('/api/users/password',
        headers=auth_headers,
        json={
            'current_password': 'WrongPassword',
            'new_password': 'NewPass123'
        }
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'incorrect' in data['message'].lower()


def test_protected_route_without_token(client):
    """Test accessing protected route without token"""
    response = client.get('/api/users/profile')
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'token' in data['message'].lower()
