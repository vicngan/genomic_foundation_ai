import React, { useState, KeyboardEvent, useRef, useEffect } from 'react';

interface Message {
  id: number;
  text: string;
  sender: 'user' | 'ai';
}

const Chatbox: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([
    { id: 1, text: 'Hello! How can I help you with genomic data today?', sender: 'ai' },
    { id: 2, text: 'I have a question about variant analysis.', sender: 'user' },
    { id: 3, text: 'Of course. Please provide the variant ID or coordinates.', sender: 'ai' },
  ]);

  const [newMessage, setNewMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const chatEndRef = useRef<HTMLDivElement>(null);

  const scrollToBottom = () => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages, isLoading]);

  const sendMessage = async () => {
    if (newMessage.trim() === '' || isLoading) return;

    const userMessage: Message = {
      id: Date.now(),
      text: newMessage,
      sender: 'user',
    };

    const updatedMessages = [...messages, userMessage];
    setMessages(updatedMessages);
    setNewMessage('');
    setIsLoading(true);

    try {
      // Replace with your actual AI model's API endpoint
      const response = await fetch('https://api.example.com/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          // Example for authenticating with an API key
          // 'Authorization': `Bearer ${process.env.REACT_APP_AI_API_KEY}`,
        },
        body: JSON.stringify({
          // The request body format depends on your AI API
          history: updatedMessages,
        }),
      });

      if (!response.ok) {
        throw new Error(`API request failed with status ${response.status}`);
      }

      const data = await response.json();

      // Assume the API returns a response like: { reply: "This is the AI's message." }
      const aiMessage: Message = {
        id: Date.now() + 1, // Ensure a unique ID
        text: data.reply,
        sender: 'ai',
      };

      setMessages(prevMessages => [...prevMessages, aiMessage]);

    } catch (error) {
      console.error('Error fetching AI response:', error);
      const errorMessage: Message = {
        id: Date.now() + 1,
        text: 'Sorry, I encountered an error. Please try again.',
        sender: 'ai',
      };
      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (event: KeyboardEvent<HTMLInputElement>) => {
    if (event.key === 'Enter' && !isLoading) {
      sendMessage();
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-lg h-full flex flex-col">
      <div className="p-4 border-b">
        <h2 className="text-xl font-semibold">AI Chat</h2>
      </div>
      <div className="flex-grow p-4 overflow-y-auto h-96">
        {messages.map((message) => (
          <div key={message.id} className="mb-4">
            <div
              className={`p-3 rounded-lg max-w-xs ${
                message.sender === 'user'
                  ? 'bg-blue-500 text-white ml-auto'
                  : 'bg-gray-200 text-gray-800'
              }`}
            >
              {message.text}
            </div>
          </div>
        ))}
        {isLoading && (
          <div className="mb-4">
            <div className="p-3 rounded-lg max-w-xs bg-gray-200 text-gray-800">
              AI is typing...
            </div>
          </div>
        )}
        <div ref={chatEndRef} />
      </div>
      <div className="p-4 border-t">
        <div className="flex">
          <input
            type="text"
            value={newMessage}
            disabled={isLoading}
            onChange={(e) => setNewMessage(e.target.value)}
            onKeyUp={handleKeyPress}
            placeholder="Type your message..."
            className="flex-grow border rounded-l-lg p-2 focus:outline-none focus:ring-2 focus:ring-blue-500"
          />
          <button
            disabled={isLoading}
            onClick={sendMessage}
            className="bg-blue-500 text-white px-4 py-2 rounded-r-lg hover:bg-blue-600 focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-blue-300"
          >
            {isLoading ? '...' : 'Send'}
          </button>
        </div>
      </div>
    </div>
  );
};

export default Chatbox;