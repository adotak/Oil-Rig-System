import React, { useState, useRef, useEffect } from 'react';
import './chat.css';

interface ChatPanelProps {
  token: string;
}

interface Message {
  id: string;
  sender: 'user' | 'orion';
  text: string;
}

export const ChatPanel: React.FC<ChatPanelProps> = ({ token }) => {
  const [isOpen, setIsOpen] = useState(false);
  const [messages, setMessages] = useState<Message[]>([
    { id: 'msg-0', sender: 'orion', text: 'Hello. I am ORION, your autonomous AI supervisor. How can I assist you with the rig today?' }
  ]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const endOfMessagesRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    endOfMessagesRef.current?.scrollIntoView({ behavior: 'smooth' });
  }, [messages, isOpen]);

  const handleSend = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMsg: Message = { id: Date.now().toString(), sender: 'user', text: input };
    setMessages(prev => [...prev, userMsg]);
    setInput('');
    setIsLoading(true);

    try {
      const res = await fetch('http://localhost:8000/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${token}`
        },
        body: JSON.stringify({ message: userMsg.text })
      });

      if (res.ok) {
        const data = await res.json();
        const orionMsg: Message = { id: (Date.now() + 1).toString(), sender: 'orion', text: data.reply };
        setMessages(prev => [...prev, orionMsg]);
      } else {
        const errormsg: Message = { id: (Date.now() + 1).toString(), sender: 'orion', text: 'Communication error with ORION server.' };
        setMessages(prev => [...prev, errormsg]);
      }
    } catch (err) {
      const errormsg: Message = { id: (Date.now() + 1).toString(), sender: 'orion', text: 'Network error. Cannot reach ORION.' };
      setMessages(prev => [...prev, errormsg]);
    } finally {
      setIsLoading(false);
    }
  };

  const toggleChat = () => setIsOpen(!isOpen);

  return (
    <>
      {/* Floating Chat Button */}
      <button className="chat-toggle-btn" onClick={toggleChat}>
        <span className="chat-icon">💬</span>
        ORION NLP
      </button>

      {/* Sliding Chat Panel */}
      <div className={`chat-panel ${isOpen ? 'open' : ''}`}>
        <div className="chat-header">
          <h3>ORION Supervisor</h3>
          <button className="chat-close" onClick={toggleChat}>×</button>
        </div>
        
        <div className="chat-messages">
          {messages.map(m => (
            <div key={m.id} className={`chat-message ${m.sender}`}>
              <div className="chat-bubble">
                <span dangerouslySetInnerHTML={{ __html: m.text.replace(/\n/g, '<br/>') }} />
              </div>
            </div>
          ))}
          {isLoading && (
            <div className="chat-message orion">
              <div className="chat-bubble typing">
                <span>.</span><span>.</span><span>.</span>
              </div>
            </div>
          )}
          <div ref={endOfMessagesRef} />
        </div>

        <form className="chat-input-area" onSubmit={handleSend}>
          <input 
            type="text" 
            placeholder="Ask about V-101, robots..." 
            value={input}
            onChange={e => setInput(e.target.value)}
            disabled={isLoading}
          />
          <button type="submit" disabled={isLoading || !input.trim()}>Send</button>
        </form>
      </div>
    </>
  );
};
