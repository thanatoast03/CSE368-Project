import React from 'react';
import { BrowserRouter as Router, Route, Routes } from 'react-router-dom';
import Home from './webpages/Home';
import Login from './webpages/Login';
import Register from './webpages/Register.jsx';
import Chat from './webpages/Chat.jsx';
import Protector from './webpages/Protector.jsx'

function App() {
  return (
    <Router>
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/register" element={<Register />} />
        <Route path="/loggedIn" element={<Protector element={<Chat />} />} />
      </Routes>
    </Router>
  );
}

export default App;