import React from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';

export const Navbar = () => {
    const { user, isAdmin, logout } = useAuth();
    const navigate = useNavigate();

    const handleLogout = () => {
        logout();
        navigate('/login');
    };

    if (!user) return null;

    return (
        <nav className="navbar">
            <div className="navbar-content">
                <Link to="/dashboard" className="navbar-brand">
                    <span>🎯</span>
                    UserHub
                </Link>

                <div className="navbar-menu">
                    <Link to="/dashboard" className="navbar-link">
                        Dashboard
                    </Link>
                    <Link to="/profile" className="navbar-link">
                        Profile
                    </Link>
                    {isAdmin && (
                        <Link to="/admin" className="navbar-link">
                            Admin Panel
                        </Link>
                    )}
                </div>

                <div className="navbar-user">
                    <span style={{ color: 'var(--gray-700)', fontWeight: 500 }}>
                        {user.full_name}
                    </span>
                    <span className={`user-badge ${isAdmin ? 'admin' : ''}`}>
                        {user.role}
                    </span>
                    <button onClick={handleLogout} className="btn btn-secondary btn-sm">
                        Logout
                    </button>
                </div>
            </div>
        </nav>
    );
};
