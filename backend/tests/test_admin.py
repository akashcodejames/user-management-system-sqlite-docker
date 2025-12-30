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
def admin_headers(client, app):
    """Create an admin user and return auth headers"""
    with app.app_context():
        admin = User(
            email='admin@example.com',
            full_name='Admin User',
            role='admin',
            status='active'
        )
        admin.set_password('AdminPass123')
        db.session.add(admin)
        db.session.commit()
    
    response = client.post('/api/auth/login',
        json={
            'email': 'admin@example.com',
            'password': 'AdminPass123'
        }
    )
    
    data = json.loads(response.data)
    return {'Authorization': f'Bearer {data["token"]}'}


@pytest.fixture
def regular_user_headers(client):
    """Create a regular user and return auth headers"""
    response = client.post('/api/auth/signup',
        json={
            'email': 'user@example.com',
            'password': 'UserPass123',
            'full_name': 'Regular User'
        }
    )
    
    data = json.loads(response.data)
    return {'Authorization': f'Bearer {data["token"]}'}


def test_get_all_users_admin(client, admin_headers, app):
    """Test admin can get all users"""
    # Create some test users
    with app.app_context():
        for i in range(5):
            user = User(
                email=f'user{i}@example.com',
                full_name=f'User {i}',
                role='user',
                status='active'
            )
            user.set_password('Pass123')
            db.session.add(user)
        db.session.commit()
    
    response = client.get('/api/admin/users', headers=admin_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert 'users' in data
    assert 'total' in data
    assert 'page' in data
    assert len(data['users']) > 0


def test_get_all_users_pagination(client, admin_headers, app):
    """Test pagination works correctly"""
    # Create 15 users
    with app.app_context():
        for i in range(15):
            user = User(
                email=f'user{i}@example.com',
                full_name=f'User {i}',
                role='user',
                status='active'
            )
            user.set_password('Pass123')
            db.session.add(user)
        db.session.commit()
    
    # Get first page
    response = client.get('/api/admin/users?page=1&per_page=10', headers=admin_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert len(data['users']) == 10
    assert data['page'] == 1


def test_get_all_users_non_admin(client, regular_user_headers):
    """Test regular user cannot access admin endpoint"""
    response = client.get('/api/admin/users', headers=regular_user_headers)
    
    assert response.status_code == 403
    data = json.loads(response.data)
    assert 'admin' in data['message'].lower()


def test_activate_user(client, admin_headers, app):
    """Test admin can activate a user"""
    # Create inactive user
    with app.app_context():
        user = User(
            email='inactive@example.com',
            full_name='Inactive User',
            role='user',
            status='inactive'
        )
        user.set_password('Pass123')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    
    response = client.put(f'/api/admin/users/{user_id}/activate', headers=admin_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['user']['status'] == 'active'


def test_deactivate_user(client, admin_headers, app):
    """Test admin can deactivate a user"""
    # Create active user
    with app.app_context():
        user = User(
            email='active@example.com',
            full_name='Active User',
            role='user',
            status='active'
        )
        user.set_password('Pass123')
        db.session.add(user)
        db.session.commit()
        user_id = user.id
    
    response = client.put(f'/api/admin/users/{user_id}/deactivate', headers=admin_headers)
    
    assert response.status_code == 200
    data = json.loads(response.data)
    assert data['user']['status'] == 'inactive'


def test_admin_cannot_deactivate_self(client, admin_headers, app):
    """Test admin cannot deactivate their own account"""
    # Get admin user ID
    with app.app_context():
        admin = User.query.filter_by(email='admin@example.com').first()
        admin_id = admin.id
    
    response = client.put(f'/api/admin/users/{admin_id}/deactivate', headers=admin_headers)
    
    assert response.status_code == 400
    data = json.loads(response.data)
    assert 'cannot deactivate your own' in data['message'].lower()


def test_activate_nonexistent_user(client, admin_headers):
    """Test activating non-existent user returns 404"""
    response = client.put('/api/admin/users/99999/activate', headers=admin_headers)
    
    assert response.status_code == 404
    data = json.loads(response.data)
    assert 'not found' in data['message'].lower()
