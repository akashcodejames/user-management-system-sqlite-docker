# Docker Setup with SQLite - Local Development

## 🎯 Overview

This Docker Compose setup provides a complete local development environment with:
- **Backend**: Flask API with SQLite database
- **Frontend**: React/Vite application
- **Persistent Storage**: SQLite database stored in `./backend/instance/app.db`
- **Auto-initialization**: Database migrations and admin user creation

## 📋 Prerequisites

- Docker Desktop installed and running
- Docker Compose (usually included with Docker Desktop)

## 🚀 Quick Start

### 1. Start the Application

```bash
# Build and start all services
docker-compose up --build

# Or run in detached mode (background)
docker-compose up --build -d
```

### 2. Access the Application

- **Frontend**: http://localhost:5173
- **Backend API**: http://localhost:5001
- **Health Check**: http://localhost:5001/health

### 3. Default Admin Credentials

```
Email: admin@example1.com
Password: Admin@12345678
```

## 🗄️ Database Information

### SQLite Storage Location
The SQLite database is persisted at:
```
./backend/instance/app.db
```

This file is created automatically and persists across container restarts.

### Database Initialization

The setup automatically:
1. ✅ Runs Flask database migrations (`flask db upgrade`)
2. ✅ Creates database tables
3. ✅ Creates the admin user via `create_admin.py`

## 🛠️ Common Commands

### Start Services
```bash
# Start with logs in foreground
docker-compose up

# Start in background
docker-compose up -d

# Rebuild and start
docker-compose up --build
```

### Stop Services
```bash
# Stop containers (keeps data)
docker-compose down

# Stop and remove volumes (deletes data)
docker-compose down -v
```

### View Logs
```bash
# All services
docker-compose logs

# Specific service
docker-compose logs backend
docker-compose logs frontend

# Follow logs (real-time)
docker-compose logs -f backend
```

### Check Status
```bash
# View running containers
docker-compose ps

# View resource usage
docker stats
```

### Reset Database
```bash
# Stop containers
docker-compose down

# Delete database file
rm -rf backend/instance

# Recreate empty instance directory
mkdir -p backend/instance

# Start fresh
docker-compose up --build
```

## 🔧 Configuration Files

### docker-compose.yml
Main orchestration file that:
- Defines backend and frontend services
- Mounts volumes for code hot-reload
- Maps SQLite database to project folder
- Sets environment variables

### Backend Dockerfile
Located at `./backend/Dockerfile`:
- Uses Python 3.9-slim base image
- Installs dependencies from requirements.txt
- Creates instance directory for SQLite
- Sets up Flask environment

### Frontend Dockerfile
Located at `./frontend/Dockerfile`:
- Uses Node 22 Alpine base image
- Installs npm dependencies
- Runs Vite dev server with hot-reload

## 📁 Volume Mounts

### Backend
- `./backend:/app` - Full backend code (hot-reload)
- `./backend/instance:/app/instance` - SQLite database persistence

### Frontend
- `./frontend:/app` - Full frontend code (hot-reload)
- `/app/node_modules` - Node modules (anonymous volume for performance)

## 🌐 Environment Variables

### Backend Environment
```yaml
FLASK_ENV=development
FLASK_APP=run.py
FLASK_DEBUG=1
DATABASE_URL=sqlite:////app/instance/app.db
SECRET_KEY=dev-secret-key-change-in-production
JWT_SECRET_KEY=dev-jwt-secret-key-change-in-production
CORS_ORIGINS=http://localhost:5173
```

### Frontend Environment
```yaml
VITE_API_URL=http://localhost:5001
```

## 🔍 Troubleshooting

### Port Already in Use
If you get port conflicts:
```bash
# Check what's using the port
lsof -i :5001  # Backend
lsof -i :5173  # Frontend

# Kill the process or change ports in docker-compose.yml
```

### Database Issues
```bash
# Check if database exists
ls -lah backend/instance/

# View database inside container
docker-compose exec backend ls -la /app/instance/

# Check migration status
docker-compose exec backend flask db current
```

### Container Won't Start
```bash
# View detailed logs
docker-compose logs backend

# Rebuild from scratch
docker-compose down -v
docker-compose build --no-cache
docker-compose up
```

### Database Locked Error
SQLite can have issues with concurrent access. If you see "database is locked":
```bash
# Restart the backend service
docker-compose restart backend
```

## 🔄 Hot Reload

Both frontend and backend support hot reload:
- **Frontend**: Vite automatically detects changes
- **Backend**: Volume mount at `./backend:/app` enables code changes

Note: For backend, you're using Gunicorn with `--reload` flag which watches for file changes.

## 📝 Creating New Database Migrations

If you modify database models:

```bash
# Create migration
docker-compose exec backend flask db migrate -m "description of changes"

# Apply migration
docker-compose exec backend flask db upgrade

# Or restart containers (migration runs automatically)
docker-compose restart backend
```

## 🧪 Running Tests

```bash
# Run backend tests
docker-compose exec backend pytest

# Run with coverage
docker-compose exec backend pytest --cov=app
```

## 🎨 Accessing Frontend

Navigate to http://localhost:5173 in your browser. The frontend will automatically connect to the backend API at http://localhost:5001.

## 📊 Database Inspection

You can inspect the SQLite database directly:

```bash
# Using sqlite3 command line
sqlite3 backend/instance/app.db

# Common queries
sqlite> .tables
sqlite> SELECT * FROM user;
sqlite> .exit
```

## 🛡️ Security Notes

⚠️ **This setup is for LOCAL DEVELOPMENT only**

For production:
- Change SECRET_KEY and JWT_SECRET_KEY
- Use PostgreSQL instead of SQLite
- Enable HTTPS
- Update CORS_ORIGINS
- Use environment-specific .env files

## 📚 Additional Resources

- Flask Documentation: https://flask.palletsprojects.com/
- Docker Compose: https://docs.docker.com/compose/
- Vite: https://vitejs.dev/

## ✅ Verify Setup

Run these commands to verify everything is working:

```bash
# 1. Check services are running
docker-compose ps

# 2. Test backend health
curl http://localhost:5001/health

# 3. Test admin login
curl -X POST http://localhost:5001/api/auth/login \
  -H "Content-Type: application/json" \
  -d '{"email":"admin@example1.com","password":"Admin@12345678"}'

# 4. Check database file exists
ls -lah backend/instance/app.db

# 5. Open frontend
open http://localhost:5173
```

All checks should pass! ✨
