import React from 'react';
import './ResultDisplay.css';

const ResultDisplay = ({ result }) => {
    return (
        <div className="result-container">
            <div className="result-content">
                <div className="result-icon">
                    <span>☑</span>
                </div>
                <h2 className="result-title">評量完畢！☺</h2>

                {/* Show result */}
                <div className="result-box">
                    <div className="result-details">
                        <p className="result-label">☀ 您的得分：</p>
                        <p className="result-score">{result.score}</p>
                        <p className="result-label">☀ 評量結果：</p>
                        <p className="result-text">{result.result}</p>
                    </div>
                </div>

                <p className="result-message">{result.message}</p>

                <div className="result-buttons">
                    <button
                        onClick={() => window.location.href = '/'}
                        className="btn-primary"
                    >
                        回到首頁
                    </button>

                    <button
                        onClick={() => window.location.href = '/'}
                        className="btn-secondary"
                    >
                        完成其他評量
                    </button>

                    <button
                        onClick={() => window.location.href = '/history'}
                        className="btn-secondary"
                    >
                        查看歷史評量
                    </button>
                </div>
            </div>
        </div>
    );
};

export default ResultDisplay;