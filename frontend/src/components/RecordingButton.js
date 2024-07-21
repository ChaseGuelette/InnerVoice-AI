import React from 'react';
import api from '../api';

const RecordingButton = () => {
  const handleRecording = async () => {
    try {
      const response = await api.get('/start-recording');
      console.log('Recording response:', response.data);
    } catch (error) {
      console.error('Error starting recording:', error);
    }
  };

  return (
    <button onClick={handleRecording}>Start Recording</button>
  );
};

export default RecordingButton;
