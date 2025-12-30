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
    # Create a test user
    response = client.post('/api/auth/signup', 
        json={
            'email': 'test@example.com',
            'password': 'TestPass123',
            'full_name': 'Test User'
        }
    )
    
    data = json.loads(response.data)
    token = data['token']
    
    return {'Authorization': f'Bearer {token}'}


@pytest.fixture
def admin_headers(client, app):
    """Create an admin user and return auth headers"""
    with app.app_context():
        # Create admin user directly
        admin = User(
            email='admin@example.com',
            full_name='Admin User',
            role='admin',
            status='active'
        )
        admin.set_password('AdminPass123')
        db.session.add(admin)
        db.session.commit()
        
        # Login as admin
        response = client.post('/api/auth/login',
            json={
                'email': 'admin@example.com',
                'password': 'AdminPass123'
            }
        )
        
        data = json.loads(response.data)
        token = data['token']
    
    return {'Authorization': f'Bearer {token}'}


def test_user_signup_success(client):
    """Test successful user signup"""
    response = client.post('/api/auth/signup',
        json={
            'email': 'newuser@example.com',
            'password': 'SecurePass123',
            'full_name': 'New User'
        }
    )
    
    assert response.status_code == 201
    data = json.loads(response.data)
    assert 'token' in data
    assert data['user']['email'] == 'newuser@example.com'
    assert data['user']['role'] == 'user'
    assert data['user']['status'] == 'active'


def test_user_signup_duplicate_email(client):
    """Test signup with duplicate email fails"""
    # Create first user
    client.post('/api/auth/signup',
        json={
            'email': 'duplicate@example.com',
            'password': 'SecurePass123',
            'full_name': 'First User'
        }
    )
    
    # Try to create second user with same email
    response = client.post('/api/auth/signup',
        json={
            'email': 'duplicate@example.com',
            'password': 'Pass456',
            'full_name': 'Second User'
        }
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'already registered' in data['message'].lower()


def test_user_signup_weak_password(client):
    """Test signup with weak password fails"""
    response = client.post('/api/auth/signup',
        json={
            'email': 'weak@example.com',
            'password': 'weak',
            'full_name': 'Weak User'
        }
    )
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'password' in data['message'].lower()


def test_user_login_success(client):
    """Test successful user login"""
    # Create user
    client.post('/api/auth/signup',
        json={
            'email': 'login@example.com',
            'password': 'LoginPass123',
            'full_name': 'Login User'
        }
    )
    
    # Login
    response = client.post('/api/auth/login',
        json={
            'email': 'login@example.com',
            'password': 'LoginPass123'
        }
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'token' in data
    assert data['user']['email'] == 'login@example.com'
    assert 'last_login' in data['user']


def test_user_login_invalid_credentials(client):
    """Test login with invalid credentials fails"""
    response = client.post('/api/auth/login',
        json={
            'email': 'nonexistent@example.com',
            'password': 'WrongPass123'
        }
    )
    
    assert response.status_code == 401
    data = json.loads(response.data)
    assert 'invalid' in data['message'].lower()


def test_get_current_user(client, auth_headers):
    """Test getting current user info"""
    response = client.get('/api/auth/me', headers=auth_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['email'] == 'test@example.com'
    assert 'created_at' in data


def test_jwt_token_validation(client):
    """Test JWT token generation and validation"""
    # Signup
    response = client.post('/api/auth/signup',
        json={
            'email': 'token@example.com',
            'password': 'TokenPass123',
            'full_name': 'Token User'
        }
    )
    
    data = json.loads(response.data)
    token = data['token']
    
    # Use token to access protected route
    response = client.get('/api/auth/me',
        headers={'Authorization': f'Bearer {token}'}
    )
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['email'] == 'token@example.com'
