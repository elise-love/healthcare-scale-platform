import React from 'react'
import { BrowserRouter, Routes, Route } from 'react-router-dom' 
import Header from './components/common/Header.jsx';
import HomePage from './pages/HomePage.jsx'
import ScalePage from './pages/ScalePage.jsx'
import ResultPage from './pages/ResultPage.jsx'


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
                <Route path="/result" element={<ResultPage />} />
            </Routes>
        </BrowserRouter>
    )
}

export default App
