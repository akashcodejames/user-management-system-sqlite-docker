# User Management System

## 1. Project Overview & Purpose

The **User Management System** is a robust, full-stack web application designed to handle user authentication, role-based access control, and profile management. It was built to demonstrate a production-ready architecture using modern technologies, emphasizing security, scalability, and developer experience.

**Key Features:**
*   **Secure Authentication**: JWT-based login and signup with password hashing.
*   **Role-Based Access Control (RBAC)**: Distinct 'Admin' and 'User' roles with protected routes.
*   **Admin Dashboard**: Centralized management to activate/deactivate users.
*   **Profile Management**: Self-service profile updates and password changes.
*   **Dockerized**: Fully containerized for consistent development and deployment.

---

## 2. Tech Stack Used

| Component | Technology | Description |
| :--- | :--- | :--- |
| **Backend** | **Flask (Python)** | REST API framework |
| | **SQLAlchemy** | ORM for database interactions |
| | **SQLite** | Lightweight, file-based database (Local Dev) |
| | **PyJWT** | JSON Web Token authentication |
| **Frontend** | **React.js** | Library for building user interfaces |
| | **Vite** | Next-generation frontend build tool |
| | **Axios** | Promise-based HTTP client |
| | **CSS3** | Modern, responsive styling |
| **Infrastructure** | **Docker** | Containerization platform |
| | **Docker Compose** | Multi-container orchestration |

---

## 3. Setup Instructions (Frontend & Backend)

The easiest way to run the application is using **Docker Compose**, which sets up both the frontend and backend automatically.

### Prerequisites
*   Docker & Docker Compose installed

### Steps

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/akashcodejames/user-management-system-sqlite-docker.git
    cd user-management-system-sqlite-docker
    ```

2.  **Start the Application**
    ```bash
    docker-compose up --build -d
    ```

3.  **Access the App**
    *   **Frontend**: [http://localhost:5173](http://localhost:5173)
    *   **Backend**: [http://localhost:5001](http://localhost:5001)

4.  **Login with Default Admin**
    *   **Email**: `admin@example1.com`
    *   **Password**: `Admin@12345678`

---

## 4. Environment Variables

The application uses the following environment variables. **Do not commit actual values to version control.**

### Backend (`/backend/.env`)

```ini
# Flask Configuration
FLASK_APP=run.py
FLASK_ENV=development
FLASK_DEBUG=1

# Database
DATABASE_URL=sqlite:////app/instance/app.db

# Security
SECRET_KEY=<your-secret-key>
JWT_SECRET_KEY=<your-jwt-secret-key>

# CORS
CORS_ORIGINS=http://localhost:5173
```

### Frontend (`/frontend/.env`)

```ini
# API Connection
VITE_API_URL=http://localhost:5001/api
```

---

## 5. Deployment Instructions

This project is configured for easy deployment using Docker.

### Option A: VPS / Docker Host (Recommended)
1.  **Provision a server** (e.g., Ubuntu on AWS, DigitalOcean).
2.  **Install Docker & Docker Compose**.
3.  **Clone the repo** onto the server.
4.  **Create production `.env` files** with secure secrets.
5.  **Run**: `docker-compose up -d --build`.

### Option B: Cloud Platforms (Render/Railway)
*   **Backend**: Deploy the `./backend` folder as a Python service. Set `DATABASE_URL` to a persistent PostgreSQL instance.
*   **Frontend**: Deploy the `./frontend` folder as a Static Site. Set `VITE_API_URL` to your backend's URL.

---

## 6. API Documentation

The API follows RESTful conventions. Below is a summary of available endpoints.

### Authentication
*   `POST /api/auth/signup` - Register a new user
*   `POST /api/auth/login` - Authenticate and receive JWT
*   `GET /api/auth/me` - Get current user details
*   `POST /api/auth/logout` - Logout

### Users
*   `GET /api/users/profile` - Get profile information
*   `PUT /api/users/profile` - Update profile details
*   `PUT /api/users/password` - Change password

### Admin
*   `GET /api/admin/users` - List all users (paginated)
*   `PUT /api/admin/users/<id>/activate` - Activate a user account
*   `PUT /api/admin/users/<id>/deactivate` - Deactivate a user account

> **Note**: For full specification, import the collection into Postman or inspect the routes in `backend/app`.
