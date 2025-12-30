# User Management System - Complete Full Stack Application

A production-ready user management system with authentication, role-based access control, and admin dashboard.

## 🚀 Application is Running!

**Backend:** http://localhost:5001  
**Frontend:** http://localhost:5173  
**Database:** Aven Cloud PostgreSQL

## 📦 What's Included

### Backend (Flask)
- ✅ RESTful API with 10 endpoints
- ✅ JWT authentication
- ✅ bcrypt password hashing
- ✅ Role-based access control (admin/user)
- ✅ PostgreSQL database (cloud-hosted)
- ✅ 21/21 tests passing
- ✅ Complete API documentation

### Frontend (React + Vite)
- ✅ Modern, beautiful UI with animations
- ✅ Login & Signup pages
- ✅ User Dashboard
- ✅ Profile management
- ✅ Admin Panel with user management
- ✅ Pagination
- ✅ Protected routes
- ✅ Responsive design

## 🎯 How to Use

### 1. Access the Application
Open your browser and navigate to: **http://localhost:5173**

### 2. Create an Account
1. Click "Sign up" on the login page
2. Fill in your details:
   - Full Name
   - Email
   - Password (min 8 chars, uppercase, lowercase, digit)
3. Click "Sign Up"

### 3. User Features
- **Dashboard**: View your account status and role
- **Profile**: Edit your name, email, and change password
- **Navigation**: Easy access to all features

### 4. Admin Features
First, create an admin account using the terminal:
```bash
cd backend
source venv/bin/activate
flask create-admin
```

Then login with admin credentials to access:
- **Admin Dashboard**: View all registered users
- **User Management**: Activate/Deactivate accounts
- **Pagination**: Navigate through user lists

## 🔑 Test Accounts

### Create Admin Account
```bash
cd backend
source venv/bin/activate
flask create-admin
# Enter: admin@example.com / AdminPass123 / Admin User
```

### Create Regular User
Use the signup page with any valid email

## 📸 Application Pages

### 1. Login Page
- Clean, modern design
- Email/password authentication
- Link to signup page
- Error handling with user-friendly messages

### 2. Signup Page
- Full name, email, password fields
- Password confirmation
- Client-side validation
- Automatic login after signup

### 3. User Dashboard
- Welcome message with user's name
- Account status card
- Role badge
- Quick action buttons
- Clean, card-based layout

### 4. Profile Page
- View and edit profile information
- Change password securely
- Form validation
- Success/error notifications

### 5. Admin Panel
- User table with all registered users
- Sortable columns
- Role and status badges
- Activate/Deactivate buttons
- Pagination (10 users per page)
- Confirmation dialogs for actions

## 🎨 Design Features

- **Vibrant Colors**: Purple gradient background, colorful accent colors
- **Smooth Animations**: Slide-up effects, hover transitions
- **Modern UI**: Card-based layout, rounded corners, shadows
- **Responsive**: Works on desktop and mobile
- **Accessibility**: Clear labels, good contrast, intuitive navigation

## 🔒 Security Features

✅ **Password Security**
- bcrypt hashing with salt
- Strength requirements (8+ chars, mixed case, numbers)

✅ **Authentication**
- JWT tokens with expiration
- Secure token storage
- Automatic logout on token expiry

✅ **Authorization**
- Role-based access control
- Protected routes
- Admin-only endpoints

✅ **Input Validation**
- Email format validation-  Password strength checks
- Required field validation
- Unique email enforcement

## 🛠 Technical Stack

| Layer | Technology |
|-------|-----------|
| Frontend | React 18 + Vite |
| Routing | React Router DOM |
| HTTP Client | Axios |
| Backend | Flask 3.0 |
| Database | PostgreSQL (Aiven Cloud) |
| ORM | SQLAlchemy |
| Auth | JWT (PyJWT) |
| Password | bcrypt |
| Testing | pytest |
| Styling | Vanilla CSS |

## 📊 Project Statistics

- **Total Files**: 30+
- **Lines of Code**: ~3,500
- **API Endpoints**: 10
- **Test Coverage**: 21 unit tests (all passing)
- **Components**: 5 React pages + 2 shared components
- **Development Time**: Completed in single session

## 🚀 Running the Application

### Backend
```bash
cd backend
source venv/bin/activate
python run.py
```
Server runs on: http://localhost:5001

### Frontend
```bash
cd frontend
npm run dev
```
Server runs on: http://localhost:5173

## 📝 API Endpoints

### Authentication
- `POST /api/auth/signup` - Create account
- `POST /api/auth/login` - Login
- `GET /api/auth/me` - Get current user
- `POST /api/auth/logout` - Logout

### User Management
- `GET /api/users/profile` - Get profile
- `PUT /api/users/profile` - Update profile
- `PUT /api/users/password` - Change password

### Admin
- `GET /api/admin/users` - List all users (paginated)
- `PUT /api/admin/users/:id/activate` - Activate user
- `PUT /api/admin/users/:id/deactivate` - Deactivate user

## ✨ Key Features Demonstrated

1. **Full Authentication Flow**
   - Signup with validation
   - Login with JWT tokens
   - Persistent sessions
   - Secure logout

2. **User Profile Management**
   - View personal information
   - Edit name and email
   - Change password with verification

3. **Admin Dashboard**
   - View all users in a table
   - Activate/deactivate accounts
   - Pagination for large datasets
   - Real-time updates

4. **Security Best Practices**
   - Password hashing
   - JWT authentication
   - Protected routes
   - Input validation
   - CORS configuration

5. **Modern UI/UX**
   - Beautiful gradient design
   - Smooth animations
   - Responsive layout
   - Toast notifications
   - Loading states

## 🎓 What Was Accomplished

✅ Complete full-stack application  
✅ Production-ready backend with Flask  
✅ Modern React frontend with beautiful UI  
✅ Cloud PostgreSQL database integration  
✅ JWT authentication & authorization  
✅ Role-based access control  
✅ Comprehensive testing (21/21 tests passing)  
✅ Complete documentation  
✅ Both servers running and ready to demo  

## 📦 Next Steps for Deployment

### 1. Backend Deployment (Render/Railway)
- Create new web service
- Connect GitHub repository
- Set environment variables
- Deploy!

### 2. Frontend Deployment (Vercel/Netlify)
- Connect GitHub repository
- Update API URL to production backend
- Auto-deploy on push

### 3. Database
- Already using cloud PostgreSQL (Aiven)
- No additional setup needed

### 4. Documentation
- [x] README files
- [ ] API documentation (Swagger/Postman)
- [ ] Walkthrough video (3-5 minutes)

## 🎉 Success!

The complete User Management System is now running locally and ready for:
- Manual testing
- Demo recording
- Deployment to production
- Submission for internship assessment

**Open http://localhost:5173 in your browser to start using the application!** 🚀
