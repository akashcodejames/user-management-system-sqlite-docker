# User Management System

## 1. Project Overview & Purpose

The **User Management System** is a full-stack, production-ready web application designed to handle user authentication, role-based access control (RBAC), and profile management securely and efficiently.

**Purpose:**
To demonstrate a scalable, secure, and modern architecture for managing users (Admin vs. Regular User) with features like JWT authentication, password hashing, and a responsive dashboard.

**Key Features:**
*   **Authentication**: Secure Signup/Login with JWT and bcrypt.
*   **RBAC**: Admin-only routes to manage (activate/deactivate) users.
*   **Profile Management**: Self-service profile updates and password changes.
*   **Responsive UI**: Modern interface built with React and Vite.

---

## 2. Tech Stack Used

| Layer | Technology | Usage |
| :--- | :--- | :--- |
| **Backend** | **Flask** | (Python) REST API Framework |
| | **SQLAlchemy** | ORM for database management |
| | **PyJWT** | Token-based authentication |
| | **SQLite** | Database (Local/Docker) |
| **Frontend** | **React.js** | UI Library |
| | **Vite** | Build tool |
| | **Axios** | HTTP Client |
| | **CSS Modules** | Component-level styling |
| **DevOps** | **Docker** | Containerization |
| | **Docker Compose** | Orchestration for local dev |

---

## 3. Setup Instructions (Local Development)

### Prerequisites
- Node.js & npm (if running locally without Docker)
- Python 3.9+ (if running locally without Docker)
- Docker & Docker Compose (Recommended)

### Option A: Using Docker Compose (Recommended)
1.  **Clone the repository:**
    ```bash
    git clone https://github.com/akashcodejames/user-management-system-sqlite-docker.git
    cd user-management-system-sqlite-docker
    ```

2.  **Start the services:**
    ```bash
    docker-compose up --build -d
    ```

3.  **Access the Application:**
    - **Frontend**: [http://localhost:5173](http://localhost:5173)
    - **Backend API**: [http://localhost:5001](http://localhost:5001)

### Option B: Manual Setup

**Backend:**
1.  Navigate to `/backend`.
2.  Create virtual env: `python -m venv venv` && `source venv/bin/activate`.
3.  Install deps: `pip install -r requirements.txt`.
4.  Run migrations: `flask db upgrade`.
5.  Start server: `python run.py`.

**Frontend:**
1.  Navigate to `/frontend`.
2.  Install deps: `npm install`.
3.  Start server: `npm run dev`.

---

## 4. Environment Variables

Create `.env` files in the respective directories. **Do not share actual values in public repos.**

### Backend (`/backend/.env`)
| Variable | Description |
| :--- | :--- |
| `FLASK_APP` | Entry point (e.g., `run.py`) |
| `FLASK_ENV` | Environment (`development` or `production`) |
| `DATABASE_URL` | Connection string (e.g., `sqlite:////app/instance/app.db`) |
| `SECRET_KEY` | Secret for Flask sessions |
| `JWT_SECRET_KEY` | Secret for signing JWTs |
| `CORS_ORIGINS` | Allowed frontend origins |

### Frontend (`/frontend/.env`)
| Variable | Description |
| :--- | :--- |
| `VITE_API_URL` | URL of the Backend API (e.g., `http://localhost:5001/api`) |

---

## 5. Deployment Instructions

### Deployment Strategy
This application is designed to be deployed as decoupled services.

1.  **Database**: Hosted on a managed Cloud Database (e.g., Neon PostgreSQL or MongoDB Atlas).
2.  **Backend**: Deployed to a Platform-as-a-Service (Render/Railway).
    *   **Steps**: Connect GitHub repo, set build command to `pip install -r requirements.txt`, start command to `gunicorn run:app`, and add environment variables.
3.  **Frontend**: Deployed to a Static Site Host (Vercel/Netlify).
    *   **Steps**: Connect GitHub repo, set framework to `Vite`, build command `npm run build`, and add `VITE_API_URL` environment variable pointing to the deployed backend.

### Live Deployment Links
*   **Frontend**: *[Insert Vercel/Netlify Link Here]*
*   **Backend API**: *[Insert Render/Railway Link Here]*
*   **API Docs**: *[Insert Postman/Swagger Link Here]*

---

## 6. API Documentation

### Base URL: `/api`

### 1. **Login**
**Endpoint**: `POST /auth/login`

**Request Body:**
```json
{
  "email": "user@example.com",
  "password": "Password123!"
}
```

**Response (200 OK):**
```json
{
  "token": "eyJhbGciOiJIUzI1Ni...",
  "user": {
    "id": 1,
    "email": "user@example.com",
    "role": "user"
  }
}
```

### 2. **Get Profile**
**Endpoint**: `GET /users/profile`  
**Headers**: `Authorization: Bearer <token>`

**Response (200 OK):**
```json
{
  "id": 1,
  "full_name": "Test User",
  "email": "user@example.com",
  "role": "user",
  "created_at": "2025-12-30T10:00:00"
}
```

### 3. **Admin: List Users**
**Endpoint**: `GET /admin/users?page=1&per_page=10`  
**Headers**: `Authorization: Bearer <token>` (Admin Only)

**Response (200 OK):**
```json
{
  "users": [
    {
      "id": 2,
      "email": "another@example.com",
      "status": "active"
    }
  ],
  "total": 5,
  "pages": 1
}
```

---

## 📂 Deliverables Checklist

- [x] **GitHub Repository**: [https://github.com/akashcodejames/user-management-system-sqlite-docker](https://github.com/akashcodejames/user-management-system-sqlite-docker)
- [x] **Proper Commit History**: Structured commits used throughout development.
- [x] **Sensitive Data Handled**: All secrets in `.env` (excluded from git).
- [ ] **Live Links**: *(Please refer to Deployment Instructions section)*.
