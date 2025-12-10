import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [message, setMessage] = useState('');
  const [, setResponse] = useState('');
  const [loading, setLoading] = useState(false);
  const [chatHistory, setChatHistory] = useState([]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!message.trim()) return;

    setLoading(true);
    const userMessage = message;
    setMessage('');

    // Add user message to chat history
    setChatHistory(prev => [...prev, { type: 'user', content: userMessage }]);

    try {
      const result = await axios.post('http://127.0.0.1:8000/weather', {
        message: userMessage
      });

      const botResponse = result.data.response;
      setResponse(botResponse);
      
      // Add bot response to chat history
      setChatHistory(prev => [...prev, { type: 'bot', content: botResponse }]);
    } catch (error) {
      console.error('Full error:', error);
      console.error('Error response:', error.response);
      let errorMessage = 'Sorry, there was an error processing your request. Please try again.';
      
      if (error.response) {
        errorMessage = `Server error: ${error.response.status} - ${error.response.data?.detail || 'Unknown error'}`;
      } else if (error.request) {
        errorMessage = 'Cannot connect to server. Please check if the backend is running.';
      }
      
      setResponse(errorMessage);
      setChatHistory(prev => [...prev, { type: 'bot', content: errorMessage }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>🌤️ Weather Assistant</h1>
        <p>Ask me about the weather in any city!</p>
      </header>

      <main className="chat-container">
        <div className="chat-history">
          {chatHistory.length === 0 ? (
            <div className="welcome-message">
              <p>👋 Welcome! Ask me about the weather in any city.</p>
              <p>Try: "What's the weather in New York?" or "How's the weather in Tokyo today?"</p>
            </div>
          ) : (
            chatHistory.map((msg, index) => (
              <div key={index} className={`message ${msg.type}`}>
                <div className="message-content">
                  {msg.content}
                </div>
              </div>
            ))
          )}
          {loading && (
            <div className="message bot">
              <div className="message-content loading">
                <div className="typing-indicator">
                  <span></span>
                  <span></span>
                  <span></span>
                </div>
                Checking weather...
              </div>
            </div>
          )}
        </div>

        <form onSubmit={handleSubmit} className="input-form">
          <div className="input-container">
            <input
              type="text"
              value={message}
              onChange={(e) => setMessage(e.target.value)}
              placeholder="Ask about weather in any city..."
              disabled={loading}
              className="message-input"
            />
            <button 
              type="submit" 
              disabled={loading || !message.trim()}
              className="send-button"
            >
              {loading ? '⏳' : '📤'}
            </button>
          </div>
        </form>
      </main>

      <footer className="App-footer">
        <p>SanchAI Analytics - Weather App Assessment</p>
      </footer>
    </div>
  );
}

export default App;