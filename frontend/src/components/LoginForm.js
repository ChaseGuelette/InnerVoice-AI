import React, { useState } from 'react';
import api from '../api';

const LoginForm = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [preferredName, setPreferredName] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    try {
      const response = await api.post('/login', { username, password, preferredName });
      onLogin(response.data);
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Username:</label>
        <input type="text" value={username} onChange={(e) => setUsername(e.target.value)} />
      </div>
      <div>
        <label>Password:</label>
        <input type="password" value={password} onChange={(e) => setPassword(e.target.value)} />
      </div>
      <div>
        <label>Preferred Name:</label>
        <input type="text" value={preferredName} onChange={(e) => setPreferredName(e.target.value)} />
      </div>
      <button type="submit">Login</button>
    </form>
  );
};

export default LoginForm;
