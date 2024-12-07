import React from 'react';
import { useNavigate } from 'react-router-dom';
import "./home.css";

const Home = () => {
  const navigate = useNavigate();

  const handleRegister = () => {
    navigate('/register');
  };

  const handleLogin = () => {
    navigate('/login');
  };

  return (
    <div className="homeContainer">
      <div className="greeting">
        <h1>Welcome to the Homepage</h1>
      </div>
      <div className="buttonContainer">
        <button onClick={handleRegister}>Register</button>
        <button onClick={handleLogin}>Login</button>
      </div>
      <div>
        <p></p>
      </div>
    </div>
  );
};

export default Home;
