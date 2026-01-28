import axios from 'axios'; // import http client library

//built axios instance
const api = axios.create({
  baseURL: '/api',
    headers: {
        'Content-Type': 'application/json',
    },
});

//GET a sscale
export const getScale = async (scaleId) => {
    const response = await api.get(`/scales/${scaleId}`);
    return response.data;

//submit responses
export const submitScaleResponses = async (scaleId, answers, userID =null) => {
    const response = await api.post('/scales/${scaledID}/responses', {
        answers,
        user_id: userId,
    })
    return response.data;
    };

//GET history
export const getUserHistory = a


