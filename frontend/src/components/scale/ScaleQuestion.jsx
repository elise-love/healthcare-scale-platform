import React from 'react';
import './ScaleQuestion.css';

const ScaleQuestion = ({ question, value, onChange }) => {
    return (
        <div className="scale-question">
            <h3>{question.text}</h3>
            <div className="question-options">
                {question.options.map((option) => (
                    <label
                        key={option.value}
                        className="option-label"
                    >
                        <input
                            type="radio"
                            name={question.id}
                            value={option.value}
                            checked={value === option.value}
                            onChange={(e) => onChange(question.id, parseInt(e.target.value))}
                        />
                        <span>{option.text}</span>
                    </label>
                ))}
            </div>
        </div>
    );
};

export default ScaleQuestion;