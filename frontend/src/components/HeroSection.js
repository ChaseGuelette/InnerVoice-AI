import React, { useState } from 'react';
import ChatHistory from './ChatHistory';
import RecordingButton from './RecordingButton';
import './HeroSection.css';
import api from '../api';

function HeroSection() {
  const [isLoggedIn, setIsLoggedIn] = useState(false);
  const [user, setUser] = useState(null);

  const handleLogin = async (username, password, preferredName) => {
    try {
      const response = await api.post('/login', { username, password, preferredName });
      setUser(response.data);
      setIsLoggedIn(true);
    } catch (error) {
      console.error('Login error:', error);
    }
  };

  return (
    <div className='hero-container'>
      <div className='video-box'>
        <video src='/images/video2.mp4' autoPlay loop muted />
      </div>
      <div className='chat-box'>
          <>
            <ChatHistory />
            <RecordingButton />
          </>
      </div>
    </div>
  );
}

const LoginForm = ({ onLogin }) => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [preferredName, setPreferredName] = useState('');

  const handleSubmit = (e) => {
    e.preventDefault();
    onLogin(username, password, preferredName);
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

export default HeroSection;
