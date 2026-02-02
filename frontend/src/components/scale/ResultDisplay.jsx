import React from 'react';

const ResultDisplay = ({ result }) => {
    return (
        <div className="max-w-2xl mx-auto bg-white rounded-lgg shadow-lg p-8">
            <div className="text-center">
                <div className="mb-6">
                    <span className="text-6xl">☑</span>
                </div>
                <h2 className="text-3xl font bold mb-4">評量完畢！☺</h2>

                /*sshow result*/
                <div className="bg-blue-50 border-1-4 border-blue-500 p-6 mb-6">
                    <div className="text-left">
                        <p className="text-gray-600 mb-2">☀ 您的得分：</p>
                        <p className="text-5xl font-bold text-blue-600 mb-4">{result.score}</p>
                        <p className="text-text-gray-600 mb-2">☀ 評量結果：</p>
                        <p className="text--2xl font-semiblod text-gray-800">{result.result}</p>
                    </div>
                </div>

                <p className="text-gray-600 mb-6">{result.message}</p>

                <div className="space-x-4">
                    <button
                        onClick={() => window.location.href = '/'}
                        className="bg-blue-600 text-white px-6 py-2 rounded hover:bg-blue-700"
                    >
                        回到首頁
                    </button>

                    <button
                        onClick={() => window.location.href = '/'}
                        className="bg-gray-200 text-gray-800 px-6 py-2 rounded hover:bg-gray-300"
                    >
                        完成其他評量
                    </button>

                    <button
                        onClick={() => window.location.href = '/history'}
                        className="bg-gray-200 text-gray-800 px-6 py-2 rounded hover:bg-gray-300"
                    >
                        查看歷史評量
                    </button>

                </div>
            </div>
        </div>
    );
};

export default ResultDisplay;