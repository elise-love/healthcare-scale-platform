import React from 'react';
import { Link } from 'react-router-dom';
import './HomePage.css';

const HomePage = () => {
    //fetch available scalessss from API
    const availableScales = [ 
        {
            id: 'GDS-15',
            name: (
                <>
                    老人憂鬱量表
                    <br />
                    Geriatric Depression Scale
                </>
            ),
            description:
                '是一份專為高齡者設計的情緒篩檢工具，用於評估近一週內是否出現憂鬱相關情緒與心理狀態。',
        },

        //add more scales here!!!!
    ];

    return (
        <div className="container homepage-container">
            <div className="homepage-header">
                <h1 className="homepage-title">ꕤ 歡迎進入健康量表系統！ꕤ</h1>
                <p className="homepage-description">
                    在健康量表系統裡，您可以找到各種健康量表，幫助您評估和了解自己的心理健康狀況。
                </p>
                <p className="homepage-description">
                    請選擇您想要填寫的量表，開始您的健康之旅吧！
                </p>
            </div>

            <div className="scales-grid">
                {availableScales.map((scale) => (
                    <Link
                        key={scale.id}
                        to={`/scales/${scale.id}`}
                        className="scale-card"
                    >
                        <h3>{scale.name}</h3>
                        <p>{scale.description}</p>
                        <div className="scale-card-footer">開始填寫 ⮕</div>
                    </Link>
                ))}
            </div>
        </div>
    );
};

export default HomePage;