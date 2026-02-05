import React from 'react';
import './ScaleQuestion.css';

const ScaleQuestion = ({ question, options = [], value, onChange }) => {
    const safeOptions = Array.isArray(options) ? options : [];
    return (
        <div className="scale-question">
            <h3>{question.text}</h3>

            <div className="question-options">
                {safeOptions.map((opt) => (
                    <label
                        key={`${question?.item_id}-${opt.key}`}
                        className="option-label"
                    >

                        <input
                            type="radio"
                            name={question?.item_id}
                            value={opt.key}
                            checked={value === opt .value}
                            onChange={(e) => onChange(question.item_id, parseInt(e.target.value, 10))}
                        />
                        <span>{opt.text}</span>
                    </label>
                ))}
            </div>
        </div>
    );
};

export default ScaleQuestion;