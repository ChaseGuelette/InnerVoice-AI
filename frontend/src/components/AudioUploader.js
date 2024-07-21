import React, { useState } from 'react';
import api from '../api';

const AudioUploader = () => {
  const [file, setFile] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    const formData = new FormData();
    formData.append('audio', file);

    try {
      const response = await api.post('/upload-audio', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      });
      console.log('Audio upload response:', response.data);
    } catch (error) {
      console.error('Error uploading audio:', error);
    }
  };

  return (
    <form onSubmit={handleSubmit}>
      <div>
        <label>Upload Audio:</label>
        <input type="file" accept="audio/*" onChange={handleFileChange} />
      </div>
      <button type="submit">Upload</button>
    </form>
  );
};

export default AudioUploader;
