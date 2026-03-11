import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { loginUser } from '../services/api.js';
import './AuthPage.css';

const LoginPage = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);

    const formatError = (err) => {
        const detail = err.response?.data?.detail;
        if (typeof detail === 'string') return detail;
        return err.message || '登入失敗，請稍後再試';
    };

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');

        if (!email) return setError('請輸入電子郵件');
        if (!password) return setError('請輸入密碼');

        setLoading(true);
        try {
            await loginUser(email, password);
            navigate('/');
        } catch (err) {
            setError(formatError(err));
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="auth-container">
            <div className="auth-card">
                <h1 className="auth-title">登入 ✉</h1>
                <form onSubmit={handleSubmit} className="auth-form">
                    <div className="auth-field">
                        <label htmlFor="email">電子郵件</label>
                        <input
                            id="email"
                            type="email"
                            value={email}
                            onChange={(e) => setEmail(e.target.value)}
                            placeholder="your@email.com"
                            autoComplete="email"
                        />
                    </div>
                    <div className="auth-field">
                        <label htmlFor="password">密碼</label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="輸入密碼"
                            autoComplete="current-password"
                        />
                    </div>
                    {error && <p className="auth-error">{error}</p>}
                    <button type="submit" className="auth-btn" disabled={loading}>
                        {loading ? '登入中…' : '登入'}
                    </button>
                </form>
                <p className="auth-switch">
                    還沒有帳號？<Link to="/register">立即註冊</Link>
                </p>
            </div>
        </div>
    );
};

export default LoginPage;
