//components\scale\ScaleForm.jsx
import React, { useState } from 'react';
import ScaleQuestion from './ScaleQuestion';
import './ScaleForm.css';

const ScaleForm = ({ scale, onSubmit }) => {
    const [answers, setAnswers] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    const items = Array.isArray(scale?.items) ? scale.items : [];
    const options = Array.isArray(scale?.options) ? scale.options : [];

    if (!scale) {
        return <div className="scale-form"><p>加載量表中...</p></div>
    }

    if (items.length === 0) {
        return (
            <div className="scale-form">
                <p>此量表目前沒有任何問題可供回答。</p>
                <pre style={{ whiteSpace: "pre-wrap" }}>
                    {JSON.stringify(scale, null, 2)}
                </pre>
            </div>
        )
    }

    const handleAnswerChange = (itemId, value) => {
        setAnswers((prev) => ({
            ...prev,
            [itemId]: value,
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        // Validate all questions answered
        const allAnswered = items.every((q) => answers[q.item_id] !== undefined);
        if (!allAnswered) {
            alert('尚有問題未作答完畢！請完成後再次提交');
            return;
        }

        setIsSubmitting(true);
        try {
            await onSubmit(answers);
        } finally {
            setIsSubmitting(false);
        }
    };

    const progress = (Object.keys(answers).length / items.length) * 100;

    return (
        <form onSubmit={handleSubmit} className="scale-form">
            {/* Progress Bar */}
            <div className="progress-section">
                <div className="progress-bar-container">
                    <div
                        className="progress-bar-fill"
                        style={{ width: `${progress}%` }}
                    ></div>
                </div>

                {/* Numeric progress text */}
                <p className="progress-text">
                    {Object.keys(answers).length} of {items.length} answered
                </p>
            </div>

            {/* Questions */}
            {items.map((question) => (
                <ScaleQuestion
                    key={question.item_id}
                    question={question}
                    options={options}
                    value={answers[question.item_id]}
                    onChange={handleAnswerChange}
                />
            ))}

            {/* Submit button */}
            <button
                type="submit"
                disabled={isSubmitting}
                className="submit-button"
            >
                {isSubmitting ? '提交中...' : '提交問卷'}
            </button>
        </form>
    );
};

export default ScaleForm;