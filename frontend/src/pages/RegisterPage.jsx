import React, { useState } from 'react';
import { useNavigate, Link } from 'react-router-dom';
import { registerUser } from '../services/api.js';
import './AuthPage.css';

const RegisterPage = () => {
    const navigate = useNavigate();
    const [email, setEmail] = useState('');
    const [password, setPassword] = useState('');
    const [confirmPassword, setConfirmPassword] = useState('');
    const [error, setError] = useState('');
    const [loading, setLoading] = useState(false);
    const [verificationToken, setVerificationToken] = useState('');

    const formatError = (err) => {
        const detail = err.response?.data?.detail;
        if (typeof detail === 'string') return detail;
        if (Array.isArray(detail)) return detail.map((e) => e.msg).join('; ');
        return err.message || '註冊失敗，請稍後再試';
    };

    const validateEmail = (val) => /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(val);

    const handleSubmit = async (e) => {
        e.preventDefault();
        setError('');
        setVerificationToken('');

        if (!email) return setError('請輸入電子郵件');
        if (!validateEmail(email)) return setError('電子郵件格式不正確');
        if (!password) return setError('請輸入密碼');
        if (password.length < 6) return setError('密碼至少需要 6 個字元');
        if (password !== confirmPassword) return setError('兩次輸入的密碼不一致');

        setLoading(true);
        try {
            const data = await registerUser(email, password);
            setVerificationToken(data.verification_token);
        } catch (err) {
            setError(formatError(err));
        } finally {
            setLoading(false);
        }
    };

    if (verificationToken) {
        return (
            <div className="auth-container">
                <div className="auth-card">
                    <h1 className="auth-title">✅ 註冊成功！</h1>
                    <p className="auth-info">
                        請使用以下驗證 Token 完成電子郵件驗證：
                    </p>
                    <div className="auth-token-box">{verificationToken}</div>
                    <p className="auth-info">
                        點擊下方按鈕前往驗證頁面，或複製 Token 並手動驗證。
                    </p>
                    <button
                        className="auth-btn"
                        onClick={() =>
                            navigate(`/verify-email?token=${verificationToken}`)
                        }
                    >
                        前往驗證電子郵件
                    </button>
                </div>
            </div>
        );
    }

    return (
        <div className="auth-container">
            <div className="auth-card">
                <h1 className="auth-title">註冊 ✎</h1>
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
                        <label htmlFor="password">密碼（至少 6 字元）</label>
                        <input
                            id="password"
                            type="password"
                            value={password}
                            onChange={(e) => setPassword(e.target.value)}
                            placeholder="輸入密碼"
                            autoComplete="new-password"
                        />
                    </div>
                    <div className="auth-field">
                        <label htmlFor="confirmPassword">確認密碼</label>
                        <input
                            id="confirmPassword"
                            type="password"
                            value={confirmPassword}
                            onChange={(e) => setConfirmPassword(e.target.value)}
                            placeholder="再次輸入密碼"
                            autoComplete="new-password"
                        />
                    </div>
                    {error && <p className="auth-error">{error}</p>}
                    <button type="submit" className="auth-btn" disabled={loading}>
                        {loading ? '處理中…' : '註冊'}
                    </button>
                </form>
                <p className="auth-switch">
                    已有帳號？<Link to="/login">立即登入</Link>
                </p>
            </div>
        </div>
    );
};

export default RegisterPage;
