import React, { useState } from 'react';
import { Navbar } from '../components/Navbar';
import { useAuth } from '../context/AuthContext';
import { userAPI } from '../services/api';

export const Profile = () => {
    const { user, updateUser } = useAuth();
    const [editing, setEditing] = useState(false);
    const [formData, setFormData] = useState({
        full_name: user?.full_name || '',
        email: user?.email || ''
    });
    const [passwordData, setPasswordData] = useState({
        current_password: '',
        new_password: '',
        confirm_password: ''
    });
    const [message, setMessage] = useState({ type: '', text: '' });
    const [loading, setLoading] = useState(false);

    const handleProfileUpdate = async (e) => {
        e.preventDefault();
        setMessage({ type: '', text: '' });
        setLoading(true);

        try {
            const response = await userAPI.updateProfile(formData);
            updateUser(response.data);
            setMessage({ type: 'success', text: 'Profile updated successfully!' });
            setEditing(false);
        } catch (err) {
            setMessage({ type: 'error', text: err.response?.data?.message || 'Failed to update profile' });
        } finally {
            setLoading(false);
        }
    };

    const handlePasswordChange = async (e) => {
        e.preventDefault();
        setMessage({ type: '', text: '' });

        if (passwordData.new_password !== passwordData.confirm_password) {
            setMessage({ type: 'error', text: 'New passwords do not match' });
            return;
        }

        setLoading(true);

        try {
            await userAPI.changePassword({
                current_password: passwordData.current_password,
                new_password: passwordData.new_password
            });
            setMessage({ type: 'success', text: 'Password changed successfully!' });
            setPasswordData({ current_password: '', new_password: '', confirm_password: '' });
        } catch (err) {
            setMessage({ type: 'error', text: err.response?.data?.message || 'Failed to change password' });
        } finally {
            setLoading(false);
        }
    };

    return (
        <>
            <Navbar />
            <div className="dashboard">
                <div className="container">
                    <div className="dashboard-header">
                        <h1 className="dashboard-title">Profile Settings</h1>
                        <p className="dashboard-subtitle">Manage your account information</p>
                    </div>

                    {message.text && (
                        <div className={`alert ${message.type === 'success' ? 'alert-success' : 'alert-danger'}`}>
                            <span>{message.type === 'success' ? '✅' : '⚠️'}</span>
                            <span>{message.text}</span>
                        </div>
                    )}

                    {/* Profile Information */}
                    <div className="card">
                        <div className="card-header">
                            <div className="flex-between">
                                <h2 className="card-title">Profile Information</h2>
                                <button
                                    onClick={() => setEditing(!editing)}
                                    className="btn btn-secondary btn-sm"
                                >
                                    {editing ? 'Cancel' : 'Edit'}
                                </button>
                            </div>
                        </div>

                        <form onSubmit={handleProfileUpdate}>
                            <div className="form-group">
                                <label className="form-label">Full Name</label>
                                <input
                                    type="text"
                                    className="form-input"
                                    value={formData.full_name}
                                    onChange={(e) => setFormData({ ...formData, full_name: e.target.value })}
                                    disabled={!editing}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label className="form-label">Email Address</label>
                                <input
                                    type="email"
                                    className="form-input"
                                    value={formData.email}
                                    onChange={(e) => setFormData({ ...formData, email: e.target.value })}
                                    disabled={!editing}
                                    required
                                />
                            </div>

                            {editing && (
                                <button type="submit" className="btn btn-primary" disabled={loading}>
                                    {loading ? 'Saving...' : 'Save Changes'}
                                </button>
                            )}
                        </form>
                    </div>

                    {/* Change Password */}
                    <div className="card">
                        <div className="card-header">
                            <h2 className="card-title">Change Password</h2>
                        </div>

                        <form onSubmit={handlePasswordChange}>
                            <div className="form-group">
                                <label className="form-label">Current Password</label>
                                <input
                                    type="password"
                                    className="form-input"
                                    value={passwordData.current_password}
                                    onChange={(e) => setPasswordData({ ...passwordData, current_password: e.target.value })}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label className="form-label">New Password</label>
                                <input
                                    type="password"
                                    className="form-input"
                                    placeholder="Min 8 characters"
                                    value={passwordData.new_password}
                                    onChange={(e) => setPasswordData({ ...passwordData, new_password: e.target.value })}
                                    required
                                />
                            </div>

                            <div className="form-group">
                                <label className="form-label">Confirm New Password</label>
                                <input
                                    type="password"
                                    className="form-input"
                                    value={passwordData.confirm_password}
                                    onChange={(e) => setPasswordData({ ...passwordData, confirm_password: e.target.value })}
                                    required
                                />
                            </div>

                            <button type="submit" className="btn btn-primary" disabled={loading}>
                                {loading ? 'Changing...' : 'Change Password'}
                            </button>
                        </form>
                    </div>
                </div>
            </div>
        </>
    );
};
