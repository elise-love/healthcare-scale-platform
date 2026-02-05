import React from 'react';
import './ScaleQuestion.css';

const ScaleQuestion = ({ question, options = [], value, onChange }) => {
    const safeOptions = Array.isArray(options) ? options : [];
    //normalize value
    const normalizedValue = value !== null && value !== undefined ? String(value) : null;

    return (
        <div className="scale-question">
            <h3>{question.text}</h3>

            <div className="question-options" role="group" aria-label={question.text}>
                {safeOptions.map((opt) => {
                    const optValue = opt.key;
                    const checked = normalizedValue === String(optValue);

                    //console.log(`  Option ${opt.key}: optValue=${optValue}, checked=${checked}`);

                    return (
                        <button
                            key={`${question.item_id}-${opt.key}`} //ex: gds15_q01-0 / gds15_q01-1
                            type="button"
                            className="option-label"
                            data-checked={checked ? "true" : "false"}
                            aria-pressed={checked}
                            onClick={() => onChange(question.item_id, optValue)}
                        >
                            <span className="option-text">{opt.label}</span>
                        </button>
                    );
                })}
            </div>
        </div>
    );
};

export default ScaleQuestion;