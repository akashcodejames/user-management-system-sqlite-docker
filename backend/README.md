# User Management System - Backend

A secure Flask-based REST API for user management with JWT authentication and role-based access control.

## 🚀 Features

- **Authentication**: JWT-based signup, login, and logout
- **User Management**: Profile viewing/editing, password changes
- **Admin Dashboard**: User listing with pagination, activate/deactivate users
- **Security**: bcrypt password hashing, protected routes, RBAC
- **Testing**: Comprehensive unit tests with pytest

## 🛠️ Tech Stack

- **Backend**: Python 3.9+ with Flask
- **Database**: PostgreSQL
- **Authentication**: JWT (PyJWT)
- **Password Hashing**: bcrypt
- **ORM**: SQLAlchemy
- **Testing**: pytest
- **CORS**: Flask-CORS

## 📋 Prerequisites

- Python 3.9 or higher
- PostgreSQL database
- pip (Python package manager)

## ⚙️ Setup Instructions

### 1. Clone the Repository

```bash
cd intern/backend
```

### 2. Create Virtual Environment

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the backend directory:

```bash
cp .env.example .env
```

Edit `.env` with your settings:

```env
FLASK_ENV=development
SECRET_KEY=your-super-secret-key-change-this
JWT_EXPIRATION_HOURS=24
DATABASE_URL=postgresql://username:password@localhost:5432/user_management
CORS_ORIGINS=http://localhost:3000,http://localhost:5173
PORT=5000
```

### 5. Set Up Database

Create a PostgreSQL database:

```bash
createdb user_management
```

Initialize the database tables:

```bash
python run.py
```

### 6. Create Admin User

```bash
flask create-admin
# Follow the prompts to enter email, password, and name
```

### 7. Run the Application

```bash
python run.py
```

The API will be available at `http://localhost:5000`

## 🧪 Running Tests

Run all tests:

```bash
pytest
```

Run with coverage:

```bash
pytest --cov=app tests/
```

Run specific test file:

```bash
pytest tests/test_auth.py -v
```

## 📡 API Documentation

### Base URL
```
http://localhost:5000/api
```

### Authentication Endpoints

#### POST /auth/signup
Create a new user account.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123",
  "full_name": "John Doe"
}
```

**Response (201):**
```json
{
  "token": "eyJ0eXAiOiJKV1...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user",
    "status": "active"
  }
}
```

#### POST /auth/login
Login with existing credentials.

**Request:**
```json
{
  "email": "user@example.com",
  "password": "SecurePass123"
}
```

**Response (200):**
```json
{
  "token": "eyJ0eXAiOiJKV1...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "full_name": "John Doe",
    "role": "user",
    "status": "active",
    "created_at": "2025-12-29T12:00:00",
    "last_login": "2025-12-29T13:00:00"
  }
}
```

#### GET /auth/me
Get current user information (requires authentication).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "user",
  "status": "active",
  "created_at": "2025-12-29T12:00:00",
  "updated_at": "2025-12-29T12:00:00"
}
```

### User Management Endpoints

#### GET /users/profile
Get current user's profile (requires authentication).

**Headers:**
```
Authorization: Bearer <token>
```

**Response (200):**
```json
{
  "id": 1,
  "email": "user@example.com",
  "full_name": "John Doe",
  "role": "user",
  "status": "active",
  "created_at": "2025-12-29T12:00:00"
}
```

#### PUT /users/profile
Update profile information (requires authentication).

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "full_name": "John Smith",
  "email": "newmail@example.com"
}
```

**Response (200):**
```json
{
  "id": 1,
  "email": "newmail@example.com",
  "full_name": "John Smith",
  "role": "user",
  "status": "active"
}
```

#### PUT /users/password
Change password (requires authentication).

**Headers:**
```
Authorization: Bearer <token>
```

**Request:**
```json
{
  "current_password": "OldPass123",
  "new_password": "NewSecurePass123"
}
```

**Response (200):**
```json
{
  "message": "Password updated successfully"
}
```

### Admin Endpoints

#### GET /admin/users
Get all users with pagination (admin only).

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Query Parameters:**
- `page` (optional): Page number (default: 1)
- `per_page` (optional): Users per page (default: 10, max: 100)

**Example:**
```
GET /admin/users?page=1&per_page=10
```

**Response (200):**
```json
{
  "users": [
    {
      "id": 1,
      "email": "user@example.com",
      "full_name": "John Doe",
      "role": "user",
      "status": "active",
      "created_at": "2025-12-29T12:00:00",
      "last_login": "2025-12-29T13:00:00"
    }
  ],
  "total": 50,
  "page": 1,
  "pages": 5,
  "per_page": 10
}
```

#### PUT /admin/users/:id/activate
Activate a user account (admin only).

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Response (200):**
```json
{
  "message": "User activated successfully",
  "user": {
    "id": 2,
    "email": "user@example.com",
    "status": "active"
  }
}
```

#### PUT /admin/users/:id/deactivate
Deactivate a user account (admin only).

**Headers:**
```
Authorization: Bearer <admin-token>
```

**Response (200):**
```json
{
  "message": "User deactivated successfully",
  "user": {
    "id": 2,
    "email": "user@example.com",
    "status": "inactive"
  }
}
```

## 🔒 Security Features

- **Password Hashing**: bcrypt with salt
- **JWT Authentication**: Secure token-based auth
- **Role-Based Access Control**: Admin and user roles
- **Input Validation**: Email format, password strength
- **Protected Routes**: Middleware for authentication
- **CORS**: Configured for frontend origins
- **Environment Variables**: Sensitive data in .env

## 🚀 Deployment

### Deploy to Render

1. Create a new Web Service on Render
2. Connect your GitHub repository
3. Configure build command: `pip install -r requirements.txt`
4. Configure start command: `gunicorn run:app`
5. Add environment variables in Render dashboard
6. Deploy!

### Environment Variables for Production

Set these in your deployment platform:
- `FLASK_ENV=production`
- `SECRET_KEY=<strong-secret-key>`
- `DATABASE_URL=<postgresql-url>`
- `CORS_ORIGINS=<frontend-url>`

## 📁 Project Structure

```
backend/
├── app/
│   ├── __init__.py          # Flask app factory
│   ├── config.py            # Configuration
│   ├── models.py            # User model
│   ├── auth/
│   │   ├── routes.py        # Auth endpoints
│   │   └── utils.py         # Validation helpers
│   ├── users/
│   │   ├── routes.py        # User endpoints
│   │   └── decorators.py    # Auth decorators
│   └── admin/
│       └── routes.py        # Admin endpoints
├── tests/
│   ├── test_auth.py         # Auth tests
│   ├── test_users.py        # User tests
│   └── test_admin.py        # Admin tests
├── requirements.txt         # Dependencies
├── .env.example            # Environment template
├── .gitignore              # Git ignore
└── run.py                  # Entry point
```

## 🏥 Health Check

```bash
curl http://localhost:5000/health
```

**Response:**
```json
{
  "status": "healthy",
  "message": "User Management API is running"
}
```

## 📝 License

This project is created for the Backend Intern Assessment at Purple Merit Technologies.
