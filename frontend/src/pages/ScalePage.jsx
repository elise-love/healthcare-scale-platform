import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import { getScale, submitScaleResponses } from '../services/api.js'; 
import ScaleForm from '../components/scale/ScaleForm.jsx'; 
import Loading from '../components/common/Loading.jsx';
import ErrorMessage from '../components/common/ErrorMessage.jsx'; 
import './ScalePage.css';

const ScalePage = () => {
    const { scaleId } = useParams(); //extracts scaleId from URL
    const navigate = useNavigate(); //function to navigate to other routes
    const [scale, setScale] = useState(null); //scale stores fetched scale data. null-> not loaded yet
    const [loading, setLoading] = useState(true);//trackes loading state, True when not loaded yet
    const [error, setError] = useState(null);//null-> no error


    //fetch data from server
    useEffect(() => {
        const fetchScale = async () => {
            try {
                const data = await getScale(scaleId);
                setScale(data);
            } catch (err) {
                setError(err.response?.data?.detail || '無法取得量表資料。');
            } finally {
                setLoading(false);
            }
        };

        fetchScale(); //call async function
    }, [scaleId]);//re-run when scaleId changes

    const handleSubmit = async (answers) => {
        try {
            const result = await submitScaleResponses(scaleId, answers);
            navigate('/results', { state: { result } });
        } catch (err) {
            setError(err.response?.data?.detail || '提交失敗！');
        }
    };

    //conditional rendering
    if (loading) return <Loading />; //show spinner
    if (error) return <ErrorMessage message={error} />;//error message
    if (!scale) return <ErrorMessage message="量表未找到。" />;//api returns nothign

    return (
        <div className="scalePageContainer"> /* classs control layout*/
            <div className="scaleHeader">
                <h1 className="scaleTitle">{scale.name}</h1> 

                {scale.description && (
                    <p className="scaleDescription">{scale.description}</p>
                )} /*render description if exists*/
            </div>

            <ScaleForm scale={scale} onSubmit={handleSubmit} /> /*callback when submits*/ */
        </div>
    );
};

export default ScalePage;