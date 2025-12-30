# 🚀 User Management System

A full-stack, dockerized **User Management System** built with **Flask**, **React**, and **SQLite**. This application demonstrates a production-ready architecture with JWT authentication, role-based access control, and a modern, responsive user interface.

![Python](https://img.shields.io/badge/Python-3.9-blue)
![React](https://img.shields.io/badge/React-18-blue)
![Flask](https://img.shields.io/badge/Flask-3.0-green)
![Docker](https://img.shields.io/badge/Docker-Compose-blue)
![License](https://img.shields.io/badge/License-MIT-green)

---

## ✨ Features

### � Authentication & Security
- **JWT Authentication**: Secure stateless authentication using JSON Web Tokens.
- **Role-Based Access Control (RBAC)**: Distinct permissions for `Admin` and `User` roles.
- **Secure Password Hashing**: Uses `bcrypt` for storing passwords securely.
- **Protected Routes**: Frontend routing ensures restricted access to authorized users only.

### 👤 User Management
- **Dashboard**: Personalized user dashboard showing profile status and roles.
- **Profile Management**: Users can update their profile details and change passwords.
- **Registration**: Self-service user signup with email validation.

### 🛡️ Admin Capabilities
- **Admin Dashboard**: Centralized view of all registered users.
- **User Control**: Ability to **activate** or **deactivate** user accounts.
- **Pagination**: Efficiently browse through large lists of users.

### 🐳 DevOps & Infrastructure
- **Dockerized**: Fully containerized backend and frontend for consistent environments.
- **Hot Reload**: Development environment configured for instant code updates.
- **Persistent Storage**: SQLite database changes persist across container restarts.

---

## 🛠️ Tech Stack

### Backend
- **Framework**: Flask (Python)
- **Database**: SQLite (SQLAlchemy ORM)
- **Migrations**: Flask-Migrate (Alembic)
- **Authentication**: PyJWT
- **Server**: Gunicorn (Production-grade WSGI server)

### Frontend
- **Framework**: React.js (Vite)
- **Styling**: Modern CSS3 with responsive design
- **State Management**: Context API
- **HTTP Client**: Axios

### Infrastructure
- **Containerization**: Docker & Docker Compose
- **Orchestration**: Docker Compose

---

## 🚀 Getting Started

### Prerequisites
- [Docker Desktop](https://www.docker.com/products/docker-desktop/) installed and running.

### 1. Clone the Repository
```bash
git clone https://github.com/akashcodejames/user-management-system-sqlite-docker.git
cd user-management-system-sqlite-docker
```

### 2. Run with Docker Compose
Start the application in detached mode:
```bash
docker-compose up --build -d
```

### 3. Access the Application
- **Frontend**: [http://localhost:5173](http://localhost:5173)
- **Backend API**: [http://localhost:5001](http://localhost:5001)

---

## 🔑 Default Admin Credentials

Upon the first run, an admin user is **automatically created**. 

| Role | Email | Password |
|------|-------|----------|
| **Admin** | `admin@example1.com` | `Admin@12345678` |

> Required login to access the Admin Panel.

---

## 📂 Project Structure

```bash
.
├── backend/                 # Flask Backend
│   ├── app/                 # Application Factory & Blueprints
│   │   ├── auth/            # Authentication Routes
│   │   ├── users/           # User Management Routes
│   │   ├── admin/           # Admin Routes
│   │   └── models.py        # Database Models
│   ├── instance/            # Persistent SQLite Database
│   ├── migrations/          # Database Migrations
│   ├── create_admin.py      # Script to seed admin user
│   ├── config.py            # Configuration settings
│   └── Dockerfile           # Backend Docker config
│
├── frontend/                # React Frontend
│   ├── src/
│   │   ├── components/      # Reusable UI Components
│   │   ├── pages/           # Application Pages
│   │   ├── context/         # Auth Context
│   │   └── services/        # API Service calls
│   └── Dockerfile           # Frontend Docker config
│
└── docker-compose.yml       # Service Orchestration
```

---

## � API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| `POST` | `/api/auth/login` | User Login | No |
| `POST` | `/api/auth/signup` | User Registration | No |
| `GET` | `/api/auth/me` | Get Current User | Yes |
| `GET` | `/api/users/profile` | Get User Profile | Yes |
| `PUT` | `/api/users/profile` | Update Profile | Yes |
| `GET` | `/api/admin/users` | List All Users | **Admin** |
| `PUT` | `/api/admin/users/:id/activate` | Activate User | **Admin** |

---

## 🔧 Troubleshooting

**Database not found / Reset Database**
If you need to reset the database to a clean state:
```bash
docker-compose down
rm -rf backend/instance
docker-compose up --build -d
```

**Port Conflicts**
Ensure ports `5173` (Frontend) and `5001` (Backend) are not in use by other applications.

---

## 📄 License

This project is open-source and available under the [MIT License](LICENSE).
