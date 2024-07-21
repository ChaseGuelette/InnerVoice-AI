import React, { useEffect, useState } from 'react';
import api from '../api';

const ChatHistory = () => {
  const [history, setHistory] = useState([]);

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const response = await api.get('/chat-history');
        setHistory(response.data.conversation);
      } catch (error) {
        console.error('Error fetching chat history:', error);
      }
    };

    fetchHistory();
  }, []);

  return (
    <div>
      <h2>Chat History</h2>
      <ul>
        {history.map((message, index) => (
          <li key={index}>
            <strong>{message.role}:</strong> {message.content}
          </li>
        ))}
      </ul>
    </div>
  );
};

export default ChatHistory;
