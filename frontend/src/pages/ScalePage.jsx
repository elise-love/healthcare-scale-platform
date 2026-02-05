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

    const formatError = (err) => {
        const detail = err.response?.data?.detail;

        // If it's an array (FastAPI validation errors)
        if (Array.isArray(detail)) {
            return detail.map(e => `${e.loc?.join('.')}: ${e.msg}`).join('; ');
        }

        // If it's an object with errors array
        if (typeof detail === 'object' && detail?.errors) {
            return `${detail.message || 'Validation failed'}: ${detail.errors.join(', ')}`;
        }

        // If it's a string
        if (typeof detail === 'string') {
            return detail;
        }

        // Default fallback
        return err.message || '發生未知錯誤';
    };

    //fetch data from server
    useEffect(() => {
        const fetchScale = async () => {
            try {
                const data = await getScale(scaleId);
                setScale(data);
            } catch (err) {
                setError(formatError(err));
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
            setError(formatError(err));
        }
    };

    //conditional rendering
    if (loading) return <Loading />; //show spinner
    if (error) return <ErrorMessage message={error} />;//error message
    if (!scale) return <ErrorMessage message="量表未找到。" />;//api returns nothign

    return (
        <div className="scalePageContainer">
            <div className="scaleHeader">
                <h1 className="scaleTitle">{scale.name}</h1> 

                {scale.description && (
                    <p className="scaleDescription">{scale.description}</p>
                )}
                {/*render description if exists*/}
            </div>

            <ScaleForm scale={scale} onSubmit={handleSubmit} /> {/*callback when submits*/}
        </div>
    );
};

export default ScalePage;