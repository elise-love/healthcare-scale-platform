import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom' 
import Header from './components/common/Header.jsx';
import HomePage from './pages/HomePage.jsx'
import ScalePage from './pages/ScalePage.jsx'
import ResultPage from './pages/ResultPage.jsx'
import LoginPage from './pages/LoginPage.jsx'
import RegisterPage from './pages/RegisterPage.jsx'
import VerifyEmailPage from './pages/VerifyEmailPage.jsx'

import './App.css'

//React component
function App() {
    return (
        <BrowserRouter>
            <Header>
            </Header>
            <Routes>
                <Route path="/" element={<HomePage />} />
                <Route path="/scales/:scaleId" element={<ScalePage />} />
                <Route path="/results" element={<ResultPage />} />
                <Route path="/login" element={<LoginPage />} />
                <Route path="/register" element={<RegisterPage />} />
                <Route path="/verify-email" element={<VerifyEmailPage />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
