import React from 'react';
import '../App.css';
import { Button } from './Button';
import './HeroSection.css';

function HeroSection() {
  return (
    <div className='hero-container'>

      <div className='video-box'>
        <video src='../../public/images/video2.mp4' autoPlay loop muted />
      </div>
      <div className='chat-box'>
        <div id="chatHistory" class="chat-history">
              <div class="chat-history-header">
                <h2>Chat History</h2>
              </div>
              <div class="chat-history-messages">
                {/* Chat messages will be inserted here  */}
              </div>
        </div>
        
        <button type="button" onclick="submitForm()">Start Recording</button>

        <p id="responseText"></p>
        <audio id="audio" controls hidden preload="auto">
            <source id="audioSource" src="{{ url_for('static', filename='output.mp3') }}" type="audio/mpeg" />
        </audio>
      </div>

    </div>
  );
}

export default HeroSection;
