import React from 'react';
import { Link } from 'react-router-dom';
import './Header.css';

const Header = () => {
    return (
        <header className="header">
            <div className="container header-content">
                <Link to="/" className="header-logo">
                    醫療量表平台系統 ଘ( 'ω' )ଓ ✙
                </Link>
                <nav className="header-nav">
                    <Link to="/">首頁 ꕤ</Link>
                    <Link to="/scales">量表列表 ☰</Link>
                    <Link to="/login">登入 ✉</Link>
                    <Link to="/history">查看歷史紀錄 ✎</Link>
                    <Link to="/about">關於我們 ❤</Link>
                </nav>
            </div>
        </header>
    );
};

export default Header;