import React, { useState } from 'react';
import "./login.css";
import Navbar from "../navbar.jsx";

const Login = () => {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();

    const response = await fetch('http://localhost:5001/login', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({ username, password }),
    });

    if (response.ok) {
      // Redirect to homepage on successful login
      window.location.href = '/'; // Redirect to homepage
    } else {
      const data = await response.json();
      alert(data.error || 'Login failed');
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
        <button onClick={handleSubmit}>Login</button>
      </div>
    </div>
  );
};

export default Login;

