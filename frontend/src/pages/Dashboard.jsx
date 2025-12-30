import React from 'react';
import { Navbar } from '../components/Navbar';
import { useAuth } from '../context/AuthContext';

export const Dashboard = () => {
    const { user, isAdmin } = useAuth();

    return (
        <>
            <Navbar />
            <div className="dashboard">
                <div className="container">
                    <div className="dashboard-header">
                        <h1 className="dashboard-title">
                            Welcome back, {user?.full_name}! 👋
                        </h1>
                        <p className="dashboard-subtitle">
                            {isAdmin ? 'Admin Dashboard - Manage users and system' : 'User Dashboard - Manage your profile and settings'}
                        </p>
                    </div>

                    <div className="stats-grid">
                        <div className="stat-card">
                            <div className="stat-label">Account Status</div>
                            <div className="stat-value">
                                <span className={`badge ${user?.status === 'active' ? 'badge-success' : 'badge-danger'}`}>
                                    {user?.status}
                                </span>
                            </div>
                        </div>

                        <div className="stat-card">
                            <div className="stat-label">Role</div>
                            <div className="stat-value">
                                <span className={`badge ${isAdmin ? 'badge-secondary' : 'badge-primary'}`}>
                                    {user?.role}
                                </span>
                            </div>
                        </div>

                        <div className="stat-card">
                            <div className="stat-label">Email</div>
                            <div className="stat-value" style={{ fontSize: '1.2rem' }}>
                                {user?.email}
                            </div>
                        </div>
                    </div>

                    <div className="card">
                        <div className="card-header">
                            <h2 className="card-title">Quick Actions</h2>
                        </div>
                        <div className="flex gap-2">
                            <a href="/profile" className="btn btn-primary">
                                📝 Edit Profile
                            </a>
                            {isAdmin && (
                                <a href="/admin" className="btn btn-secondary">
                                    👥 Manage Users
                                </a>
                            )}
                        </div>
                    </div>

                    {!isAdmin && (
                        <div className="card">
                            <div className="card-header">
                                <h2 className="card-title">Account Information</h2>
                            </div>
                            <div className="alert alert-info">
                                <span>ℹ️</span>
                                <div>
                                    <strong>Welcome to UserHub!</strong>
                                    <p style={{ marginTop: '0.5rem', marginBottom: 0 }}>
                                        You can manage your profile, update your information, and change your password from the Profile page.
                                    </p>
                                </div>
                            </div>
                        </div>
                    )}
                </div>
            </div>
        </>
    );
};
