import React, { useState, useEffect, useCallback, useRef } from 'react';
import { Navbar } from '../components/Navbar';
import { ConfirmModal } from '../components/ConfirmModal';
import { adminAPI } from '../services/api';

export const AdminPanel = () => {
    const [users, setUsers] = useState([]);
    const [loading, setLoading] = useState(true);
    const [page, setPage] = useState(1);
    const [totalPages, setTotalPages] = useState(1);
    const [message, setMessage] = useState({ type: '', text: '' });

    // Confirmation modal state
    const [confirmModal, setConfirmModal] = useState({
        isOpen: false,
        title: '',
        message: '',
        onConfirm: null,
        type: 'danger'
    });

    const fetchUsers = async (pageNum = 1) => {
        setLoading(true);
        try {
            const response = await adminAPI.getUsers(pageNum, 10);
            setUsers(response.data.users);
            setTotalPages(response.data.pages);
            setPage(pageNum);
        } catch (err) {
            setMessage({ type: 'error', text: 'Failed to fetch users' });
        } finally {
            setLoading(false);
        }
    };

    useEffect(() => {
        fetchUsers();
    }, []);

    // Use ref to prevent double execution (React StrictMode or rapid clicks)
    const isProcessingRef = useRef(false);

    const handleActivate = useCallback(async (e, userId) => {
        // Prevent event bubbling
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }

        // Prevent double execution
        if (isProcessingRef.current) {
            return;
        }

        // Find the user to get their name
        const user = users.find(u => u.id === userId);
        const userName = user ? user.full_name : 'this user';

        // Show confirmation modal
        setConfirmModal({
            isOpen: true,
            title: 'Activate User',
            message: `Are you sure you want to activate ${userName}'s account? This will allow them to access the system.`,
            type: 'success',
            onConfirm: async () => {
                isProcessingRef.current = true;
                setConfirmModal({ ...confirmModal, isOpen: false });

                try {
                    await adminAPI.activateUser(userId);
                    setMessage({ type: 'success', text: 'User activated successfully!' });
                    setTimeout(() => setMessage({ type: '', text: '' }), 3000);
                    fetchUsers(page);
                } catch (err) {
                    setMessage({ type: 'error', text: err.response?.data?.message || 'Failed to activate user' });
                } finally {
                    setTimeout(() => {
                        isProcessingRef.current = false;
                    }, 300);
                }
            }
        });
    }, [users, page]);

    const handleDeactivate = useCallback(async (e, userId) => {
        // Prevent event bubbling
        if (e) {
            e.preventDefault();
            e.stopPropagation();
        }

        // Prevent double execution
        if (isProcessingRef.current) {
            return;
        }

        // Find the user to get their name
        const user = users.find(u => u.id === userId);
        const userName = user ? user.full_name : 'this user';

        // Show confirmation modal
        setConfirmModal({
            isOpen: true,
            title: 'Deactivate User',
            message: `Are you sure you want to deactivate ${userName}'s account? This will prevent them from accessing the system.`,
            type: 'danger',
            onConfirm: async () => {
                isProcessingRef.current = true;
                setConfirmModal({ ...confirmModal, isOpen: false });

                try {
                    setMessage({ type: '', text: '' }); // Clear previous messages
                    await adminAPI.deactivateUser(userId);
                    setMessage({ type: 'success', text: 'User deactivated successfully!' });
                    setTimeout(() => setMessage({ type: '', text: '' }), 3000);
                    fetchUsers(page);
                } catch (err) {
                    console.error('Deactivate error:', err);
                    const errorMsg = err.response?.data?.message || 'Failed to deactivate user';
                    setMessage({ type: 'error', text: errorMsg });
                } finally {
                    setTimeout(() => {
                        isProcessingRef.current = false;
                    }, 300);
                }
            }
        });
    }, [users, page]);

    return (
        <>
            <Navbar />
            <ConfirmModal
                isOpen={confirmModal.isOpen}
                title={confirmModal.title}
                message={confirmModal.message}
                onConfirm={confirmModal.onConfirm}
                onCancel={() => setConfirmModal({ ...confirmModal, isOpen: false })}
                confirmText={confirmModal.type === 'success' ? 'Activate' : 'Deactivate'}
                type={confirmModal.type}
            />
            <div className="dashboard">
                <div className="container">
                    <div className="dashboard-header">
                        <h1 className="dashboard-title">Admin Panel 👥</h1>
                        <p className="dashboard-subtitle">Manage users and their accounts</p>
                    </div>

                    {message.text && (
                        <div className={`alert ${message.type === 'success' ? 'alert-success' : 'alert-danger'}`}>
                            <span>{message.type === 'success' ? '✅' : '⚠️'}</span>
                            <span>{message.text}</span>
                        </div>
                    )}

                    <div className="card">
                        <div className="card-header">
                            <h2 className="card-title">All Users</h2>
                        </div>

                        {loading ? (
                            <div className="loading">
                                <div className="spinner"></div>
                                <p>Loading users...</p>
                            </div>
                        ) : (
                            <>
                                <div className="table-container">
                                    <table className="table">
                                        <thead>
                                            <tr>
                                                <th>ID</th>
                                                <th>Name</th>
                                                <th>Email</th>
                                                <th>Role</th>
                                                <th>Status</th>
                                                <th>Created At</th>
                                                <th>Actions</th>
                                            </tr>
                                        </thead>
                                        <tbody>
                                            {users.map((user) => (
                                                <tr key={user.id}>
                                                    <td>{user.id}</td>
                                                    <td>{user.full_name}</td>
                                                    <td>{user.email}</td>
                                                    <td>
                                                        <span className={`badge ${user.role === 'admin' ? 'badge-secondary' : 'badge-primary'}`}>
                                                            {user.role}
                                                        </span>
                                                    </td>
                                                    <td>
                                                        <span className={`badge ${user.status === 'active' ? 'badge-success' : 'badge-danger'}`}>
                                                            {user.status}
                                                        </span>
                                                    </td>
                                                    <td>
                                                        {new Date(user.created_at).toLocaleDateString()}
                                                    </td>
                                                    <td>
                                                        <div className="flex gap-2">
                                                            {user.status === 'inactive' ? (
                                                                <button
                                                                    type="button"
                                                                    onClick={(e) => handleActivate(e, user.id)}
                                                                    className="btn btn-success btn-sm"
                                                                >
                                                                    Activate
                                                                </button>
                                                            ) : (
                                                                <button
                                                                    type="button"
                                                                    onClick={(e) => handleDeactivate(e, user.id)}
                                                                    className="btn btn-danger btn-sm"
                                                                >
                                                                    Deactivate
                                                                </button>
                                                            )}
                                                        </div>
                                                    </td>
                                                </tr>
                                            ))}
                                        </tbody>
                                    </table>
                                </div>

                                {/* Pagination */}
                                {totalPages > 1 && (
                                    <div className="pagination">
                                        <button
                                            className="pagination-btn"
                                            onClick={() => fetchUsers(page - 1)}
                                            disabled={page === 1}
                                        >
                                            ← Previous
                                        </button>

                                        {[...Array(totalPages)].map((_, i) => (
                                            <button
                                                key={i + 1}
                                                className={`pagination-btn ${page === i + 1 ? 'active' : ''}`}
                                                onClick={() => fetchUsers(i + 1)}
                                            >
                                                {i + 1}
                                            </button>
                                        ))}

                                        <button
                                            className="pagination-btn"
                                            onClick={() => fetchUsers(page + 1)}
                                            disabled={page === totalPages}
                                        >
                                            Next →
                                        </button>
                                    </div>
                                )}
                            </>
                        )}
                    </div>
                </div>
            </div>
        </>
    );
};
