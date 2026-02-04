import React from 'react';
import { useLocation } from 'react-router-dom';
//import ResultDisplay from '../components/ResultDisplay/ResultDisplay';
import ErrorMessage from '../components/common/ErrorMessage';
import './ResultPage.css';

const ResultPage = () => {
    const Location = useLocation();
    const result = location.state?.result;

    if (!result) {
        return <ErrorMessage message="發收錯誤 ><" />;
    }

    return (
        <div className="resultPageConstainer">
            <ResultDisplay result={result} />
        </div>
    );
};

export default ResultPage;


