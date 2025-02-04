import { useState } from 'react';
import './App.css';
import { BrowserRouter, Route, Routes } from 'react-router-dom';
import HomePage from './screens/HomePage';
import VideoPage from './screens/VideoPage';
import LoginPage from './screens/LoginPage';
import ProfilePage from './screens/ProfilePage';
import AboutPage from './screens/AboutPage';
import HelpPage from './screens/HelpPage';
import UploadImagePage from './screens/UploadVideoPage';
import MyMediaPage from './screens/MyMediaPage';
import ChatContainer from './components/ChatContainer';
import { AuthProvider } from './AuthContext';
import SignupPage from './screens/SignupPage';
import ProtectedContext from './ProtectedContext';
import { setDoc, doc, addDoc, collection } from "firebase/firestore";
import { db } from "./firebase";


function App() {
  const [isContainerOpen, setIsContainerOpen] = useState(false);
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: 'Hello! How can I help you?',
      isBot: true
    }
  ]);
  const [newMessage, setNewMessage] = useState('');

  const handleSendMessage = (e) => {
    e.preventDefault();
    if (newMessage.trim()) {
      setMessages([...messages, {
        id: messages.length + 1,
        text: newMessage,
        isBot: false
      }]);
      setNewMessage('');
    }
  };

  const video = {
    src: 'Link',
    title: 'United States vs. Japan Game Highlights | 2023 World Baseball Classic Final',
    description: 'Rick Astley performing his hit song "Never Gonna Give You Up".',
    views: '1.2M views',
    timestamp: '3 days ago'
  };






  return (
    <AuthProvider>
    <BrowserRouter>
      <div className="relative">
        <Routes>
          <Route path="/" element={<ProtectedContext><HomePage /></ProtectedContext>} />
          <Route path="/video" element={<ProtectedContext><VideoPage video={video} /></ProtectedContext>} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/profile" element={<ProtectedContext><ProfilePage /></ProtectedContext>} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/help" element={<HelpPage />} />
          <Route path="/upload" element={<ProtectedContext><UploadImagePage /></ProtectedContext>} />
          <Route path="/mymedia" element={<ProtectedContext><MyMediaPage /></ProtectedContext>} />
          <Route path="/signup" element={<SignupPage />} />
        </Routes>

        
        <ChatContainer
          isContainerOpen={isContainerOpen}
          setIsContainerOpen={setIsContainerOpen}
          messages={messages}
          setMessages={setMessages}
          newMessage={newMessage}
          setNewMessage={setNewMessage}
          handleSendMessage={handleSendMessage}
        />


      </div>

    

    </BrowserRouter>
    </AuthProvider>
  );
}


export default App;
