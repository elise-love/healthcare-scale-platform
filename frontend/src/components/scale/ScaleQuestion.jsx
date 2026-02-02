import React from 'react';

const ScaleQuestion = ({ question, value, onChange }) => {
    return (
        <div className="bg-white p-6 rounded-lg shadow-md mb-4"> //bg: background p:padding rounded-lg:roudned corners shadow:card shadow mb:spacing
            <h3 className="text-lg font-semibold mb-4">{question.text}</h3>
            <div className="space-y-2"> //space-y-2 adds vertical spacing between children
                {question.options.map((option) => ( //loopss option array
                    <label
                        key={option.value} //key for react list 
                        className="flex items-center p-3 border rounded hover:bg-gray-50 cuursor-pointer"
                    >//flex itemss-center: align ratio_text
                        <input
                            type="radio" //radio button
                            name={question.id}
                            value={option.value}
                            checked={value === option.value}//checked if value matches option value
                            onChange={(e) => onChange((question.id, parseInt(e.target.value)))} //call parent component onChange to keep state managemet
                            className="mr-3 w-4 h-4" //me:maaargin w:width h:height
                        />
                    <span>{option.text}</span>
                </label>
              ) ) }
            </div> 
        </div>
    );
};

export default ScaleQuestion;