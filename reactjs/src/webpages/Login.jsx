import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import "./login.css";
import Navbar from "../navbar.jsx";

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [status, setStatus] = useState('');
  const navigate = useNavigate();

  const loggedIn = () => {
    navigate("/loggedin");
  }

  const handleLogin = async (e) => {
    e.preventDefault();

    const response = await fetch('http://localhost:5001/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      credentials: "include",
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      // Redirect to homepage on successful login
      console.log("logged in");
      loggedIn();
    } else {
      const data = await response.json();
      setStatus(data.error);
    }
  };

  return (
    <div className="loginContainer">
      <Navbar/>
      <div className="loginForm">
        <h1>Login</h1>
        <input
          type="text"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          placeholder="Username"
          required
        />
        <input
          type="password"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          placeholder="Password"
          required
        />
        <button onClick={handleLogin}>Login</button>
        <p>{status}</p>
      </div>
    </div>
  );
};

export default Login;

