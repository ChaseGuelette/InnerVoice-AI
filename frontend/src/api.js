import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:5000', // Make sure this matches your Flask backend URL
});

export default api;
