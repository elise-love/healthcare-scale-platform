import React from 'react';

const ErrorMessage = ({ message }) => {
    return(
        <div className = "bg-red-100 border border-red-400 text-red-700 px-4 py-3 rounded relative" role = "alert" >
            <strong className="font-bold" > 發生錯誤✖︎~ </strong>
            <span className = "blcok sm:inline">{message}</span>
        </div >
    );
};
   
export default ErrorMessage;