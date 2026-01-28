import React from 'react';
import { Link } from 'react-router-dom';

const Header = () => {
    return (
        <header className="bg-blue-600 text-white shadow-md">
            <div className="container mx-auto px-4 py-4 flex justify-between items-center">
                <Link to="/" className="text-2xl font-bold">
                    醫療量表平台系統
                </Link>
                <nav className="space-x-6">
                    <Link to="/" className="hover:underline">首頁</Link>
                    <Link to="/scales" className="hover:underline">量表列表</Link>
                    <Link to="/login" className="hover:underline">登入</Link>"
                    <Link to="/history" className="hover:underline">查看歷史紀錄</Link>
                    <Link to="/about" className="hover:underline">關於我們</Link>
                </nav>
            </div>
        </header>
    );
};

export default Header;