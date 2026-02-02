import React, { useState } from 'react';
import ScaleQuestion from './ScaleQuestion';

const ScaleForm = ({ scale, onSubmit }) => {
    const [answers, setAnswers] = useState({});
    const [isSubmitting, setIsSubmitting] = useState(false);

    const handleAnswerChange = (questionId, value) => {
        setAnswers((prev) => ({ //previous answer obj
            ...prev,//copies all previous answers
            [questionId]: value, //adds or updates one specific answer
        }));
    };

    const handleSubmit = async (e) => {
        e.preventDefault();

        //validate all quesstions answwered
        const allAnswered = scale.questions.every((q) => answers[q.id] !== undefined) //scale.quuestions: array of questions .every(...):check all elements
        if (!allAnswered) {
            alert('尚有問題未作答完畢！請完成後再次提交')
            return;
        }

        setIsSubmitting(true);
        try {
            await onSubmit(answers);
        } finally {
            setIsSubmitting(false);
        }
    };

    const progress = (Object.keys(answers).length / scale.questions.length) * 100; //Obj.keys(awws).length: how many questions anwered / scale.questions.length: total questions

    return (
        <form onSubmit={handleSubmit} className="max-w-3xl mx-auto"> /*React Controlled submit*/
            /* Progress Bar */
            <div className="mb-6"> /*margin bottom 6*/
                <div className="w-full bg-gray-200 rounded-full h-2"> /*gray background*/
                    /*inner bar*/
                    <div
                        className="bg-blue-600 h-2 rounded-full transition-all duration-300"
                        style={{ width: `${progress}%` }}
                    ></div>
                </div>

                /*numeric progresst text */
                <p className="text-sm text-gray-600 mt-2">
                    {Object.keys(answers).length} of {scale.questions.length} answered
                </p>
            </div>

            /* Questions*/
            {scale.questions.map((question) => ( /*loops through questions aarray*/
                <ScaleQuestion
                    key={question.id} /*key for Reaact list*/
                    question={question} /*passses full question obj*/
                    value={answers[question.id]} /*if unanswered -> uundefined*/
                    onChange={handleAnswerChange}/*passses callback*/
                />
            ))}

            /*submit button */
            <button
                type="submit"
                disabled={isSubmitting}
                className="w-full bg-blue-600 text-white py-3 rounded-lg font-semibold hover:bg-blue-700 diabled:bg-gray-400 disabled: cursor-not-allowed"
            >
                {isSubmitting ? '提交中...' : '提交問卷'}
            </button>
        </form>
    );
};

export default ScaleForm;