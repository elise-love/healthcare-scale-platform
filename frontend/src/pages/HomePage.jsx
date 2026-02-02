import React from 'react';
import { Link } from 'react-router-dom';

const HomePage = () => {
    //fetch available scalessss from API
    const availableScales = [
        { id: 'GDS-15', name: '老人憂鬱量表 Geriatric Depression Scale', description: '是一份專為高齡者設計的情緒篩檢工具，用於評估近一週內是否出現憂鬱相關情緒與心理狀態。量表共包含 15 題是非題，題目內容聚焦於生活滿意度、活動興趣、情緒感受、精力狀態與自我價值感等面向，填寫方式簡單，適合由長者自行填答，或在醫療與照護人員協助下完成。' },
        //add more scales here!!!!
    ];

    return (
        <div className="container mx-auto px-4 py-8">
            <div className="text-center mb-12">
                <h1 className="text-4xl font-bold mb-4">=ꕤ 歡迎進入健康量表系統！ꕤ</h1>
                <p className="text-gray-600 text-lg">
                    在健康量表系統裡，您可以找到各種健康量表，幫助您評估和了解自己的心理健康狀況。請選擇您想要填寫的量表，開始您的健康之旅吧！
                </p>
            </div>

            <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6 max-w-6xl mx-auto">
            {availableScales.map((scale) => (
                <Link
                    key={scale.id}
                    to={`/scales/${scale.id}` }
                    className="bg-white p-6 rounded-lg shadow-md hover:shadow-xl transition-shadow border-2 border-transparent hover:border-blue-500"
                >
                <h3 className="text-xl font-semibold mb-2"> {scale.name}</h3>
                <p className="text-gray-600">{scale.description}</p>
                    <div className="mt-4 text-blue-500 font-semibold">開始填寫 ⮕ </div>"
                
                </Link>
            ))}
            </div>
        </div>
    );
};

export default HomePage;