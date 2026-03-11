import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams, Link } from 'react-router-dom';
import { verifyEmail } from '../services/api.js';
import './AuthPage.css';

const VerifyEmailPage = () => {
    const navigate = useNavigate();
    const [searchParams] = useSearchParams();
    const [token, setToken] = useState(searchParams.get('token') || '');
    const [status, setStatus] = useState('idle'); // idle | loading | success | error
    const [message, setMessage] = useState('');

    const handleVerify = async (e) => {
        if (e) e.preventDefault();
        if (!token) {
            setStatus('error');
            setMessage('請輸入驗證 Token');
            return;
        }
        setStatus('loading');
        try {
            const data = await verifyEmail(token);
            setStatus('success');
            setMessage(data.message);
        } catch (err) {
            setStatus('error');
            const detail = err.response?.data?.detail;
            setMessage(typeof detail === 'string' ? detail : '驗證失敗，請確認 Token 是否正確');
        }
    };

    // Auto-verify if token is in URL
    useEffect(() => {
        if (searchParams.get('token')) {
            handleVerify();
        }
    }, []); // eslint-disable-line react-hooks/exhaustive-deps

    return (
        <div className="auth-container">
            <div className="auth-card">
                <h1 className="auth-title">電子郵件驗證 ✉</h1>

                {status === 'success' ? (
                    <>
                        <p className="auth-success">{message}</p>
                        <button className="auth-btn" onClick={() => navigate('/login')}>
                            前往登入
                        </button>
                    </>
                ) : (
                    <form onSubmit={handleVerify} className="auth-form">
                        <div className="auth-field">
                            <label htmlFor="token">驗證 Token</label>
                            <input
                                id="token"
                                type="text"
                                value={token}
                                onChange={(e) => setToken(e.target.value)}
                                placeholder="貼上驗證 Token"
                            />
                        </div>
                        {status === 'error' && <p className="auth-error">{message}</p>}
                        <button
                            type="submit"
                            className="auth-btn"
                            disabled={status === 'loading'}
                        >
                            {status === 'loading' ? '驗證中…' : '驗證'}
                        </button>
                    </form>
                )}

                <p className="auth-switch">
                    <Link to="/login">返回登入</Link>
                </p>
            </div>
        </div>
    );
};

export default VerifyEmailPage;
