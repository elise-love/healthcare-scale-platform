import React from 'react';
import './ErrorMessage.css';

const ErrorMessage = ({ message }) => {
    return (
        <div className="error-message" role="alert">
            <strong>發生錯誤✖︎~ </strong>
            <span>{message}</span>
        </div>
    );
};

export default ErrorMessage;