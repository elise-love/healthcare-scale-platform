import React from 'react';
import { useLocation } from 'react-router-dom';
import ResultDisplay from '../components/scale/ResultDisplay';
import ErrorMessage from '../components/common/ErrorMessage';
import './ResultPage.css';

const ResultPage = () => {
    const location = useLocation();
    const result = location.state?.result;

    if (!result) {
        return <ErrorMessage message="發收錯誤 ><" />;
    }

    return (
        <div className="resultPageContainer">
            <ResultDisplay result={result} />
        </div>
    );
};

export default ResultPage;


