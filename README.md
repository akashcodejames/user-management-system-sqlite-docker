# User Management System (Docker + SQLite)

A complete full-stack User Management System featuring a Flask backend, React frontend, and SQLite database, fully dockerized for easy local development.

## 🚀 Quick Start

1. **Clone the repository**
2. **Start the application**:
   ```bash
   docker-compose up --build -d
   ```
3. **Access the application**:
   - Frontend: [http://localhost:5173](http://localhost:5173)
   - Backend API: [http://localhost:5001](http://localhost:5001)

## 📋 Admin Login Credentials

Use these credentials to log in to the admin dashboard:

- **Email**: `admin@example1.com`
- **Password**: `Admin@12345678`

## 🏗️ Architecture

- **Backend**: Flask (Python) with SQLAlchemy & SQLite
- **Frontend**: React (Vite)
- **Containerization**: Docker & Docker Compose
- **Database**: SQLite (persisted in `./backend/instance/app.db`)

## ✨ Features

- **Authentication**: Login, Signup, JWT (JSON Web Tokens)
- **Role-Based Access Control**: Admin & User roles
- **User Management**: Admin can view, activate, and deactivate users
- **Profile Management**: Users can update their profile and password
- **Persistent Storage**: Database data survives container restarts
- **Hot Reload**: Code changes in backend or frontend reflect immediately

## 🛠️ Docker Commands Reference

- **Start**: `docker-compose up -d`
- **Stop**: `docker-compose down`
- **View Logs**: `docker-compose logs -f`
- **Rebuild**: `docker-compose up --build -d`
- **Reset Database**:
  ```bash
  docker-compose down
  rm -rf backend/instance
  docker-compose up -d
  ```

## 📂 Project Structure

```
.
├── backend/                # Flask Backend
│   ├── app/                # Application Code
│   ├── instance/           # SQLite Database Storage
│   └── Dockerfile          # Backend Config
├── frontend/               # React Frontend
│   ├── src/                # React Source Code
│   └── Dockerfile          # Frontend Config
└── docker-compose.yml      # Service Orchestration
```

## 🔧 Configuration

The application is pre-configured for local development.
- **Backend Port**: 5001
- **Frontend Port**: 5173
- **Database**: SQLite
