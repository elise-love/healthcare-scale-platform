import axios from 'axios'; // import http client library

//built axios instance
const api = axios.create({
  baseURL: '/api',
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true, // send/receive HttpOnly cookies
});

//GET a sscale
export const getScale = async (scaleId) => {
    const response = await api.get(`/scales/${scaleId}`);
    return response.data;
};

//submit responses (user_id comes from server-side JWT cookie, not client)
export const submitScaleResponses = async (scaleId, answers) => {
    const payload = { answers };

    const response = await api.post(`/scales/${scaleId}/responses`, payload);
    return response.data;
};

//GET history
export const getUserHistory = async (userId) => {
  const response = await api.get(`/users/${userId}/history`);
  return response.data;
};

// Auth API calls
export const registerUser = async (email, password) => {
    const response = await api.post('/auth/register', { email, password });
    return response.data;
};

export const verifyEmail = async (token) => {
    const response = await api.post('/auth/verify', { token });
    return response.data;
};

export const loginUser = async (email, password) => {
    const response = await api.post('/auth/login', { email, password });
    return response.data;
};

export const logoutUser = async () => {
    const response = await api.post('/auth/logout');
    return response.data;
};

export const getMe = async () => {
    const response = await api.get('/auth/me');
    return response.data;
};

export default api;
