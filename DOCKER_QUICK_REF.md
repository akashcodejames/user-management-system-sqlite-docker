# Quick Reference - Docker Commands

## 🚀 Start
```bash
docker-compose up --build -d
```

## 🛑 Stop
```bash
docker-compose down
```

## 📊 Status
```bash
docker-compose ps
docker-compose logs -f
```

## 🔄 Restart
```bash
docker-compose restart
```

## 🗄️ Fresh Database
```bash
docker-compose down
rm -rf backend/instance
mkdir -p backend/instance
docker-compose up --build -d
```

## 🔍 Access Points
- Frontend: http://localhost:5173
- Backend: http://localhost:5001
- Health: http://localhost:5001/health

## 🔑 Admin Login
- Email: `admin@example1.com`
- Password: `Admin@12345678`

## 📂 Database Location
```
./backend/instance/app.db
```
